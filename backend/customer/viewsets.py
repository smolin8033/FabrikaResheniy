from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from .models import Customer
from .serializers import CustomerSerializer


@extend_schema(tags=['Клиенты'])
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
