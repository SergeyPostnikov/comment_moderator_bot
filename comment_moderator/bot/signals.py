from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from .models import Comment

TOKEN = settings.TG_KEY
bot = Bot(token=TOKEN)


@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, **kwargs):
    chat_id = settings.ADMIN_ID
    message_text = f"Новый комментарий:\n\n{instance.text}"
    
    keyboard = [
        [InlineKeyboardButton("Опубликовать", callback_data='publish'),
         InlineKeyboardButton("Отклонить", callback_data='reject')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        bot.send_message(
            chat_id=chat_id, 
            text=message_text,
            reply_markup=reply_markup
        )
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
