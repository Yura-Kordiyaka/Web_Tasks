from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from orders.models import Order


@shared_task
def send_order_delivered_email(user_email, user_first_name, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.is_delivered = True
        order.save(update_fields=["is_delivered"])
        subject = "Your Order Has Been Delivered!"
        message = (f"Dear {user_first_name},\n\nYour order #{order_id} has been successfully delivered!"
                   f"\nThank you for choosing us.")
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    except Order.DoesNotExist:
        pass
