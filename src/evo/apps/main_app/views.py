from django.shortcuts import render

from django.views import View

from .mixins import RoleBasedTemplateMixin

class HomePageView(RoleBasedTemplateMixin, View): 
    def get(self, request):
        template_name = self.get_template_name(request)
        
        return render(request, template_name=template_name)