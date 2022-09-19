from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)


class EditUserView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'registration/edit_user.html'
    model = CustomUser
    form_class = CustomUserChangeForm

    def form_valid(self, form):
        messages.success(self.request, f"Le profil: {self.request.user} has been updated ✅")
        return super(EditUserView, self).form_valid(form)


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
