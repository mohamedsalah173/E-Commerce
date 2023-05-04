from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import Registration, UserBase, LoginSerializer
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


# class LoginView(generics.GenericAPIView):
#     serializer_class = UserBase

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(request, email=email, password=password)

#         if user:
#             login(request, user)
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh)
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 'error': 'Invalid email/password'
#             }, status=status.HTTP_401_UNAUTHORIZED)

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
