from rest_framework import viewsets

from notifications.models import Subscription
from notifications.serializers import SubscriptionSerializer


class SubscriptionView(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.filter(id=0)
