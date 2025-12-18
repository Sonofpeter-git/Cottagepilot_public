from rest_framework import viewsets, status, permissions, generics, status
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.db.models import Count, Q
from django.utils import timezone
from django.http import HttpResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.core.mail import send_mail

from datetime import timedelta

from .models import CustomUser
from .serializers import (
    UserSerializer, PasswordChangeSerializer, LoginSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer
)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AccountViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['username']
    ordering = ['-username']

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'false',
                'errors': serializer.errors
            }, status=status.HTTP_200_OK)
        
        user = request.user        
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'status': 'false',
                'errors': {'old_password': ['Wrong old password.']}}, status=status.HTTP_200_OK)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'status': 'true', 'message':'New password set.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get', 'post'], url_path='me')
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response({'status': 'success', 'results': serializer.data}, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'success', 'results': serializer.data}, status=status.HTTP_200_OK)



    @action(detail=False, methods=['get'], url_path='fetchCottageUsers')
    def fetchCottageUsers(self, request):
        if request.method == 'GET':
            if request.user.access_to_cottage:
                cottageUsers = CustomUser.objects.filter(access_to_cottage = request.user.access_to_cottage).values('id', 'username', 'user_color')

                return Response({'status': 'success', 'results': cottageUsers}, status=status.HTTP_200_OK)
            
            else:
                return Response({'status': 'failed', 'results': {}}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    from .serializers import SignupSerializer
    serializer = SignupSerializer(data=request.data)
    
    if serializer.is_valid():
        newUser = serializer.save(password=serializer.validated_data['password1'])
        newUser.is_active = True
        newUser.save()
        token, created = Token.objects.get_or_create(user=newUser)
        user_serializer = UserSerializer(newUser)
        return Response({
            'token': token.key,
            'created': created,
            'redirect': '/add-or-create-cottage/',
            'cottageInstanceActive' : 'false',
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
            'token': "no",
            'created': "no",
            'user': None,
            'redirect': '/add-or-create-cottage/',
            'cottageInstanceActive' : 'false',
            'message': serializer.errors
        }, status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data,
                                     context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        #decide does user have cottage active
        if user.access_to_cottage:
            cottageInstanceActive = 'true'  
        else:
            cottageInstanceActive = 'false'
        return Response({
            'token': token.key,
            'created': created,
            'user': user_serializer.data,
            'cottageInstanceActive' : cottageInstanceActive,
        }, status=status.HTTP_200_OK)
    
    
    def self_post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data,
                                    context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        #decide does user have cottage active
        if user.access_to_cottage:
            cottageInstanceActive = 'true'
        else:
            cottageInstanceActive = 'false'
        return Response({
            'token': token.key,
            'created': created,
            'user': user_serializer.data,
            'cottageInstanceActive' : cottageInstanceActive,
            'status' : 'success'
        }, status=status.HTTP_200_OK)

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)}, status=201)




class RequestPasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email'].lower()

        try:
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = f"{settings.FRONTEND_URL}reset-password/{uid}/{token}/"

            send_mail(
                subject="Reset your password",
                message=f"Click the link to reset your password: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        except CustomUser.DoesNotExist:
            pass  # For security, don't reveal whether user exists

        return Response({'message': 'If that email exists, a reset link was sent.'})



class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid or expired token'}, status=400)
            return Response({'message': 'Token valid', 'uid': uidb64, 'token': token})
        except Exception:
            return Response({'error': 'Invalid reset link'}, status=400)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'false',
                'errors': serializer.errors
            }, status=200)

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = CustomUser.objects.get(pk=uid)
            if not PasswordResetTokenGenerator().check_token(user, serializer.validated_data['token']):
                return Response({'error': 'Invalid or expired token',
                                 'status':'false'}, status=400)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password reset successful',
                             'status':'true'})
        except Exception:
            return Response({'error': 'Something went wrong',
                             'status':'false'}, status=400)
