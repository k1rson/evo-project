from django.views import View
from django.shortcuts import render

from ..authentication_app.mixins import RedirectNoneAuthenticatedUserMixin

class ChatPageView(RedirectNoneAuthenticatedUserMixin, 
                   View):
    template_name = 'chat_app/chat_app.html'

    def get(self, request): 
        return render(request, self.template_name)