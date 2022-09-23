from django.db.models import Q

from apps.contacts.models import Contact


def filter_contacts(request, contacts_filter):
    if contacts_filter == "filter":
        query = request.GET.get("filter")
        if query:
            filtered_contacts = Contact.objects.filter(
                Q(name__icontains=query) | Q(lastname__icontains=query)
            )
            return filtered_contacts
        else:
            return Contact.objects.filter(user_id=request.user)
    elif contacts_filter == 'active':
        return Contact.objects.filter(user_id=request.user, is_active=True)
    elif contacts_filter == 'archived':
        return Contact.objects.filter(user_id=request.user, is_active=False)
    else:
        return Contact.objects.filter(user_id=request.user)

