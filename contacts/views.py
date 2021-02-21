from django.views import generic

from .models import Contact
from .forms import ContactsModelForm


class IndexView(generic.ListView):
    template_name = 'contacts/contacts_listview.html'
    context_object_name = 'contacts_list'

    def get_queryset(self):
        return Contact.objects.all()


class DetailView(generic.DetailView):
    template_name = 'contacts/contacts_other_infos.html'
    model = Contact


class CreateView(generic.CreateView):
    template_name = 'contacts/contacts_createview.html'
    form_class = ContactsModelForm
    queryset = Contact.objects.all()
