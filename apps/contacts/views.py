import csv
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from next_prev import next_in_order, prev_in_order

from .forms import ContactsModelForm, ImportContactsModelForm
from .models import Contact, ContactsImport


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    template_name = 'contacts/contacts_listview.html'
    context_object_name = 'contacts_list'

    def get_queryset(self):
        query = self.request.GET.get("filter")
        print(f"The query is {query}!")
        if query:
            object_list = Contact.objects.filter(
                Q(name__icontains=query) | Q(lastname__icontains=query)
            )
            return object_list
        return Contact.objects.filter(user_id=self.request.user)


class DetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'contacts/contacts_other_infos.html'
    model = Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = next_in_order(self.object)
        context['previous'] = prev_in_order(self.object)
        return context


class CreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'contacts/contacts_createview.html'
    form_class = ContactsModelForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class EditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'contacts/contacts_createview.html'
    model = Contact
    form_class = ContactsModelForm


class DeleteView(LoginRequiredMixin, generic.DeleteView):
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


def process_data(path_to_csv=False):
    if path_to_csv:
        with open(path_to_csv) as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for row in reader:
                _, created = Contact.objects.get_or_create(
                    is_active=row[0],
                    title=row[1],
                    lang=row[2],
                    lastname=row[3],
                    name=row[4],
                    age=row[5],
                    street=row[6],
                    region_zip=row[7],
                    city=row[8],
                    country=row[9],
                    phone=row[10],
                    mobile=row[11],
                    email=row[12],
                    state=row[13],
                )


def upload_file(request):
    if request.method == 'POST':
        form = ImportContactsModelForm(request.POST, request.FILES)
        if form.is_valid():
            file_id = form.save()
            doc = ContactsImport.objects.get(pk=file_id.id)
            process_data(path_to_csv=doc.file.path)
            return redirect("contacts")
        else:
            messages.error(request, "Please use CSV file format !")
    else:
        form = ImportContactsModelForm()
    return render(request, 'contacts/contacts_import.html', {'form': form})
