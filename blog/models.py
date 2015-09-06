from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# class User(AbstractBaseUser):
# 	username = models.CharField('username', max_length=30, unique=True)
# 	email =	models.EmailField('email address', unique=True)
# 	firstname = models.CharField('first name', max_length=30)
# 	lastname = models.CharField('last name', max_length=30)
# 	joined = models.DateTimeField(auto_now_add=True)
# 	is_active=models.BooleanField(default=True)
# 	is_admin = models.BooleanField(default=False)
# 	USERNAME_FIELD = 'username'

# 	def __str__(self):
# 		return	self.username


class Article(models.Model):
    headline = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now())
    author = models.ForeignKey(User)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.headline


class Comment(models.Model):
    article = models.ForeignKey(Article)
    content = models.TextField(max_length=30)
    pub_date = models.DateTimeField('date published', default=timezone.now())
    author = models.ForeignKey(User)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.content

