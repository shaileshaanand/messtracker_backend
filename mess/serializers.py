from rest_framework import serializers
from core.models import Mess, User
from user.serializers import UserSerializer


class MessSerializer(serializers.ModelSerializer):

    owner = UserSerializer()

    class Meta:
        model = Mess
        fields = ["external_id", "name", "owner"]
        read_only_fields = ["external_id"]


class MessCreateSerializer(MessSerializer):
    owner = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="external_id"
    )

    class Meta:
        model = Mess
        fields = ["name", "owner"]
