from django.shortcuts import render, redirect
from .forms import ImportContactsModelForm


def upload_file(request):
    if request.method == 'POST':
        form = ImportContactsModelForm(request.POST, request.FILES)
        print(f"The form is : {form}")
        if form.is_valid():
            print("is valid")
            # file is saved
            form.save()
            return redirect("contacts")
        else:
            print("the form is not valid")
    else:
        print("not POST")
        form = ImportContactsModelForm()
    return render(request, 'tools/contacts_import.html', {'form': form})
