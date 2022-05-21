from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta

from .serializers import (
                            AccountSerializer, LoginSerializer
                )
from .models import Account
from .renderers import UserJSONRenderer
from fly_image_python.settings import JWT_TOKEN_LIFETIME_MIN
from controll_pkg.models import ObservationObjectChronology, Fly

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AccountSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        account = request.data.get('account', {})
        user = {
            'email': account.pop('email', None),
            'password': account.pop('password', None),
            'username': account.get('first_name', '')+' '+account.get('last_name','')
        }
        account['user'] = user
        serializer = self.serializer_class(data=account)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        result = serializer.data
        result.update(result.pop('user'))

        return Response(result, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('account', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        result = {'user': {
                    'token': user.token,
                    'creation':int(datetime.now().timestamp()*1000),
                    'expiration':int((datetime.now() + timedelta(minutes=JWT_TOKEN_LIFETIME_MIN)).timestamp()*1000)
                    } 
                }
        return Response(result, status=status.HTTP_200_OK)

class AccountView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, request):
        account = Account.objects.get(user=request.user)
        serializer = self.serializer_class(account)
        result = serializer.data
        result.update(result.pop('user'))
        result.pop('token')
        
        fly_count = Fly.objects.filter(author__id=account.id).count()
        object_count = ObservationObjectChronology.objects.filter(author__id=account.id).count()        
        result['fly_count'] = fly_count
        result['object_count'] = object_count
        result['at_create'] = request.user.created_at        
        
        return Response({'user':{**result}}, status=status.HTTP_200_OK)
