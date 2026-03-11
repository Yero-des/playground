from datetime import date
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

dev = {
    "name": "Yeromi",
    "last_name": "Zavala Castillo",
    "stack": [
        {
            "id": "python",
            "name": "Python",
            "description": "This is a short description of python."
        },
        {
            "id": "django",
            "name": "Django",
            "description": "This is a funny description about django."
        },
        {
            "id": "golang",
            "name": "Golang",
            "description": "This is a large description about golang"
        },
        {
            "id": "php",
            "name": "PHP",
            "description": "This is a description about php."
        },
        {
            "id": "js",
            "name": "JS",
            "description": "This is a messy description of js."
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
        "stack": dev["stack"],
    }
    return render(request, "landing/landing.html", context)

def get_tool(tool_id):
    return next(
        (tool for tool in dev["stack"] if tool["id"] == tool_id),
        None
    )
    
def stack_detail(request, tool):

    tool_data = get_tool(tool)
    
    if tool_data == None:
        return HttpResponseNotFound("No se encontro la herramienta")
        
    context = {
        "tool": tool_data
    }
    return render(request, "landing/stack_detail.html", context)