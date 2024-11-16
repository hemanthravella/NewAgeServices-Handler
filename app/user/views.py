"""This is the user views"""

from django.shortcuts import render
from rest_framework import generics

from app.user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """Creates a new user in the system"""
    serializer_class = UserSerializer