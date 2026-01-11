from django.urls import path
from board.views import AdvertisementDetailView, AdvertisementListView

app_name = 'board'

urlpatterns = [
    path('', AdvertisementListView.as_view(), name='advertisement_list'),
    path('advertisements/<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement_detail'),
]
