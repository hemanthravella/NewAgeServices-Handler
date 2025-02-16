from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db import transaction
from .models import Order
from .serializers import GetOrderSerializer, CreateOrderSerializer
from drf_spectacular.utils import extend_schema


class OrderDetailView(APIView):
    """view for fetching the order details by order id"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=GetOrderSerializer,  # Specifies the request body schema
        responses={
            201: GetOrderSerializer,  # Specifies the response schema
            400: 'Bad Request',
            403: 'Forbidden',
            500: 'Internal Server Error'
        }
    )
    def get(self, request, order_id: int) -> Response:
        """Get the order details of the provided id"""
        order = get_object_or_404(Order, order_id=order_id, customer_id=request.user)

        serializer = GetOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrderView(APIView):
    """View for creating the order"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CreateOrderSerializer,  # Specifies the request body schema
        responses={
            201: CreateOrderSerializer,  # Specifies the response schema
            400: 'Bad Request',
            403: 'Forbidden',
            500: 'Internal Server Error'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():  # to avoid partial order creation
                    order = serializer.save(customer_id=request.user)
                    return Response(
                        {"message": "Order created successfully!", "order_id": order.order_id},
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return Response(
                    {"error": f"An unexpected error occurred: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
