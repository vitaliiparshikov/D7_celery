from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post, Subscriber

@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        subscribers = Subscriber.objects.filter(category__in=instance.categories.all())
        recipient_list = [s.user.email for s in subscribers]
        send_mail(
            subject=f'New post in {instance.categories.first().name}',
            message=f'Read the new post: {instance.title}\n\n{instance.content}\n\nLink: http://127.0.0.1:8000/news/{instance.id}/',
            from_email='your_email@example.com',
            recipient_list=recipient_list
        )