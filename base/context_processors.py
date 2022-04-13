from .models import Category, Flag

def common(request):
    category_data = Category.objects.all()
    flags = Flag.objects.all()
    context = {
        'category_data': category_data,
        'flags': flags,
    }
    return context