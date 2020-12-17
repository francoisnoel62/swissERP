from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Contact


def index(request):
    contacts_list = Contact.objects.all()
    context = {'contacts_list': contacts_list}
    return render(request, 'contacts/contacts_listview.html', context)


def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'contacts/contacts_other_infos.html', {'contact': contact})