"""Contains menu views"""
from django.contrib.auth.models import PermissionsMixin
from django.db.models.lookups import Exact
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from drf_spectacular.utils import extend_schema


class MenuItemDetailView(APIView):
    """View for fetching a menu item by its ID"""

    def get(self, request, item_id):
        # Fetch the MenuItem by item_id
        menu_item = get_object_or_404(MenuItem, item_id=item_id)

        # Return the item details
        return Response({
            'item_name': menu_item.item_name,
            'item_type': menu_item.item_type,
            'menu_type': menu_item.menu_type,
            'item_cost': str(menu_item.item_cost),  # Converting decimal to string for consistent formatting
            'item_description': menu_item.item_description,
            'is_allergic': menu_item.is_allergic,
            'is_vegetarian': menu_item.is_vegetarian,
            'is_available': menu_item.is_available,
        })


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
            if not (request.user.is_admin or request.user.is_superuser):
                return Response(
                    {"Error": "Only admin/super user's can create menu items"},
                    status = status.HTTP_403_FORBIDDEN,
            )

            serializer = MenuItemSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(item_upd_usr_id=request.user,item_upd_usr_email=request.user.email)
                return Response(serializer.data,status=HTTP_201_CREATED)

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







