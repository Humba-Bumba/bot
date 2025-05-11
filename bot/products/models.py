import requests
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} x {self.quantity} для {self.user.username}"


# @receiver(post_save, sender=Order)
# def send_telegram_notification(sender, instance, created, **kwargs):
#     if created:
#         telegram_id = getattr(instance.user, 'telegram_id', None)
#         if telegram_id:
#             token = settings.TELEGRAM_BOT_TOKEN
#             if not token:
#                 print("TELEGRAM_BOT_TOKEN не задан")
#                 return
#             url = f"https://api.telegram.org/bot{token}/sendMessage"
#             message = "Вам пришёл новый заказ!"
#             try:
#                 requests.post(url, data={
#                     "chat_id": telegram_id,
#                     "text": message
#                 })
#             except requests.RequestException as e:
#                 print(f"Ошибка отправки уведомления в Telegram: {e}")