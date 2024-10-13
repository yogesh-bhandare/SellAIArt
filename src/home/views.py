from django.shortcuts import render
from products.models import Product

def home_view(request):
    obj_qs = Product.objects.order_by('-timestamp')[:4]
    context = {"obj_list": obj_qs}
    return render(request, 'pages/home.html', context)
    # return render(request, 'home.html', {})


