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


class DetailView(generic.DetailView):
    model = Contact
    template_name = 'contacts/contacts_other_infos.html'