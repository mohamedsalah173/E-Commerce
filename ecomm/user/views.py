from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import Registration, UserBase, LoginSerializer, UserDeleteSerializer, UserUpdateSerializer, UserListSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class RegisterView(generics.GenericAPIView):
    serializer_class = Registration

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


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:

            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserBase.objects.filter(id=self.request.user.id)


class UserDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            user = UserBase.objects.get(pk=pk)
            serializer = UserDeleteSerializer(user)
            user.delete()
            return Response({"message": "User deleted successfully.", "data": serializer.data}, status=status.HTTP_204_NO_CONTENT)
        except UserBase.DoesNotExist:
            return Response({"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)


class UserListView(APIView):

    def get(self, request, pk):
        permission_classes = [IsAuthenticated]
        user = UserBase.objects.filter(id=pk).first()

        if user:
            serializer = UserListSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
