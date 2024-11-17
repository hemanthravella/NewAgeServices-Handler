"""Contains menu views"""
from django.db.models.lookups import Exact
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.core.exceptions import ObjectDoesNotExist


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






