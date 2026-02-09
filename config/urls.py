from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('messages/', include("quotes.urls")),
    path('landings/', include("landing.urls")),
    path('calculator/', include("calculator.urls")),
    path("library/", include('library.urls')),
    path("documentation/", include('documentation.urls')),
]