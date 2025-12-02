from .models import Category

def menu(request):
    return {'categories': Category.objects.all()}