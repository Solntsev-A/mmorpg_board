from django.urls import path
from board.views import (AdvertisementDetailView,
                         AdvertisementListView,
                         MyAdvertisementResponsesView,
                         accept_response_view,
                         delete_response_view,
                         MyAdvertisementsView
                         )

app_name = 'board'

urlpatterns = [
    path('', AdvertisementListView.as_view(), name='advertisement_list'),
    path('advertisements/<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    path('my-responses/', MyAdvertisementResponsesView.as_view(), name='my_responses'),
    path('responses/<int:pk>/accept/', accept_response_view, name='accept_response'),
    path('responses/<int:pk>/delete/', delete_response_view, name='delete_response'),
    path('my-advertisements/', MyAdvertisementsView.as_view(), name='my_advertisements'),
]
