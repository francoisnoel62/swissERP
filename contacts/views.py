from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Contact


class IndexView(generic.ListView):
    template_name = 'contacts/contacts_listview.html'
    context_object_name = 'contacts_list'

    def get_queryset(self):
        return Contact.objects.all()


class DetailView(generic.ListView):
    model = Contact
    template_name = 'contacts/contacts_formview.html'

def detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'contacts/contacts_formview.html', {'contact': contact})