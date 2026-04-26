from django.contrib.auth.views import LoginView
from library.forms import CustomLoginForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomLoginForm