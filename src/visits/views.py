from django.shortcuts import render
from .models import PageVisit

# Create your views here.

def PageVisitView(request):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    context = {
        "page_count": page_qs.count(),
        "total_count": qs.count()
    }
    PageVisit.objects.create(path=request.path)
    return render(request, "home.html", context)
