from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from ..models import *
from ..serializers import *

from rest_framework import status
import sys

@api_view(['POST'])
def addOrderItem(request):
    user = User.objects.filter(username=request.user.username).first()
    data = request.data

    try:
        product = Product.objects.filter(_id=data["productId"]).first()


        if not isinstance(product, Product) or product == None:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
                user=user,
                product=product,
                paymentMethod=data['paymentMethod'],
                shippingPrice=data['shippingPrice'],
                shippingAddress=data['shippingAddress'],
                totalPrice=data['totalPrice']
            )

        orderItem = OrderItem.objects.create(
            seller = product.user,
            product = product,
            order= order,
            name = user.first_name if user else "None",
            qty = data['qty'],
            price = data['totalPrice']
        )

        serializer = OrderItemSerializer(orderItem, many=False)
        return Response(serializer.data)
    except:
        return Response({'detail': "Cannot create the order"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAskedOrders(request):
    askedOrdersItems = OrderItem.objects.filter(seller=request.user)
    askedOrders = []
    for orderItem in askedOrdersItems:
        askedOrders.append(orderItem.order)
    serializer = OrderSerializer(askedOrders, many=True)
    return Response(serializer.data)


# Orders

# Get all the orders of a database

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = ShopSerializer(orders, many=True)
    return Response(serializer.data)


# Get all the orders of a user

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserOrders(request,pk):
    user = User.objects.get(_id=pk)
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=False)
    return Response(serializer.data)

# Add an order in the database

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrder(request):

    data = request.data

    if request.method == 'POST':
        serializer = OrderSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Edit an order's details in the database

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editOrder(request, pk):
    data = request.data
    try:
        order = Order.objects.get(_id=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = OrderSerializer(order, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Delete an order

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteOrder(request, pk):
    try:
        order = Order.objects.get(_id=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


