from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.forms import RegisterForm

from accounts.services.email_confirmation import (
    confirm_email,
    InvalidConfirmationCode,
    ExpiredConfirmationCode,
    UsedConfirmationCode,
    create_email_confirmation,
    send_confirmation_email
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
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            confirmation = create_email_confirmation(user)
            send_confirmation_email(user, confirmation)

            return redirect('accounts:confirm_email')
    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

