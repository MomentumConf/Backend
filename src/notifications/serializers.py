from rest_framework import serializers

from notifications.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ["auth"]

    def create(self, validated_data):
        subscription = Subscription.objects.get_or_create(
            auth=validated_data["details"]["keys"]["auth"], details=validated_data["details"]
        )

        return subscription[0]
