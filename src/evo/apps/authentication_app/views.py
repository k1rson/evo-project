from django.shortcuts import render

from django.views import View

from .mixins import AuthenticatedUserRedirectMixin

class AuthLoginPageView(AuthenticatedUserRedirectMixin, View):
    template_name = 'authentication_app/auth.html'

    def get(self, request):
        print(request.user)

        return render(request, template_name=self.template_name)
    
class AuthRegistrPageView(AuthenticatedUserRedirectMixin, View):
    template_name = 'authentication_app/registr.html'

    def get(self, request):
        return render(request, template_name=self.template_name)
    
class ResetPasswordPageView(AuthenticatedUserRedirectMixin, View):
    template_name = 'authentication_app/reset_password.html'

    def get(self, request): 
        return render(request, template_name=self.template_name)