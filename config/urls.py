from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    # path('logout/', LogoutView.as_view(next_page="registration/logout.html"), name="logout"), # Personalized next_page
    path('admin/', admin.site.urls),
    path('messages/', include("quotes.urls")),
    path('landings/', include("landing.urls")),
    path('calculator/', include("calculator.urls")),
    path("library/", include('library.urls')),
    path("documentation/", include('documentation.urls')),
]