from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from telegram import Bot
from .models import Comment

TOKEN = settings.TG_KEY
bot = Bot(token=TOKEN)


@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, **kwargs):
    chat_id = settings.ADMIN_ID
    message_text = f"Новый комментарий:\n\n{instance.text}"

    try:
        bot.send_message(chat_id=chat_id, text=message_text)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
