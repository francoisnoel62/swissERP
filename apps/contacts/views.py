from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from next_prev import next_in_order, prev_in_order

from apps.sale.models import SaleOrderLine

from .forms import ContactsModelForm, ImportContactsModelForm
from .models import Contact
from .utils import filter_contacts


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    template_name = 'contacts/contacts_listview.html'
    context_object_name = 'contacts_list'

    def get_queryset(self):
        if list(self.request.GET):
            filter_in_request = list(self.request.GET)
            if not filter_in_request:
                return Contact.objects.filter(user_id=self.request.user)
            else:
                contacts_filter = list(self.request.GET)[0]
                filtered_contacts = filter_contacts(self.request, contacts_filter)
                return filtered_contacts
        else:
            return Contact.objects.filter(user_id=self.request.user)


class DetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'contacts/contacts_other_infos.html'
    model = Contact

    def get_context_data(self, **kwargs):
        products = []
        sale_order_lines = SaleOrderLine.objects.filter(sale_order_id__partner_id=self.object.id).order_by('-sale_order_id__validity_date')
        for line in sale_order_lines:
            products.append(line.product_id)

        context = super().get_context_data(**kwargs)
        context.update(
            {"next": next_in_order(self.object),
             "previous": prev_in_order(self.object),
             "products": products,
             })
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

    def post(self, request, *args, **kwargs):
        try:
            messages.success(self.request, f"contact deleted ✅")
            print(messages)
            return self.delete(request, *args, **kwargs)
        except ProtectedError as e:
            messages.error(self.request, f"⛔️ Enable to delete this object as it is used in other relations !")
            objects_in_relation = e.args[1]
            for element in objects_in_relation:
                messages.info(self.request, f"{element}")
            return redirect(self.success_url)


def toggle_active(request, contact_id):
    contact = Contact.objects.get(pk=contact_id)
    contact.is_active = not contact.is_active
    contact.save()
    return redirect('contacts')


def upload_file(request):
    if request.method == 'POST':
        form = ImportContactsModelForm(request.POST, request.FILES)
        if form.is_valid():
            file_id = form.save()
            Contact.process_data(file=file_id, current_user=request.user)
            messages.success(request, "Contacts import completed ✅")
            return redirect("contacts")
        else:
            messages.error(request, "⚠️Please use CSV file format")
    else:
        messages.info(request, "Please enter your CSV file below 👇")
        form = ImportContactsModelForm()
    return render(request, 'contacts/contacts_import.html', {'form': form})
