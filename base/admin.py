from django.contrib import admin
from .models import CustomUser, Champion, Category, Enemy, Flag
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Champion)
admin.site.register(CustomUser)
admin.site.register(Enemy)
admin.site.register(Flag)