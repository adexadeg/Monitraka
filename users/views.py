from rest_framework.exceptions import AuthenticationFailed
from users.serializers import UserSerializer,ProfileSettingsSerializer,LoginSerializer,LogoutSerializer,PasswordSettingsSerializer,ForgotPasswordSerializers,CreateNewPasswordSerializer
from rest_framework.response import Response
from .models import User
from rest_framework import status
import uuid
from rest_framework import generics, viewsets
import jwt, datetime
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

# Create your views here.
class RegisterView(generics.GenericAPIView): 
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                'RequestId': str(uuid.uuid4()),
                'Message': 'User created successfully',

                'User': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'Errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView): 
    serializer_class = LoginSerializer
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly= True)
        response.data = {
            'message': 'login successful',
            'jwt': token
        }
        return response

class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            #redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl#+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success':True,'message': 'Credentials Valid','uidb64':uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class CreateNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = CreateNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)



class UserView(generics.GenericAPIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': "Bye, Don't forget to check back again"
        }
        return response


class ProfileSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSettingsSerializer
    queryset = User.objects.all()
    #permission_classes = (IsAuthenticated,)

class PasswordSettingsView(generics.UpdateAPIView): 
    serializer_class = PasswordSettingsSerializer
    queryset = User.objects.all()
    #permission_classes = (IsAuthenticated,)
    