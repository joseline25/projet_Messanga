from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Category, Product, User, Variants, Review, Tag
from ..serializers import CategorySerializer, ProductSerializer, VariantsSerializer, ReviewSerializer, TagSerializer
from rest_framework import status, viewsets, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# Products

# list of products
"""
@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

"""

@api_view(['GET', 'POST'])
def getProducts(request):
    if request.method == 'GET':

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# details on a product
@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


# add a new product

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addProduct(request):
    data = request.data

    if request.method == 'POST':
        serializer = ProductSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete a product

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(_id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# edit a product's details

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editProduct(request, pk):
    data = request.data
    try:
        product = Product.objects.get(_id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Categories


# the list of all categories

@api_view(['GET', 'POST'])
def getCategories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data

        if request.method == 'POST':
            serializer = CategorySerializer(data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# details on a category
@api_view(['GET'])
def getCategory(request, pk):
    category = Category.objects.get(_id=pk)
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)


# add a new category (optional since already implemented)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def addCategory(request):
    data = request.data

    if request.method == 'POST':
        serializer = CategorySerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete a category

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def deleteCategory(request, pk):
    try:
        category = Category.objects.get(_id=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# edit a category's details

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def editCategory(request, pk):
    data = request.data
    try:
        category = Category.objects.get(_id=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CategorySerializer(category, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Variants


# the list of all variants of a product

@api_view(['GET', 'POST'])
def getVariants(request, pk):
    if request.method == 'GET':
        # productChoosen = Product.objects.get(_id=pk)
        variants = Variants.objects.filter(product=pk)
        serializer = VariantsSerializer(variants, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data

        if request.method == 'POST':
            serializer = VariantsSerializer(data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# add a new variant


"""def addVariant(request):
    data = request.data

    if request.method == 'POST':
        serializer = VariantsSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addVariant(request):
    data = request.data

    try:
        variant = Variants.objects.create(
            user=request.user,
            name=data['name'],
            options=data['options'],
            product=data['product']
        )

        serializer = VariantsSerializer(variant, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': "You are not allow to create a variant."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# delete a variant

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteVariant(request, pk):
    try:
        variant = Variants.objects.get(_id=pk)
    except Variants.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        variant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# edit a variant

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editVariant(request, pk):
    data = request.data
    try:
        variant = Variants.objects.get(_id=pk)
    except Variants.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = VariantsSerializer(variant, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Reviews


# the list of all the reviews of a product

@api_view(['GET'])
def getReviews(request, pk):
    reviews = Review.objects.filter(product=pk)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


# add a new review

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addReview(request):
    data = request.data

    if request.method == 'POST':
        serializer = ReviewSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete a review

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteReview(request, pk):
    try:
        review = Review.objects.get(_id=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# edit a review

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editReview(request, pk):
    data = request.data
    try:
        review = Review.objects.get(_id=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Tags


# the list of all tags related to a product

@api_view(['GET', 'POST'])
def getTags(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    elif request.method =='POST':
        data = request.data

        if request.method == 'POST':
            serializer = TagSerializer(data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# add a new tag

""" I keep getting the error Field '_id' expected a number but got 'addTag' for all my Post methods"""

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def addTag(request):
    data = request.data
    tags = Tag.objects.all()
    lastTag=tags[-1]

    if request.method == 'POST':
        serializer = TagSerializer(data)
        if serializer.is_valid():
            serializer._id = lastTag._id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete a tag

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def deleteTag(request, pk):
    try:
        tag = Tag.objects.get(_id=pk)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# edit a tag

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def editTag(request, pk):
    data = request.data
    try:
        tag = Tag.objects.get(_id=pk)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = TagSerializer(tag, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Get all the tags of a product

@api_view(['GET'])
def getProductTags(request, pk):
    product = Product.objects.get(_id=pk)
    tags = Tag.objects.filter(product=product)
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)