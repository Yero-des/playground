from datetime import date
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    today = date.today()
    context = {
        "name": "Yeromi",
        "today": today,
        "last_name": "Zavala Castillo",
        "languages": [
            "python",
            "php",
            "c++",
            "javascript"
        ]
    }
    return render(request, "landing/landing.html", context)