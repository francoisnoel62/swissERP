from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .models import Contact
from .forms import ContactsModelForm


class IndexView(generic.ListView):
    template_name = 'contacts/contacts_listview.html'
    context_object_name = 'contacts_list'
    queryset = Contact.objects.all()


class DetailView(generic.DetailView):
    template_name = 'contacts/contacts_other_infos.html'
    model = Contact


class CreateView(generic.CreateView):
    template_name = 'contacts/contacts_createview.html'
    form_class = ContactsModelForm


class EditView(generic.UpdateView):
    template_name = 'contacts/contacts_createview.html'
    model = Contact
    form_class = ContactsModelForm
    success_url = reverse_lazy("contacts")


class DeleteView(generic.DeleteView):
    model = Contact
    success_url = reverse_lazy("contacts")


def toggle_active(request, contact_id):
    contact = Contact.objects.get(pk=contact_id)
    contact.is_active = not contact.is_active
    contact.save()
    return redirect('contacts')
