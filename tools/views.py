from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import ScanJob, Dnsx
from .tasks import run_subfinder, run_dnsx, run_httpx
from django.http import JsonResponse
import json


class ScanListView(View):
    def get(self, request):
        scans = ScanJob.objects.all().order_by('-created_at')
        return render(request, 'tools/scan_list.html', {'scans': scans})

    def post(self, request):
        target = request.POST.get('target')
        if target:
            job = ScanJob.objects.create(target=target)
            run_subfinder.delay(job.id)
        return redirect('scan-list')

class Scanhttpx(View):
    def get(self, request):
        scans = Dnsx.objects.all().order_by('-created_at')
        return render(request, 'tools/scan_list.html', {'scans': scans})

    def post(self, request):
        target = request.POST.get('target')
        if target:
            job = Dnsx.objects.create(target=target)
            run_httpx.delay(job.id)
        return redirect('httpx_list')

class viewHttpx(View):
    def get(self, request, pk):
        job = get_object_or_404(Dnsx, pk=pk)
        for a in json.loads(job.raw_output):
            print(a)
        return render(request, 'tools/view_httpx.html', {'job': job.raw_output})

class ScanDetailView(View):
    def get(self, request, pk):
        job = get_object_or_404(ScanJob, pk=pk)
        return render(request, 'tools/scan_detail.html', {'job': job})

class ScanSD(View):
    def get(self, request):
        scans =  Dnsx.objects.all().order_by('-created_at')
        return render(request, 'tools/dnsx_list.html', {'scans': scans})
    
    def post(self, request):
        target = request.POST.get('target')
        if target:
            job = Dnsx.objects.create(target=target)
            run_dnsx.delay(job.id)
        return redirect('dnsx_list')


class DNSGraphView(View):
    def get(self, request):
        domain = request.GET.get('domain')
        if not domain:
            return redirect('scan-list')
        return render(request, 'tools/graph.html', {'domain': domain})

def dns_graph_data(request):
    domain = request.GET.get('domain')
    if not domain:
        return JsonResponse({'error': 'domain parameter required'}, status=400)

    job = Dnsx.objects.filter(target=domain, state='SUCCESS').order_by('-finished_at').first()
    if not job or not job.raw_output:
        return JsonResponse({'nodes': [], 'links': []})

    responses = []
    for line in job.raw_output.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            responses.append(obj)
        except json.JSONDecodeError:
            continue

    nodes = {}
    links = []
    for resp in responses:
        host = resp.get('host')
        if not host:
            continue
        nodes[host] = {'id': host, 'group': 'domain'}
        for ip in resp.get('a', []):
            nodes[ip] = {'id': ip, 'group': 'A_record'}
            links.append({'source': host, 'target': ip, 'type': 'has_A'})
        for resolver in resp.get('resolver', []):
            ip = resolver.split(':')[0]
            nodes[ip] = {'id': ip, 'group': 'resolver'}
            links.append({'source': host, 'target': ip, 'type': 'queried_by'})
        soa_node = f"soa:{host}"
        nodes[soa_node] = {'id': soa_node, 'group': 'SOA'}
        links.append({'source': host, 'target': soa_node, 'type': 'has_SOA'})
        for s in resp.get('soa', []):
            ns = s.get('ns')
            if ns:
                nodes[ns] = {'id': ns, 'group': 'NS'}
                links.append({'source': soa_node, 'target': ns, 'type': 'soa_NS'})
    graph = {'nodes': list(nodes.values()), 'links': links}
    return JsonResponse(graph)
