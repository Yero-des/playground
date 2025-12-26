# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
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
    list_items = ""
    days = list(days_of_week.keys()) # [monday, tuesday...]
    
    for day in days:
        day_path = reverse('day-quote', args=[day])
        list_items += f"<li><a href='{day_path}'>{day}</a></li>"
    
    response_html = f"<ul>{list_items}</ul>"
    # print(response_html)
    return HttpResponse(response_html)


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
        return HttpResponse(quote_text)
    except KeyError:
        return HttpResponseNotFound("No hay frases para este dia")    
    
def sum_of_two_numbers(request, number1, number2):
    
    result = number1 + number2
    return HttpResponse(f"The sumatory of the number {number1} and the number {number2} is: {result}")
