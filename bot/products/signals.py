from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
import os
import requests


@receiver(post_save, sender=Order)
def send_telegram_notification(sender, instance, created, **kwargs):
    if created:
        telegram_id = getattr(instance.user, 'telegram_id', None)
        if telegram_id:
            token = os.getenv("TELEGRAM_BOT_TOKEN")
            if not token:
                return
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            message = "Вам пришёл новый заказ!"
            try:
                requests.post(url, data={
                    "chat_id": telegram_id,
                    "text": message
                })
            except requests.RequestException as e:
                print(f"Ошибка отправки уведомления в Telegram: {e}")