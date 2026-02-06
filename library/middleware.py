import time
from django.http import HttpResponseForbidden
from datetime import datetime

from django.shortcuts import redirect

BLOCKED_IPS = []
EXCEPT_URLS = ['/login', '/admin', '/register']

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start = time.time()        
        
        response = self.get_response(request) # Ejecucion de la vista
        
        duration = time.time() - start
        print(f"Tiempo de respuesta: {duration:.2f} segundos")
        
        return response
    

class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        print(f"IP detectada: {ip}")
        
        if ip in BLOCKED_IPS:
            return HttpResponseForbidden("Tu IP está bloqueada.")
        
        return self.get_response(request)
    
class OfficeHoursOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        
        now = datetime.now().hour
        print(f"Hora actual: {now}")
        if now < 9 and now > 18:
            return HttpResponseForbidden("Estas fuera de horario laboral regresa entre las 9:00a.m y las 7:00p.m")
        
        return self.get_response(request)
    

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in EXCEPT_URLS):
            print("Usuario no autenticado, redirigiendo...") 
            return redirect('/admin/')
        
        return self.get_response(request)