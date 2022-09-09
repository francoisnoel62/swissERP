from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetCompleteView
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateUserForm, UpdateUserForm


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class EditUser(LoginRequiredMixin, generic.UpdateView):
    template_name = 'accounts/edit.html'
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, f"User has been updated successfully !")
        return super(EditUser, self).form_valid(form)


def change_pass(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm(user=request.user)

        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, f"Password has been changed successfully !")
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/change_passw.html', context)
    else:
        return redirect('login')


class PasswordResetCompleteViewInherit(PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url('login')
        return context


def reset_password(request):
    form = PasswordResetForm()

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(domain_override=request.get_host())
            messages.success(request, f"We sent you an e-mail to reset your password. Please check your inbox !")
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/reset_passw.html', context)
