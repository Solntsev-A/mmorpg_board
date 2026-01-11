from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from accounts.services.email_confirmation import (
    confirm_email,
    InvalidConfirmationCode,
    ExpiredConfirmationCode,
    UsedConfirmationCode,
)


def confirm_email_view(request):
    context = {}

    if request.method == 'POST':
        code = request.POST.get('code')

        try:
            confirm_email(code)
            context['success'] = True
        except InvalidConfirmationCode as e:
            context['error'] = str(e)
        except ExpiredConfirmationCode as e:
            context['error'] = str(e)
        except UsedConfirmationCode as e:
            context['error'] = str(e)

    return render(request, 'accounts/confirm_email.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserCreationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )
