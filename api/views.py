from rest_framework.generics import ListAPIView, CreateAPIView
from . serializers import ListCustomUserSerializer, CustomUserSerializer, CustomTokenObtainPairSerializer, ListItemsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from api.models import CustomUser, Item
from . pagination import CustomPagination


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()


class ListItemApiView(ListAPIView):
    serializer_class = ListItemsSerializer
    queryset = Item.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title', 'brand']
    ordering_fields = ['price']
    search_fields = ['title', 'brand']

    def get_queryset(self):
        queryset = Item.objects.all()
        # Filter by price greater than
        price = self.request.query_params.get('price', None)
        if price is not None:
            queryset = queryset.filter(price__gte=price)
        return queryset


