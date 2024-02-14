from django.shortcuts import redirect

class AuthenticatedUserRedirectMixin:
    """
    Mixin, который перенаправляет аутентифицированных пользователей на домашнюю страницу.
    """
    redirect_authenticated_user = True  

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and request.user.is_authenticated:
            return self.handle_authenticated_user(request=request)

        return super().dispatch(request, *args, **kwargs)
        
    def handle_authenticated_user(self, request): 
        return redirect('home')