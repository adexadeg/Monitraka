from msilib.schema import ReserveCost
from urllib import response
from rest_framework.exceptions import AuthenticationFailed
#from rest_framework.views import APIView
from users.serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework import status
import uuid
from rest_framework import generics
from .serializers import LogSerializer
import jwt, datetime
#from django.contrib.auth.models import BaseUserManager


# Create your views here.
class RegisterView(generics.GenericAPIView): #APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        #serializer.is_valid(raise_exception=True)
        #serializer.save()
        #return Response(serializer.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                'RequestId': str(uuid.uuid4()),
                'Message': 'User created successfully',

                'User': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'Errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView): #APIView):
    serializer_class = LogSerializer
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
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': "Bye, Don't forget to check back again"
        }
        return response





