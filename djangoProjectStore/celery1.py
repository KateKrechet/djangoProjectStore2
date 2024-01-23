import os
from celery import Celery


# установка настроек Django по умолчанию для celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProjectStore.settings')
# создание экземпляра приложения
app = Celery('djangoProjectStore')
# загрузка пользовательских конфигураций из настроек нашего проекта
app.config_from_object('django.conf:settings', namespace='CELERY')
# автоматическое обнаружение асинхронных задач
app.autodiscover_tasks()
