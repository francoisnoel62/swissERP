from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from apps.products.models import Product

from .forms import SessionsModelForm, PresenceFormSet
from .models import Session


# Create your views here.
class SessionsList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    template_name = 'sessions/sessions_list.html'
    context_object_name = 'sessions_list'

    def get_queryset(self):
        return Session.objects.filter(created_by=self.request.user).order_by('date')


class CreateSessionWithPresences(LoginRequiredMixin, generic.CreateView):
    template_name = 'sessions/sessions_form.html'
    form_class = SessionsModelForm

    def get_context_data(self, **kwargs):
        data = super(CreateSessionWithPresences, self).get_context_data(**kwargs)
        products = Product.objects.filter(created_by=self.request.user)

        if self.request.POST:
            data['presences'] = PresenceFormSet(self.request.POST, instance=self.object)
            for form in data['presences']:
                form.fields['product'].queryset = products
        else:
            data['presences'] = PresenceFormSet(instance=self.object)
            for form in data['presences']:
                form.fields['product'].queryset = products
        return data

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        context = self.get_context_data()
        presences = context['presences']
        with transaction.atomic():
            self.object = form.save()
            if presences.is_valid():
                presences.instance = self.object
                presences.save()
        return super().form_valid(form)


class DetailSession(LoginRequiredMixin, generic.DetailView):
    template_name = 'sessions/sessions_detail.html'
    model = Session


class UpdateSession(LoginRequiredMixin, generic.UpdateView):
    template_name = 'sessions/sessions_form.html'
    model = Session
    form_class = SessionsModelForm
    success_url = reverse_lazy('sessions')

    def get_context_data(self, **kwargs):
        data = super(UpdateSession, self).get_context_data(**kwargs)
        products = Product.objects.filter(created_by=self.request.user)

        if self.request.POST:
            data['presences'] = PresenceFormSet(self.request.POST, instance=self.object)
            for form in data['presences']:
                form.fields['product'].queryset = products
        else:
            data['presences'] = PresenceFormSet(instance=self.object)
            for form in data['presences']:
                form.fields['product'].queryset = products
        return data

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        context = self.get_context_data()
        presences = context['presences']
        with transaction.atomic():
            self.object = form.save()
            if presences.is_valid():
                presences.instance = self.object
                presences.save()
        messages.success(self.request, 'Session updated successfully')
        return super().form_valid(form)

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     messages.success(self.request, 'Session updated successfully')
    #     return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Session update failed')
        return response


def validate_session(request, pk):
    session = Session.objects.get(pk=pk)
    session.terminated = True
    session.save()
    return redirect('sessions')


class DeleteSession(LoginRequiredMixin, generic.DeleteView):
    model = Session
    success_url = reverse_lazy('sessions')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Session deleted successfully')
        return self.delete(request, *args, **kwargs)


def update_product_when_selecting_student(request, student_id):
    products = Product.objects.filter(created_by=request.user, student=student_id)
    data = {
        'products': list(products.values('id', 'name', 'student__name'))
    }
    return JsonResponse(data)
