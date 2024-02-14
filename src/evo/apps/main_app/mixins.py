
class RoleBasedTemplateMixin:
    def get_template_name(self, request): 
        role = request.user.role.lower()
        template_name = f'main_app/{role}_dashboard.html'

        return template_name