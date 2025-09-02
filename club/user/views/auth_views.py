# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.hashers import check_password
# from ..models import User
# from ..serializers import RegisterSerializer, LoginSerializer, UserSerializer


# # -----------------------------
# # Register
# # -----------------------------
# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # -----------------------------
# # Login
# # -----------------------------
# class LoginAPIView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']

#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

#             if check_password(password, user.password):
#                 return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
