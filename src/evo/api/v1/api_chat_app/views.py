from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication, status, parsers

from django.db.models import Q

from apps.authentication_app.models import CustomUser
from apps.chat_app.models import ChatRoomModel, UserChatRoomModel

from constants import error_messages 
from .serializer import ChatRoomSerializer, ChatRoomActionsSerializer, SearchTargetUserSerializer

class SharedChatRoomsAPI(APIView):
    """Получение всех общих чатов (только тех, в которых не находится пользователь)"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        current_user = request.user

        excluded_rooms_ids = UserChatRoomModel.objects.filter(user_id=current_user.id).values_list('room_id', flat=True)
        shared_chat_rooms = ChatRoomModel.objects.exclude(id__in=excluded_rooms_ids)

        serializer = ChatRoomSerializer(shared_chat_rooms, many=True)
        if not serializer.data: 
            return Response(data={
                'success': False, 
                'shared_chat_rooms': None
            })

        return Response(data={
            'success': True, 
            'shared_chat_rooms': serializer.data
            }, status=status.HTTP_200_OK)
    
class UserChatRoomsAPI(APIView):
    """Получение всех пользовательских чатов (только тех, в которых находится пользователь)"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        current_user = request.user

        user_rooms_ids = UserChatRoomModel.objects.filter(user_id=current_user.id).values_list('room_id', flat=True)
        user_rooms = ChatRoomModel.objects.filter(id__in=user_rooms_ids)

        serializer = ChatRoomSerializer(user_rooms, many=True)
        if not serializer.data:
            return Response(data={
                'success': True, 
                'user_chat_rooms': None
            })

        return Response(data={
            'success': True, 
            'user_chat_rooms': serializer.data
            }, status=status.HTTP_200_OK)

class ChatRoomActionsAPI(APIView):
    """API для выполнения действий с чатами (добавление, удаление, обновление и т.д.)"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    parser_classes = [parsers.MultiPartParser]

    def post(self, request): 
        serializer = ChatRoomActionsSerializer(data={
            'room_owner': request.user.id, 
            'room_name': request.data.get('room_name', None), 
            'room_avatar': request.data.get('room_avatar', None)
        })

        if not serializer.is_valid():
            return Response(data=serializer.errors)
        
        serializer.save()
        return Response(data=serializer.data)
    
    def put(self, request):
        pass

    def delete(self, request):
        pass

class SearchTargetUserAPI(APIView):
    """Поиск пользователя, которого желают добавить в общий чат"""
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response(data={
                'success': False,
                'err_msg': error_messages.ERROR_CHAT_APP_USER_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        # добавить проверку на выборку пользователей, который запретили себя добавлять в общие чаты
        queryset = CustomUser.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query))
        serializer = SearchTargetUserSerializer(queryset, many=True)
        if not serializer.data:
            return Response(data={
                'success': False, 
                'err_msg': error_messages.ERROR_CHAT_APP_USER_NOT_FOUND
            }, status=status.HTTP_200_OK) 
        
        return Response(data={
            'success': True,
            'searched_users': serializer.data
        }, status=status.HTTP_200_OK)