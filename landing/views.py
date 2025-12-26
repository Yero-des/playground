from datetime import date
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

dev = {
    "name": "Yeromi",
    "last_name": "Zavala Castillo",
    "stack": [
        {
            "id": "python",
            "name": "Python"
        },
        {
            "id": "django",
            "name": "Django"
        },
        {
            "id": "golang",
            "name": "Golang"
        },
        {
            "id": "php",
            "name": "PHP"
        },
        {
            "id": "js",
            "name": "JS"
        }
    ]
}

# Create your views here.
def home(request):
    today = date.today()
    context = {
        "name": dev["name"],
        "today": today,
        "last_name": dev["last_name"],
        "stack": dev["stack"]
    }
    return render(request, "landing/landing.html", context)

def is_tool_included(currency_tool):
    for tool in dev["stack"]:
        if tool["id"] == currency_tool:
            return True
    return False

def stack_detail(request, tool):

    if is_tool_included(tool):
        context = {
            "tool": tool
        }
        return render(request, "landing/stack_detail.html", context)
    else:
        return HttpResponseNotFound("No se encontro la herramienta")