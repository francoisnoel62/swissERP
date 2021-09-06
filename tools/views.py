import csv

from django.shortcuts import render, redirect

from contacts.models import Contact
from .forms import ImportContactsModelForm
from .models import ContactsImport


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
        form = ImportContactsModelForm()
    return render(request, 'tools/contacts_import.html', {'form': form})
