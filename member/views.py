from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as django_login

# Create your views here.

def signup(request):
    form =UserCreationForm(request.POST or None)    # 아래 코드와 같음
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    context = {
        "form": form,
    }
    return render(request, "", context)


def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())

        next = request.GET.get()
        if next:
            return redirect(next)


        return redirect(reverse(''))

    context = {
        'form': form
    }
    return render(request, '', context)


def logout(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())

        next_url = request.GET.get()
        if next_url:
            return redirect(next_url)

        return redirect(reverse(''))

    context = {
        "form": form,
    }

    return render(request, '', context)