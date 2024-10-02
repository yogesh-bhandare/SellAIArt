from django.shortcuts import render
from .models import PageVisit

# Create your views here.

def PageVisitView(request):
    return render(request, "home.html", {})
