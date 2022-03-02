from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegistrationForm


def register_view(request: HttpRequest) -> HttpResponse:
    context = {}

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account was created for {email}')
            return redirect('auth:login')
    else:
        form = RegistrationForm()
    context['form'] = form
    return render(request, 'registration/register.html', context)
