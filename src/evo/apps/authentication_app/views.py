from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.views import View

from .mixins import RedirectAuthenticatedUserMixin

class AuthLoginPageView(RedirectAuthenticatedUserMixin, View):
    template_name = 'authentication_app/auth.html'

    def get(self, request):
        return render(request, template_name=self.template_name)
    
class ResetPasswordPageView(RedirectAuthenticatedUserMixin, View):
    template_name = 'authentication_app/reset_password.html'

    def get(self, request): 
        return render(request, template_name=self.template_name)
    
class LogoutUserView(View):
    def get(self, request):
        response = redirect('auth_page')
        response.delete_cookie('token')
        response.delete_cookie('sessionid')

        logout(request)

        return response