from django.db import models
from django.utils import timezone

class ScanJob(models.Model):
    STATE_CHOICES = [
        ('PENDING', 'Pending'),
        ('STARTED', 'Started'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ]
    target = models.CharField(max_length=255)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    raw_output = models.TextField(blank=True)
    subdomains = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"ScanJob {self.id} - {self.target} ({self.state})"
