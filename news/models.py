from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):
    POST_TYPES = (
        ('news', 'News'),
        ('article', 'Article'),
    )
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    content = models.TextField()
    post_type = models.CharField(max_length=7, choices=POST_TYPES)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} subscribed to {self.category.name}'
