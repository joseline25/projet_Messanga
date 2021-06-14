from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from ..models import *
from ..serializers import  OrderSerializer, ThemeSerializer, ShopSerializer, UserProductSerializer, UserSerializer, UserSerializerWithToken, WithdrawSerializer, ShippingAddressSerializer

from rest_framework_simplejwt.serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status

    #, routers, serializers, viewsets

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v # data["username"] = serializer.username, etc.. comming from UserSerializerWithToken
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/create/',
        '/api/products/upload/',
        '/api/products/<id>/reviews/',
        '/api/products/top/',
        '/api/products/<id>/',
        '/api/products/delete/<id>/',
        '/api/products/update/<id>/',
    ]
    return Response(routes)


# Users



# Get all the users of the database


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def getUsers(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)



#Regiter a new user in the database

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': "User with this email alredy exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)



# edit the profile of a user

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    data = request.data

    user.first_name = data['name']
    user.email = data['email']
    user.username = data['email']

    if(data['password']) != '':
        user.password = make_password(data['password'])

    user.save()
    
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

# Get the profile of a user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)



# Delete the profile of a user

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request, pk):
    try:
        user = User.objects.get(_id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def createWithdraw(request):
    data = request.data
    if data['amount'] >= 500:
        try:
            withdraw = Withdraw.objects.create(
                user=request.user,
                amount=data['amount'],
                number=data['number']
            )

            serializer = WithdrawSerializer(withdraw, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': "Provide a good number."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Provide a good amount.'}, status=status.HTTP_400_BAD_REQUEST)




# Shops

# Get all the shops of a database

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def getShops(request):
    if request.method == 'GET':

        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data

        if request.method == 'POST':
            serializer = ShopSerializer(data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Add a shop in the database

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addShop(request):

    data = request.data

    try:
        shop = Shop.objects.create(
            user=request.user,
            name=data['name'],
            facebookPixel=data['facebookPixel'],
            instaPixel=data['instaPixel']
        )

        serializer = ShopSerializer(shop, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': "You are not allow to create a shop."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)



# Edit a shop's details in the database

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editShop(request, pk):
    data = request.data
    try:
        shop = Shop.objects.get(_id=pk)
    except Shop.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ShopSerializer(shop, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Delete a shop

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteShop(request, pk):
    try:
        shop = Shop.objects.get(_id=pk)
    except Shop.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# Shipping address

# Get all the shipping addresses of the database

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def getShippingAddresses(request):
    if request.method == 'GET':

        shippingAddresses = ShippingAddress.objects.all()
        serializer = ShopSerializer(shippingAddresses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data

        if request.method == 'POST':
            serializer = ShippingAddressSerializer(data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get all the shipping address of a product

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def getShippingAddresses(request):
    shippingAddresses = ShippingAddress.objects.all()
    serializer = ShopSerializer(shippingAddresses, many=True)
    return Response(serializer.data)

# Add a shipping address in the database

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addShippingAddress(request):

    data = request.data

    if request.method == 'POST':
        serializer = ShippingAddressSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Edit a shipping address's details in the database

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editShippingAddress(request, pk):
    data = request.data
    try:
        shippingAddress = ShippingAddress.objects.get(_id=pk)
    except ShippingAddress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ShippingAddressSerializer(shippingAddress, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Delete a shipping address

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteShippingAddress(request, pk):
    try:
        shippingAddress = ShippingAddress.objects.get(_id=pk)
    except ShippingAddress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        shippingAddress.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# Themes

# Get all the themes of the database

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getThemes(request):
    themes = Theme.objects.all()
    serializer = ThemeSerializer(themes, many=True)
    return Response(serializer.data)


# Add a theme in the database

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addTheme(request):
    data = request.data

    if request.method == 'POST':
        serializer = ThemeSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Edit an theme's details in the database

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editTheme(request, pk):
    data = request.data
    try:
        theme = Theme.objects.get(_id=pk)
    except Theme.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ThemeSerializer(theme, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete a theme

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTheme(request, pk):
    try:
        theme = Theme.objects.get(_id=pk)
    except Theme.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        theme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







# Withdraws

# Get all the withdraws of a database

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getWithdraws(request):
    withdraws = Withdraw.objects.all()
    serializer = WithdrawSerializer(withdraws, many=True)
    return Response(serializer.data)



# Add a withdraw in the database

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addWithdraw(request):

    data = request.data

    if request.method == 'POST':
        serializer = WithdrawSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Edit an withdraw's details in the database

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editWithdraw(request, pk):
    data = request.data
    try:
        withdraw = Withdraw.objects.get(_id=pk)
    except Withdraw.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = WithdrawSerializer(withdraw, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Delete a withdraw

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteWithdraw(request, pk):
    try:
        withdraw = Withdraw.objects.get(_id=pk)
    except Withdraw.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        withdraw.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Get all the withdraws of a user

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserWithdraws(request):
    withdraws = Withdraw.objects.filter(user=request.user)
    serializer = WithdrawSerializer(withdraws, many=False)
    return Response(serializer.data)






#Get all the products of a user

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProducts(request):
    user = request.user
    products = Product.objects.filter(user=user)
    serializer = UserProductSerializer(products, many=True)
    return Response(serializer.data)


#Get the info of a shop of a specific user

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getShopInfos(request):
    shop = Shop.objects.get(user=request.user)
    serializer = ShopSerializer(shop, many=False)
    return Response(serializer.data)


#Get all the shops of a specific user

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getShopsUser(request):
    shop = Shop.objects.filter(user=request.user)
    serializer = ShopSerializer(shop, many=False)
    return Response(serializer.data)