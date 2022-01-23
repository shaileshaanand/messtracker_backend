from rest_framework import viewsets, authentication, permissions, status
from core.permissions import IsOwner
from .serializers import MessSerializer, MessCreateSerializer

from core.models import Mess


class MessViewSet(viewsets.ModelViewSet):
    queryset = Mess.objects.all()
    serializer_class = MessSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwner]
    lookup_field = "external_id"
    http_method_names = ["patch", "get", "post", "delete"]

    def get_serializer_class(self, *args, **kwargs):
        print(self.request)
        print("ACTIONNNNN", self.action == "create")
        if self.action == "create":
            return MessCreateSerializer
        return MessSerializer
