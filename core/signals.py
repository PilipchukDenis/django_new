from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from core.utlils import check_review
from .models import Review, Visit
from .telegram_bot import send_telegram_message
from barber.settings import TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID
import asyncio

@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    if created:
        review = instance
        
        # Получаем текст отзыва
        review_text = review.text

        # Проверяем отзыв
        if check_review(review_text):
            # Если прошли проверку, меняем status на  2
            review.status = 2
            # Формируем ТГ сообщение
            message = f"""
*Новый отзыв* 

*Имя:* {review.name} 
*Отзыв:* {review.text or 'не указан'}
*Дата создания:* {review.created_at}
*Ссылка на админ-панель:* http://127.0.0.1:8000/admin/core/review/{review.id}/change/
-------------------------------------------------------------
"""
            # Отправляем ТГ сообщение
            asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))
        else:
            # Если не прошли проверку, меняем status на  3
            review.status = 3
        review.save()


@receiver(m2m_changed, sender=Visit.services.through)
def send_telegram_notification(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для модели Visit.
    Он обрабатывает добавление КАЖДОЙ услуги в запись на консультацию.
    Отправка ОДНОГО сообщения в телеграмм выполняется в первом условии
    http://127.0.0.1:8000/admin/core/visit/5/change/
    """
    if action == 'post_add' and kwargs.get('pk_set'):
        services = [service.name for service in instance.services.all()]
        # print(f"УСЛУГИ: {services}")
        message = f"""
*Новая запись на консультацию* 

*Имя:* {instance.name} 
*Телефон:* {instance.phone or 'не указан'} 
*Комментарий:* {instance.comment or 'не указан'}
*Услуги:* {', '.join(services) or 'не указаны'}
*Дата создания:* {instance.created_at}
*Мастер:* {instance.master.first_name} {instance.master.last_name}
*Ссылка на админ-панель:* http://127.0.0.1:8000/admin/core/visit/{instance.id}/change/
-------------------------------------------------------------
"""
        asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))

