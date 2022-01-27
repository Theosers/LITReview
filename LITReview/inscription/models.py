from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
class User(AbstractUser):
    pass

class UserFollows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')
    class Meta:
        unique_together = ('user', 'followed_user')

User.add_to_class('follow', models.ManyToManyField('self', through=UserFollows, related_name='followers', symmetrical=False))