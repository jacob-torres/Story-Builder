from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def welcome(request):
    """Welcome page."""
    return render(request, 'welcome.html')
