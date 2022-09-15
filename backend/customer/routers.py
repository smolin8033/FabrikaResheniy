from rest_framework.routers import DefaultRouter

from .viewsets import CustomerViewSet

router = DefaultRouter()
router.register("customers", CustomerViewSet, basename="customers")
