from django.urls import path
from .views import confirm_email_view

app_name = 'accounts'

urlpatterns = [
    path('confirm/', confirm_email_view, name='confirm_email'),
]
