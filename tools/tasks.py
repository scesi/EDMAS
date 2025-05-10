import json
import subprocess
from celery import shared_task
from django.utils import timezone
from .models import ScanJob

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
