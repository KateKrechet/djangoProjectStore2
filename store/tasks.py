from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from djangoProjectStore import settings


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    print(order.email)
    subject = 'Заказ № {}'.format(order.id)
    message = f'Уважаем -ый/-ая {order.name},\n\nВы успешно разместили заказ на сумму {order.amount_rub} рублей.\
    Номер заказа {order.id}.'
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_sent
