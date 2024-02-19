from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication

from apps.authentication_app.models import CustomUser
from apps.chat_app.models import ChatRoomModel

from constants import error_messages

from .serializer import ChatRoomUserSerializer

class ChatRoomAPI(APIView):
    """
        Класс, базирующийся на стандратном APIView, 
        отвечающий за обработку действий, совершаемых над общими чатами (получение чатов, создание чатов, удаление чатов, обновление и т.д.)
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        chat_rooms = ChatRoomModel.objects.all()
        serializer = ChatRoomUserSerializer(chat_rooms, many=True)

        return Response(data={
            'chat_rooms': serializer.data
        })
