from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Category(models.Model):
    name = models.CharField('Category', max_length=20)

    def __str__(self):
        return self.name


class Champion(models.Model):
    name = models.CharField(max_length=20)
    category = models.ManyToManyField(Category, verbose_name='Category', blank=True)
    # img_url = models.CharField(max_length=1000, null=True, blank=True)
    picture = models.FileField(null=False, upload_to='character/')
    description = models.TextField(verbose_name='description', blank=True, null=True, max_length=1000)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Champions'

'''
CustomUserの定義
'''

class UserManager(models.Manager): # 追記箇所(3～6行目)

    def pick_by_matches(self):
        return self.order_by('-matches').all()

    def pick_by_wins(self):
        return self.order_by('-wins').all()

    def pick_by_winsrate(self):
        return self.order_by('-wins_rate').all()



class CustomUser(AbstractUser):
    champions = models.ManyToManyField(Champion, blank=True)
    picture = models.FileField(null=True, upload_to='picture/')
    description = models.TextField(verbose_name='description', blank=True, null=True, max_length=1000)
    matches = models.IntegerField(verbose_name='マッチ数', default=0)
    wins = models.IntegerField(verbose_name='防衛数', default=0)
    wins_rate = models.IntegerField(verbose_name='勝率', default=0)
    donations = models.FloatField(verbose_name='寄付額', default=0)

    class Meta:
        verbose_name_plural = 'CustomUser'


'''
Option Enemy
'''

class Enemy(models.Model):
    picture = models.FileField(verbose_name='image', null=True, upload_to='enemy/')


class Flag(models.Model):
    picture = models.FileField(verbose_name='image', null=True, upload_to='flag/')