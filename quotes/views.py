# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

days_of_week = {
    "monday": "Pienso luego existo",
    "tuesday": "La vida es un sueño",
    "wednesday": "Caminante no hay camino",
    "thursday": "Se el cambio que quieres ver",
    "friday": "Solo se que no se nada",
    "saturday": "Se hace camino al andar",
    "sunday": "Haslo y si tienes miedo haslo con todo y miedo"
}

# Create your views here.
def index(request):
    
    days = list(days_of_week.keys()) # [monday, tuesday...]
    
    context = {
        "days": days,
    }
    return render(request, 'quotes/index.html', context)


def days_week_with_number(request, day):
    
    days = list(days_of_week.keys())
    if day > len(days) or day == 0:
        return HttpResponseNotFound("<h1>El dia no existe</h1>")
    
    redirect_day = days[day-1]
    redirect_path = reverse("day-quote", args=[redirect_day])
    
    return HttpResponseRedirect(redirect_path)

def days_week(request, day):
    
    try:
        quote_text = days_of_week[day]
        
        context = {
            "quote_text": quote_text,
            "day": day,
        }
        
        return render(request, 'quotes/day_quote.html', context)  
        
    except KeyError:
        return HttpResponseNotFound("No hay frases para este dia")    