from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication, status

from django.db.models import Q

from apps.authentication_app.models import CustomUser
from apps.chat_app.models import ChatRoomModel, UserChatRoomModel, ChatRoomInvitationModel

from constants import error_messages 
from .serializer import ChatRoomSerializer, ChatRoomActionsSerializer, SearchTargetUserSerializer, InvitationChatRoomSerializer, EmployeeSerializer

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

class InvitationChatRoomsAPI(APIView):
    """Получение всех чатов, в которых приглашают текущего пользователя"""
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        current_user = request.user

        invitations_chat_rooms = ChatRoomInvitationModel.objects.filter(invited_user=current_user.id)
        serializer = InvitationChatRoomSerializer(invitations_chat_rooms, many=True)
        if not serializer.data:
            return Response(data={
                'success': False,
                'invitations_chat_rooms': None
            })

        return Response(data={
            'success': True, 
            'invitations_chat_rooms': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        room_id = request.data.get('room_id', None)
        action = request.data.get('action', None)
        current_user = request.user

        if not all((room_id, action)):
            return Response(data={
                'success': False,
                'err_msg': 'room_id or action not provided'
            }, status=status.HTTP_200_OK)
        
        try:
            room = ChatRoomModel.objects.get(pk=room_id)
            if action == 'accept':
                UserChatRoomModel.objects.create(room_id=room, user_id=current_user)
                ChatRoomInvitationModel.objects.filter(room=room).delete()
                
                return Response(data={
                    'success': True, 
                    'data': 'accept'
                })
            else:
                ChatRoomInvitationModel.objects.filter(room=room).delete()
                return Response(data={
                    'success': True, 
                    'data': 'discard'
                })
        except ChatRoomModel.DoesNotExist:
            return Response(data={
                'success': False,
                'err_msg': 'not room'
            }, status=status.HTTP_200_OK)
        
class ChatRoomActionsAPI(APIView):
    """API для выполнения действий с чатами (добавление, удаление, обновление и т.д.)"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request): 
        serializer = ChatRoomActionsSerializer(data={
            'room_owner': request.user.id, 
            'room_name': request.data.get('room_name', None), 
            'room_avatar': request.data.get('room_avatar', None),
            'invited_users_ids': request.data.get('invited_users_ids', None)
        })

        if not serializer.is_valid():
            return Response(data={
                'success': False,
                'err_msg': serializer.errors
            }, status=status.HTTP_200_OK)
        
        serializer.save()
        return Response(data={
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
    
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
        queryset = CustomUser.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query)).exclude(id=request.user.id)
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
    
class EmployeeAPI(APIView):
    """Получение сотрудников"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request): 
        employees = CustomUser.objects.all().exclude(id=request.user.id)

        serializer = EmployeeSerializer(employees, many=True)
        if not serializer.data:
            return Response(data={
                'success': False, 
                'err_msg': error_messages.ERROR_CHAT_EMPLOYEES_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        return Response(data={
            'success': True, 
            'employees': serializer.data
        }, status=status.HTTP_200_OK)