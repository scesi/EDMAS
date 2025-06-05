from django.urls import path
from .views import ScanListView, ScanDetailView, ScanSD, DNSGraphView, dns_graph_data, Scanhttpx, viewHttpx

urlpatterns = [
    path('', ScanListView.as_view(), name='scan-list'),
    path('scan/<int:pk>/', ScanDetailView.as_view(), name='scan-detail'),
    path('dnsx/', ScanSD.as_view(), name='dnsx_list'),
    path('httpx/', Scanhttpx.as_view(), name='httpx_list'),
    path('httpx/<int:pk>', viewHttpx.as_view(), name='httpx_view'),
    path('graph/', DNSGraphView.as_view(), name='dns-graph'),
    path('api/graph/', dns_graph_data, name='dns-graph-data'),
]
