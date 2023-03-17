from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import SessionsModelForm
from .models import Session


# Create your views here.
class SessionsList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    template_name = 'sessions/sessions_list.html'
    context_object_name = 'sessions_list'

    def get_queryset(self):
        return Session.objects.filter(user_id=self.request.user)


class CreateSession(LoginRequiredMixin, generic.CreateView):
    template_name = 'sessions/sessions_form.html'
    form_class = SessionsModelForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class DetailSession(LoginRequiredMixin, generic.DetailView):
    template_name = 'sessions/sessions_detail.html'
    model = Session


class UpdateSession(LoginRequiredMixin, generic.UpdateView):
    template_name = 'sessions/sessions_form.html'
    model = Session
    form_class = SessionsModelForm
    success_url = reverse_lazy('sessions')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Session updated successfully')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Session update failed')
        return response
