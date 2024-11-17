"""This is the user views"""
from logging import exception

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import UserSerializer, TokenAuthSerializer, StaffUserSerializer


class CreateUserView(generics.CreateAPIView):
    """Creates a new user in the system"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CreateStaffUserView(APIView):
    """view for create user"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=StaffUserSerializer,  # Specifies the request body schema
        responses={
            201: StaffUserSerializer,  # Specifies the response schema
            400: OpenApiResponse(description="Bad Request", response=str),  # Bad request response
            403: OpenApiResponse(description="Forbidden", response=str),  # Forbidden response
            500: OpenApiResponse(description="Internal Server Error", response=str)  # Internal server error response
        }
    )

    def post(self, request, *args, **kwargs):
        """Post method to create the staff user"""
        try:
            print(f"user:{request.user.email}")
            print(f"is_admin: {request.user.is_admin}")
            print(f"is_superuser: {request.user.is_superuser}")
            print(f"check: {not (request.user.is_admin or request.user.is_superuser)}")
            if not (request.user.is_admin or request.user.is_superuser):
                raise PermissionDenied("Only admin/super users can create staff user")
            serializer = StaffUserSerializer(data=request.data)

            if serializer.is_valid():
                staff_user = serializer.save()
                return Response(
                    {
                        "message": "Created staff user successfully",
                        "email": staff_user.email
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied as p:
            return Response(
                {
                    "detail": str(p)
                },
                status=status.HTTP_403_FORBIDDEN
            )

        except ValidationError as e:
            # Catch validation errors (e.g., invalid serializer data)
            return Response(
                {
                    "detail": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist as e:
            # Catch object-related errors (e.g., if something goes wrong during the user creation)
            return Response(
                {
                    "detail": "User creation failed: Object not found."
                },
                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch any other exceptions
            return Response(
                {
                    "detail": f"An unexpected error occurred: {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = TokenAuthSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(APIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retrieve and return the authenticated user."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

