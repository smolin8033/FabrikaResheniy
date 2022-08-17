from rest_framework.routers import DefaultRouter

from .viewsets import MailingViewSet

router = DefaultRouter()
router.register("mailings", MailingViewSet, basename='Mailings')
