from datetime import datetime, timedelta
from django.core.mail import send_mail
from .models import Post, Subscriber

def send_weekly_newsletter():
    last_week = datetime.now() - timedelta(days=7)
    posts = Post.objects.filter(pub_date__gte=last_week)
    if posts.exists():
        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            user_posts = posts.filter(categories=subscriber.category)
            if user_posts.exists():
                message = '\n\n'.join([f'{post.title}\n{post.content}\nLink: http://127.0.0.1:8000/news/{post.id}/' for post in user_posts])
                send_mail(
                    subject='Weekly Newsletter',
                    message=message,
                    from_email='your_email@example.com',
                    recipient_list=[subscriber.user.email]
                )


@shared_task
def send_new_post_notification(post_id):
    post = Post.objects.get(id=post_id)
    subscribers = Subscriber.objects.filter(category__in=post.categories.all())
    recipient_list = [subscriber.user.email for subscriber in subscribers]

    send_mail(
        subject=f'New post in {post.categories.first().name}',
        message=f'Read the new post: {post.title}\n\n{post.content}\n\nLink: http://127.0.0.1:8000/news/{post.id}/',
        from_email='your_email@example.com',
        recipient_list=recipient_list
    )
