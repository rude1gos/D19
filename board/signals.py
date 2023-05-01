from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from mmorpg import settings
from board.models import Reply, SubscribedUsers
from protect.models import NewsToSend


def send_email_notif(reply, title, template, subscribers_email):
    #берет за основу шаблон и создает текст письма
    html_mail = render_to_string(
        template,
        {
            'text': reply,
        }
    )

    message = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email
    )

    message.attach_alternative(html_mail, 'text/html')
    message.send()


#обработчик сиглана на добавление отклика
@receiver(post_save, sender=Reply)
def new_reply_added(sender, instance, **kwargs):
    if kwargs['created'] == True:
        send_email_notif(instance.reply, f'Новый отклик на обьявление {instance.post.title}', 'reply_add_email.html', [instance.user.email])

#обработчик сигнала на принятие отклика
@receiver(post_save, sender=Reply)
def reply_accepted(sender, instance, **kwargs):
    if kwargs['update_fields'] == {'accepted'}:
        send_email_notif(instance.reply, f'Ваш отклик принят. Обьявление: {instance.post.title}', 'reply_add_email.html', [instance.user.email])

#Обработчик сигнала на добавление записи в модель Новостной рассылки.
@receiver(post_save, sender=NewsToSend)
def send_news(sender, instance, **kwargs):
    #Если не черновик - то рассылаем новости
    if not instance.is_draft:
        #print('Рассылаем')
        subscribers = set(SubscribedUsers.objects.all())
        subscribers_emails = []
        for sub_users in subscribers:
            subscribers_emails.append(sub_users.user.email)
        print(subscribers_emails)
        send_email_notif(instance.wysiwyn_text, f'{instance.title}',
                     'protect/news_subscribe.html', subscribers_emails)