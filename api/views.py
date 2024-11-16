from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from . serializers import ListCustomUserSerializer, CustomUserSerializer, CustomTokenObtainPairSerializer, CurrencySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import extend_schema
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import Currency
from rest_framework.views import APIView


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
        serializer = ListCustomUserSerializer(user)
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
    


    

