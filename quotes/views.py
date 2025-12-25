from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

# Create your views here.
def index(request):
    return HttpResponse("Hola mundo desde Django!")

def monday(request):
    return HttpResponse("Hola Lunes")

def tuesday(request):
    return HttpResponse("Hola Tuesday")

days_of_week = {
    "monday": "Pienso luego existo",
    "tuesday": "La vida es un sueño",
    "wednesday": "Caminante no hay camino",
    "thursday": "Se el cambio que quieres ver",
    "friday": "Solo se que no se nada",
    "saturday": "Se hace camino al andar",
    "sunday": "Haslo y si tienes miedo haslo con todo y miedo"
}

def days_week(request, day):
    
    try:
        quote_text = days_of_week[day]
        return HttpResponse(quote_text)
    except KeyError:
        return HttpResponseNotFound("No hay frases para este dia")    

def days_week_with_number(request, day):
    
    days = list(days_of_week.keys())
    if day > len(days) or day == 0:
        return HttpResponseNotFound("El dia no existe")
    redirect_day = days[day-1]
    return HttpResponseRedirect(f"/quotes/{redirect_day}")