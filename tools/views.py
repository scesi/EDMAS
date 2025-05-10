from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import ScanJob
from .tasks import run_subfinder

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

class ScanDetailView(View):
    def get(self, request, pk):
        job = get_object_or_404(ScanJob, pk=pk)
        return render(request, 'tools/scan_detail.html', {'job': job})
