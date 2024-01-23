from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Заказ № {}'.format(order.id)
    message = 'Уважаем-ый/-ая {},\n\nВы успешно разместили заказ.\
    Номер Вашего заказа {}.'.format(order.name,order.id)
    mail_sent = send_mail(subject, message,'k.krechet@yandex.ru',[order.email])
    return mail_sent