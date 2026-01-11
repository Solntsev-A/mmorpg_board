from django.urls import path
from board.views import advertisement_list

app_name = 'board'

urlpatterns = [
    path('', advertisement_list, name='advertisement_list'),
]
