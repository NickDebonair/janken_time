from django.contrib import admin
from .models import CustomUser, Champion, Category, Enemy
# Register your models here.

admin.site.register(Category)
admin.site.register(Champion)
admin.site.register(CustomUser)
admin.site.register(Enemy)