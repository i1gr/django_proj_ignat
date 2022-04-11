from rest_framework import generics

from .models import Profile
from .serializer import ProfileSerializer


class ProfileView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            return (Profile.objects.get(email=current_user.email), )
        return None
