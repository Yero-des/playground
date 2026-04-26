from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from library.views import CustomLoginView
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    # path('', RedirectView.as_view(pattern_name='tests')),
    # path('', RedirectView.as_view(pattern_name='tasks:list_tasks')),
    # path('tests/', TemplateView.as_view(template_name='tests.html'), name='tests'),
    path('', RedirectView.as_view(pattern_name='tests:index')),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    # path('logout/', LogoutView.as_view(next_page="registration/logout.html"), name="logout"), # Personalized next_page en caso se requiera
    path('admin/', admin.site.urls),
    path('messages/', include("apps.quotes.urls")),
    path('landings/', include("apps.landing.urls")),
    path('calculator/', include("apps.calculator.urls")),
    path("library/", include('library.urls')),
    path("documentation/", include('apps.documentation.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('tests/', include('apps.tests.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)