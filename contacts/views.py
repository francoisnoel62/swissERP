from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from next_prev import next_in_order, prev_in_order

from .forms import ContactsModelForm
from .models import Contact


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    template_name = 'contacts/contacts_listview.html'
    context_object_name = 'contacts_list'
    queryset = Contact.objects.all()


class DetailView(generic.DetailView):
    template_name = 'contacts/contacts_other_infos.html'
    model = Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = next_in_order(self.object)
        context['previous'] = prev_in_order(self.object)
        return context


class CreateView(generic.CreateView):
    template_name = 'contacts/contacts_createview.html'
    form_class = ContactsModelForm


class EditView(generic.UpdateView):
    template_name = 'contacts/contacts_createview.html'
    model = Contact
    form_class = ContactsModelForm


class DeleteView(generic.DeleteView):
    model = Contact
    success_url = reverse_lazy("contacts")

    def delete(self, request, *args, **kwargs):
        deleted_person = super(DeleteView, self).get_object()
        messages.success(self.request, f"{deleted_person.name} was removed from DB  ")
        return super(DeleteView, self).delete(request, *args, **kwargs)


def toggle_active(request, contact_id):
    contact = Contact.objects.get(pk=contact_id)
    contact.is_active = not contact.is_active
    contact.save()
    return redirect('contacts')

