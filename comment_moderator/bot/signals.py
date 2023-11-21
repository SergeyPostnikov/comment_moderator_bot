import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from .models import Comment
from telegram.ext import Updater, CallbackQueryHandler


def button_click(update, context):
    query = update.callback_query
    query.answer()

    instance = context.user_data['comment']

    if query.data == 'publish':
        instance.status = 'published'
        instance.save()
        query.edit_message_text(text="Комментарий опубликован.")
    elif query.data == 'reject':
        query.edit_message_text(text="Комментарий отклонен.")


TOKEN = settings.TG_KEY
# bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CallbackQueryHandler(button_click))

updater_thread = threading.Thread(target=updater.start_polling)
updater_thread.start()


@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, **kwargs):
    if isinstance.status == 'published':
        return

    chat_id = settings.ADMIN_ID
    message_text = f"Новый комментарий:\n\n{instance.text}"

    # Создание InlineKeyboard с двумя кнопками
    keyboard = [
        [InlineKeyboardButton("Опубликовать", callback_data='publish')],
        [InlineKeyboardButton("Отклонить", callback_data='reject')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        context = {'user_data': {'comment': instance}}
        updater.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=reply_markup,
            context=context
        )
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
