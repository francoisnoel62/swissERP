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
                    current_credits = presence.product.unitpass.remaining_classes
                    presence.product.unitpass.remaining_classes -= 1
                    presence.product.unitpass.save()
                    messages.success(request,
                                     f"{presence.attendee} got {current_credits} credits. Has {presence.product.unitpass.remaining_classes} remaining classes on its card now.")
                else:
                    messages.error(request, f"{presence.attendee} has no remaining classes")
        except Exception as e:
            if presence.product.subscription:
                if presence.product.subscription.current_credits > 0:
                    credits = presence.product.subscription.current_credits
                    presence.product.subscription.current_credits -= 1
                    presence.product.subscription.save()
                    messages.success(request,
                                     f"{presence.attendee} got {credits} credit. Has {presence.product.subscription.current_credits} remaining classes this week now.")
                else:
                    messages.error(request, f"{presence.attendee} has no more weekly classes")
