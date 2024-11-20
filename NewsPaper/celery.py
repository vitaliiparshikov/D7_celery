from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установка модуля настроек Django для 'celery' программы.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')

# Использование строки настроек здесь означает, что воркер не должен сериализовать конфигурационный объект.
# - namespace='CELERY' означает, что все ключи конфигурации celery должны иметь префикс `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузка модуля задач из всех зарегистрированных конфигов приложения Django.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')