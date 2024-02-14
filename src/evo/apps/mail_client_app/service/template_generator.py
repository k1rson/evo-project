import os

from jinja2 import Environment, FileSystemLoader

class TemplateGenerator:
    def __init__(self, template_name: str):
        self.template_name = template_name
        self.template = self._get_template()

    def _get_template(self): 
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, '..'))
        template_dir = os.path.join(project_dir, 'templates_to_render') 

        env = Environment(loader=FileSystemLoader(template_dir))

        try:
            template = env.get_template(self.template_name)
        except Exception as e:
            # LOGGING exception
            return None

        if template is None:
            return None
            # LOGGINS exception
        
        return template

    def generate_html_content(self, context=None):
        if context is None:
            context = {}

        html_content = self.template.render(context)
        return html_content