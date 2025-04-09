from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count

from .models import (
    Language, LearningModule, LearningActivity
)
from .serializer import (
    LanguageSerializer, LearningModuleSerializer, LearningActivitySerializer
)



class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [AllowAny]  # Public information
    
    @action(detail=True, methods=['get'])
    def modules(self, request, pk=None):
        language = self.get_object()
        modules = LearningModule.objects.filter(language=language, is_active=True)
        
        # Optional filtering by level
        level = request.query_params.get('level', None)
        if level:
            modules = modules.filter(level=level)
        
        serializer = LearningModuleSerializer(modules, many=True)
        return Response(serializer.data)

class LearningModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LearningModule.objects.filter(is_active=True)
    serializer_class = LearningModuleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by language if specified
        language_code = self.request.query_params.get('language', None)
        if language_code:
            try:
                language = Language.objects.get(code=language_code)
                queryset = queryset.filter(language=language)
            except Language.DoesNotExist:
                pass
        
        # Filter by level if specified
        level = self.request.query_params.get('level', None)
        if level:
            queryset = queryset.filter(level=level)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        module = self.get_object()
        activities = LearningActivity.objects.filter(module=module)
        
        # Check if premium content should be included
        # This would need to be expanded with subscription logic
        include_premium = request.query_params.get('premium', 'false').lower() == 'true'
        if not include_premium:
            activities = activities.filter(is_premium=False)
        
        serializer = LearningActivitySerializer(activities, many=True)
        return Response(serializer.data)
