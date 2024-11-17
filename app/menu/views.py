"""Contains menu views"""
from django.contrib.auth.models import PermissionsMixin
from django.db.models.lookups import Exact
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from drf_spectacular.utils import extend_schema


class MenuItemsDetailsView(APIView):
    """Gives details of the items"""

    def get(self,request, id):
        expand = request.query_params.get('expand',None)
        try:
            item = MenuItem.objects.get(item_id='id')
            if expand == 'all':
                serializer = MenuItemSerializer(item)
            else:
                serializer = MenuItemSerializer(item, fields=['item_name', 'is_allergic', 'is_vegetarian', 'is_available', 'item_cost'])

            return Response(serializer.data,status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': f'Item not found for id{id}'},status=status.HTTP_404_NOT_FOUND)

class MenuItemsView(APIView):
    """This view helps in creating and updating the menu item and deleting"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=MenuItemSerializer,  # Specifies the request body schema
        responses={
            201: MenuItemSerializer,  # Specifies the response schema
            400: 'Bad Request',
            403: 'Forbidden',
            500: 'Internal Server Error'
        }
    )

    def post(self,request, *args, **kwargs):
        """To create menu item"""
        try:
            if not request.user.is_staff or request.user.is_admin or request.user.is_superuser:
                return Response(
                    {"Error": "Only staff memmbers can create menu items"},
                    status = status.HTTP_403_FORBIDDEN,
            )

            serializer = MenuItemSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(item_upd_usr_id=request.user,item_upd_usr_email=request.user.email)
                return Response(serializer.data,status=HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as v:
            return Response(
                {"error": "Data provided is invalid", "Details": str(v)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "error": "An unexpected error occured",
                    "Details":"str(e)"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )







