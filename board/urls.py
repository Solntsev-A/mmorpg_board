from django.urls import path
from board.views import AdvertisementDetailView, AdvertisementListView
from .views import accept_response_view

app_name = 'board'

urlpatterns = [
    path('', AdvertisementListView.as_view(), name='advertisement_list'),
    path('advertisements/<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    path('responses/<int:pk>/accept/', accept_response_view, name='accept_response'),
]
