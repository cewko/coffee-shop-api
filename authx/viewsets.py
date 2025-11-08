from django.contrib.auth import get_user_model, logout
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from .permissions import IsOwner
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    permission_classes = [IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logout(request)
        self.perform_destroy(instance)
        
        return Response(status=HTTP_204_NO_CONTENT)