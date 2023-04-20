import django.dispatch
from django.contrib import messages
from django.dispatch import receiver

update_credits_signal = django.dispatch.Signal()


@receiver(update_credits_signal)
def update_credits_handler(request, session, **kwargs):
    presences = session.presence_set.all()
    for presence in presences:
        try:
            if presence.product.unitpass:
                if presence.product.unitpass.remaining_classes > 0:
                    presence.product.unitpass.remaining_classes -= 1
                    presence.product.unitpass.save()
                else:
                    messages.error(request, f"{presence.attendee} has no remaining classes")
        except Exception as e:
            if presence.product.subscription and presence.product.subscription.classes_by_week > 0:
                presence.product.subscription.classes_by_week -= 1
                presence.product.subscription.save()
