from rest_framework.response import Response

from apps.mail_client_app.smtp_utils.smtp_client import SMTPServer
from apps.mail_client_app.service.template_generator import TemplateGenerator

def reset_password_user(user) -> bool:
    """
        Отвечает за отправку одноразового кода (OTP) пользователю на Email

        :param user: Объект типа CustomUser
        :return: Объект типа bool() -> сигнализирует об успешной/ошибочной отправке кода для смены пароля
    """
    smtp_server = SMTPServer()
    template_generator = TemplateGenerator('reset_password_email.html')

    context = {
        'username': user.username, 
        'new_password': user_data['new_password']
    }

    html_content = template_generator.generate_html_content(context)
    send_status = smtp_server.send_message(f'Доброго времени суток, {user_data["username"]}!. Восстановление доступа к учетной записи', '', user_data['email'], html_content)

    if not send_status: 
        return False
    
    return True 
    
def create_response(status, message=None) -> Response:
    """
        Создает объект Response с заданным статусом и сообщением.

        :param status: Статус сформированного ответа -> успешно/ошибка
        :param message: Сообщение, описывающее ошибку, в случае, если ответ сформирован неудачно

        :return: Объект типа Response
    """
    if status == 'error':
        data = {
            'status': 'error',
            'err_msg': message 
        }
    else:
        data = {
            'status': 'success'
        }

    return Response(data=data)