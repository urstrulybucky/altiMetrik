# from django.shortcuts import render

# # Create your views here.
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .serializers import UserSerializer
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.decorators import api_view,permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# # @api_view(['POST'])
# # def register_user(request):
# #     if request.method == 'POST':
# #         serializer = UserSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # @api_view(['POST'])
# # def login_user(request):
# #     if request.method == 'POST':
# #         # Your login logic here
# #         return Response("Login successful", status=status.HTTP_200_OK)
    
# # @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # def get_user_name(request):
# #     if request.user.is_authenticated:
       
# #         # Your view logic for authenticated users
# #         return Response({'message': 'Authenticated user can access this endpoint', 'username': request.headers})
# #     else:
# #         # Your logic for handling unauthenticated users (optional)
# #         return Response({'message': 'Authentication credentials were not provided.'}, status=401)


# from django.test import TestCase

# # Create your tests here.
