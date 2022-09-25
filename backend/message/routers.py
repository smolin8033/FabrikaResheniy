from rest_framework.routers import DefaultRouter

from .viewsets import MessageViewSet

router = DefaultRouter()
router.register("messages", MessageViewSet, basename="messages")
