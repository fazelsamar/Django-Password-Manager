from time import sleep
from celery import shared_task


@shared_task
def send_push_notification(data):
    print('sending push notification')
    print(data)
    sleep(5)
    print('push notification sent')
