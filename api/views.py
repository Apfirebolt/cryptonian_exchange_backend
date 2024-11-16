from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.views import APIView
from . serializers import ListCustomUserSerializer, CustomUserSerializer, CustomTokenObtainPairSerializer, CurrencySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import extend_schema
from users.models import CustomUser, AuditLog
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import Currency
from rest_framework.views import APIView
from . permissions import IsOwner, IsSuperUser


class PasswordlessLoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        user = self.authenticate(username)

        if user is None:
            return Response({'error': 'Invalid username'}, status=401)

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)
        email = user.email

        return Response({'refresh': refresh, 'access': access, 'email': email})

    def authenticate(self, username):
        # Use your custom backend logic here (defined in step 1)
        return EmailLoginBackend().authenticate(self.request, username)

class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []


class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()
    # permission_classes = [IsAuthenticated, IsSuperUser]
    permission_classes = []


class RetrieveUpdateDestroyCustomUserApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserDataSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserDataSerializer(user, data=request.data, partial=True)
        # if exception is raised then return 400 with a detail message
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ListCreateCurrencyApiView(ListCreateAPIView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    permission_classes = [IsAuthenticated]
    

class RetrieveUpdateDestroyCurrencyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        currency = self.get_object()
        serializer = CurrencySerializer(currency)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def delete(self, request, *args, **kwargs):
        currency = self.get_object()
        currency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


    

