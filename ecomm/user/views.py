from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import Registration, UserBase, LoginSerializer, UserUpdateSerializer
from rest_framework.views import APIView


class RegisterView(generics.GenericAPIView):
    serializer_class = Registration
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # create user
        user = serializer.save()

        # activate user
        user.is_active = True
        user.save()

        # generate tokens
        refresh = RefreshToken.for_user(user)

        # return response
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'user_id': user.id,
            'email': user.email,
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserUpdateView(generics.UpdateAPIView):
    queryset = UserBase.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if not instance.is_active:
            return Response({'detail': 'User is inactive', 'code': 'user_inactive'}, status=status.HTTP_403_FORBIDDEN)

        serializer.save()
        return Response(serializer.data)
