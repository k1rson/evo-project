from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.views import View

from .mixins import RedirectAuthenticatedUserMixin

class AuthLoginPageView(RedirectAuthenticatedUserMixin, View):
    template_name = 'authentication_app/auth.html'

    def get(self, request):
        return render(request, template_name=self.template_name)
    
class AuthRegistrPageView(RedirectAuthenticatedUserMixin, View):
    template_name = 'authentication_app/registr.html'

    def get(self, request):
        return render(request, template_name=self.template_name)
    
class ResetPasswordPageView(RedirectAuthenticatedUserMixin, View):
    template_name = 'authentication_app/reset_password.html'

    def get(self, request): 
        return render(request, template_name=self.template_name)
    
class LogoutUserView(View):
    def get(self, request): 
        logout(request)

        return redirect('auth_page')