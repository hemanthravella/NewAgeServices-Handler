from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import Order
from .serializers import GetOrderSerializer


class OrderDetailView(APIView):
    """view for fetching the order details by order id"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id: int) -> Response:
        """Get the order details of the provided id"""
        order = get_object_or_404(Order, order_id=order_id, customer_id=request.user)

        serializer = GetOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)