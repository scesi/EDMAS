import json
import subprocess
from celery import shared_task
from django.utils import timezone
from .models import ScanJob, Dnsx

@shared_task(bind=True)
def run_subfinder(self, scan_id):
    job = ScanJob.objects.get(id=scan_id)
    job.state = 'STARTED'
    job.started_at = timezone.now()
    job.save()

    # Ejecutar subfinder
    cmd = ['subfinder', '-d', job.target, '-oJ']
    proc = subprocess.run(cmd, capture_output=True, text=True)
    raw = proc.stdout

    # Parsear subdominios
    subs = []
    for line in raw.splitlines():
        try:
            obj = json.loads(line)
            subs.append(obj.get('host'))
        except json.JSONDecodeError:
            continue

    job.raw_output = raw
    job.subdomains = subs
    job.state = 'SUCCESS' if proc.returncode == 0 else 'FAILURE'
    job.finished_at = timezone.now()
    job.save()
    return {'status': job.state}

@shared_task(bind=True)
def run_dnsx(self, scan_id):
    job = Dnsx.objects.get(id=scan_id)
    job.state = 'STARTED'
    job.started_at = timezone.now()
    job.save()

    cmd = f"subfinder -d {job.target} -silent| dnsx  -silent -recon -j"
    proc = subprocess.run(cmd, shell=True,capture_output=True, text=True)
    raw = proc.stdout

    lines = [line.strip() for line in raw.splitlines() if line.strip()]

    job.raw_output = raw
    job.subdomains = lines
    job.state = 'SUCCESS' if proc.returncode == 0 else 'FAILURE'
    job.finished_at = timezone.now()
    job.save()
    return {'status': job.state}

@shared_task(bind=True)
def run_httpx(self, scan_id):
    job = Dnsx.objects.get(id=scan_id)
    job.state = 'STARTED'
    job.started_at = timezone.now()
    job.save()

    cmd = f"subfinder -d {job.target} -silent| dnsx  -silent | httpx -j"
    proc = subprocess.run(cmd, shell=True,capture_output=True, text=True)
    raw = proc.stdout

    lines = [line.strip() for line in raw.splitlines() if line.strip()]

    job.raw_output = raw
    job.subdomains = lines
    job.state = 'SUCCESS' if proc.returncode == 0 else 'FAILURE'
    job.finished_at = timezone.now()
    job.save()
    return {'status': job.state}
