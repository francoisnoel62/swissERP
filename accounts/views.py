from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateUserForm, UpdateUserForm


def landingPage(request):
    return render(request, 'accounts/landing.html', {})


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


class EditUser(LoginRequiredMixin, generic.UpdateView):
    template_name = 'accounts/edit.html'
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('home')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')
