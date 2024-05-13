from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from rest_framework.utils import json
from django.contrib.auth.models import User

class GoogleView(APIView):
    """
    API endpoint for Google OAuth 2.0 authentication.
    This view allows users to authenticate via Google OAuth 2.0 and generates
    JWT tokens for authenticated users.
    """

    def post(self, request):
        """
        Handle a POST request to authenticate with a Google access token.
        This method validates a Google access token, creates a new user if one
        with the same email does not exist, and generates JWT tokens for the user.
        """
        payload = {'access_token': request.data.get("accessToken")}
        request_ = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(request_.text)

        if 'error' in data:
            content = {'message': 'Wrong Google token / This Google token is already expired.'}
            return Response(content)

        # Check if the user exists in the database
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            # If the user does not exist, create a new user
            user = User.objects.create_user(
                email=data['email'],
                username=data['email'],  # Set username as email
                password=make_password(BaseUserManager().make_random_password())
            )

        # Generate JWT tokens for the user
        token = RefreshToken.for_user(user)

        # Return the access token and refresh token in the response
        response = {
            'access_token': str(token.access_token),
            'refresh_token': str(token)
        }
        return Response(response)
