"""Contains menu views"""
from django.contrib.auth.models import PermissionsMixin
from django.db.models.lookups import Exact
from django.shortcuts import render, get_object_or_404
from django.utils.dateformat import DateFormat
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from yaml import serialize

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
            'item_upd_usr_email': menu_item.item_upd_usr_email,
            # Format datetime field as string in a readable format (ISO 8601 or custom format)
            'item_last_upd_ts': DateFormat(menu_item.item_last_upd_ts).format('Y-m-d H:i:s') if menu_item.item_last_upd_ts else None,

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


class MenuItemsPatchView(APIView):
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
    def patch(self, request, item_id):
        """This view updates item associated with the item_id"""

        try:
            if not (request.user.is_admin or request.user.is_superuser):
                return Response(
                    {"Error": "Only admin/super user's can update menu items"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            item = MenuItem.objects.get(item_id=item_id)

            mutable_data = request.data.copy()
            mutable_data['item_upd_usr_id'] = request.user.id
            mutable_data['item_upd_usr_email'] = request.user.email
            serializer = MenuItemSerializer(item, data=mutable_data, partial=True)

            # request.data['item_upd_usr_id'] = request.user.id
            # request.data['item_upd_usr_email'] = request.user.email
            # serializer = MenuItemSerializer(item, data=request.data, partial=True)

            if serializer.is_valid():
                updated_item = serializer.update(item, serializer.validated_data)
                return Response(MenuItemSerializer(updated_item).data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist as ODNE:
            return Response({
                "error": f"Item with id:{item_id} does not exist",
                "Details": f"{type(ODNE).__name__}, {ODNE}",
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "error": "An unexpected error occurred",
                "Details": f"{type(e).__name__}, {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


