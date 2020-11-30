from django.http import HttpResponse
from django.shortcuts import render

from .models import Contact


def index(request):
    contacts_list = Contact.objects.all()
    context = {'contacts_list': contacts_list}
    return render(request, 'contacts/contacts.html', context)
