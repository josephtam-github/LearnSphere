from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count

from .models import Parent
from .serializer import ParentRegistrationSerializer

class ParentRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ParentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            parent = serializer.save()
            # Send verification email logic would go here
            return Response({
                'message': 'Registration successful! Please verify your email.',
                'parent_id': parent.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
