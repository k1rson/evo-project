from django.shortcuts import render

from django.views import View

from .mixins import RoleBasedTemplateMixin
from ..authentication_app.mixins import RedirectNoneAuthenticatedUserMixin

class HomePageView(RedirectNoneAuthenticatedUserMixin, 
                   RoleBasedTemplateMixin, 
                   View):
    
    def get(self, request):
        template_name = self.get_template_name(request)
        
        return render(request, template_name=template_name)
    
class ChatPageView(RedirectNoneAuthenticatedUserMixin, 
                   View):
    
    def get(self, request):
        template_name = 'main_app/chat_app.html'