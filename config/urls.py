from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from library.views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    # path('logout/', LogoutView.as_view(next_page="registration/logout.html"), name="logout"), # Personalized next_page en caso se requiera
    path('admin/', admin.site.urls),
    path('messages/', include("quotes.urls")),
    path('landings/', include("landing.urls")),
    path('calculator/', include("calculator.urls")),
    path("library/", include('library.urls')),
    path("documentation/", include('documentation.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)