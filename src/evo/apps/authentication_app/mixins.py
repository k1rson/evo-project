from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class RedirectAuthenticatedUserMixin:
    """
    Mixin, который перенаправляет аутентифицированных пользователей на домашнюю страницу.
    """
    redirect_authenticated_user = True  
    home_page_url = reverse_lazy('home_page')  

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and request.user.is_authenticated:
            return self.handle_authenticated_user(request=request)

        return super().dispatch(request, *args, **kwargs)
        
    def handle_authenticated_user(self, request): 
        return HttpResponseRedirect(self.home_page_url)
    
class RedirectNoneAuthenticatedUserMixin:
    """
    Mixin, который перенаправляет неаутентифицированных пользователей на страницу авторизации.
    """
    redirect_none_authenticated_user = True  
    auth_page_url = reverse_lazy('auth_page')  

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_none_authenticated_user and not request.user.is_authenticated:
            return self.handle_none_authenticated_user(request=request)

        return super().dispatch(request, *args, **kwargs)
        
    def handle_none_authenticated_user(self, request): 
        return HttpResponseRedirect(self.auth_page_url)