from django.urls import path
from .views import ScanListView, ScanDetailView

urlpatterns = [
    path('', ScanListView.as_view(), name='scan-list'),
    path('scan/<int:pk>/', ScanDetailView.as_view(), name='scan-detail'),
]
