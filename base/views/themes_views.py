from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from ..models import *
from ..serializers import *

from rest_framework_simplejwt.serializers import *

from rest_framework import status


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
