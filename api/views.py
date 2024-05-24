from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from . serializers import ListCustomUserSerializer, CustomUserSerializer, CustomTokenObtainPairSerializer, ListItemsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
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
    # limit the number of requests per user to 5 in 1 minute
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title', 'brand']
    ordering_fields = ['price']
    search_fields = ['title', 'brand']

    def get_queryset(self):
        queryset = Item.objects.all()
        # Filter by price greater than
        price = self.request.query_params.get('price', None)

        price_gt = queryset.filter(price__gt=10000)
        brand = queryset.filter(brand='MANDARINA DUCK')

        # return combined queryset
        return price_gt.intersection(brand)
        if price is not None:
            queryset = queryset.filter(price__gte=price)
        return queryset
    

class DetailItemApiView(RetrieveAPIView):
    serializer_class = ListItemsSerializer
    queryset = Item.objects.all()
    lookup_field = 'id'




