from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *





class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # Creation of custom fields for user without update the django user model
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', '_id', 'isAdmin']  # Add custom fields

    # Setting the custom value for _id field to be id comming from django user (obj)
    def get__id(self, obj):
        return obj.id

    # Setting the custom value for name field to be id comming from django user (obj)
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name

    # Setting the custom value for isAdmin field to be id comming from django user (obj)
    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', '_id', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)  # Return a new token
        return str(token.access_token)


class UserProductSerializer(serializers.ModelSerializer):
    numOrders = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['_id', 'name', 'price', 'numOrders']

    def get_numOrders(self, obj):
        numOrders = Order.objects.filter(product=obj).count()
        return numOrders


class OrderSerializer(serializers.ModelSerializer):
    productName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['_id', 'productName', 'totalPrice', 'isDelivered', 'isPaid']

    def get_productName(self, obj):
        return obj.product.name


"""
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields= "__all__"
"""


class ProductSerializer(serializers.ModelSerializer):

    serializers.ImageField(use_url=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'desc', 'price', 'countStock']

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = "__all__"


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class VariantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variants
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
