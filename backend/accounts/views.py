from rest_framework import generics, permissions
from .serializers import UserSerializer


class CurrentUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self): # type: ignore
        return self.request.user
