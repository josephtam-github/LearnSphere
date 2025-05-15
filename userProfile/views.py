# from rest_framework import status, generics, viewsets
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.decorators import action
# from django.core.cache import cache
# from django.shortcuts import get_object_or_404
# from django.db.models import Avg
# from learningCore.models import Language, LearningActivity

# from .models import (
#     Child, ParentSettings, ChildProgress
# )
# from .serializer import (
#     ChildSerializer, ParentSettingsSerializer,
#     ChildProgressSerializer
# )


# class ChildViewSet(viewsets.ModelViewSet):
#     serializer_class = ChildSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         return Child.objects.filter(parent=self.request.user)
    
#     def perform_create(self, serializer):
#         serializer.save(parent=self.request.user)
    
#     @action(detail=True, methods=['get'])
#     def progress(self, request, pk=None):
#         child = self.get_object()
#         progress = ChildProgress.objects.filter(child=child)
#         serializer = ChildProgressSerializer(progress, many=True)
#         return Response(serializer.data)
    
#     @action(detail=True, methods=['get'])
#     def recommended_activities(self, request, pk=None):
#         child = self.get_object()
        
#         # Cache key specific to this child
#         cache_key = f'recommended_activities_{child.id}'
#         cached_data = cache.get(cache_key)
        
#         if cached_data:
#             return Response(cached_data)
        
#         # Get child's primary language and level
#         primary_language = child.primary_language
#         level = child.language_level
        
#         # Get appropriate language object
#         try:
#             language = Language.objects.get(code=primary_language)
#         except Language.DoesNotExist:
#             return Response(
#                 {"error": "Language not found"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         # Find modules for this language and level
#         modules = LearningModule.objects.filter(
#             language=language,
#             level=level,
#             is_active=True
#         )
        
#         # Get completed activities
#         completed_activities = set()
#         progress_records = ChildProgress.objects.filter(child=child, language=language)
        
#         for record in progress_records:
#             completed_activities.update(record.completed_activities)
        
#         # Find activities the child hasn't completed yet
#         recommended = []
        
#         for module in modules:
#             activities = LearningActivity.objects.filter(
#                 module=module
#             ).exclude(id__in=completed_activities)[:5]  # Limit to 5 per module
            
#             serializer = LearningActivitySerializer(activities, many=True)
#             for activity in serializer.data:
#                 recommended.append(activity)
                
#                 # Limit total recommendations
#                 if len(recommended) >= 10:
#                     break
            
#             if len(recommended) >= 10:
#                 break
        
#         # Cache the results for 1 hour
#         cache.set(cache_key, recommended, 3600)
        
#         return Response(recommended)

# class ParentSettingsView(generics.RetrieveUpdateAPIView):
#     serializer_class = ParentSettingsSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_object(self):
#         return get_object_or_404(ParentSettings, parent=self.request.user)

# class ChildProgressViewSet(viewsets.ModelViewSet):
#     serializer_class = ChildProgressSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         # Parent can only see their children's progress
#         parent = self.request.user
#         return ChildProgress.objects.filter(child__parent=parent)
    
#     @action(detail=False, methods=['post'])
#     def record_activity(self, request):
#         # Expected request data:
#         # {
#         #    "child_id": 1,
#         #    "activity_id": 123,
#         #    "completed": true,
#         #    "score": 85  # Optional
#         # }
        
#         child_id = request.data.get('child_id')
#         activity_id = request.data.get('activity_id')
#         completed = request.data.get('completed', False)
#         score = request.data.get('score', 0)
        
#         # Validate child belongs to parent
#         try:
#             child = Child.objects.get(id=child_id, parent=request.user)
#         except Child.DoesNotExist:
#             return Response(
#                 {"error": "Child not found"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         # Validate activity exists
#         try:
#             activity = LearningActivity.objects.get(id=activity_id)
#         except LearningActivity.DoesNotExist:
#             return Response(
#                 {"error": "Activity not found"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         # Get or create progress record
#         module = activity.module
#         language = module.language
        
#         progress, created = ChildProgress.objects.get_or_create(
#             child=child,
#             module=module,
#             language=language,
#             defaults={
#                 'completed_activities': [],
#                 'mastery_percentage': 0.0
#             }
#         )
        
#         # Update completed activities
#         completed_activities = progress.completed_activities
        
#         if completed and activity_id not in completed_activities:
#             completed_activities.append(activity_id)
            
#             # Award points to child
#             child.total_points += activity.points
#             child.save()
            
#             # Update last activity timestamp
#             from django.utils import timezone
#             child.last_activity = timezone.now()
#             child.save()
            
#             # Update streak if needed
#             from datetime import date
#             today = date.today()
#             last_activity_date = getattr(child.last_activity, 'date', None)
            
#             if last_activity_date and last_activity_date < today:
#                 child.streak_days += 1
#                 child.save()
        
#         # Calculate mastery percentage
#         total_activities = LearningActivity.objects.filter(module=module).count()
#         if total_activities > 0:
#             mastery = (len(completed_activities) / total_activities) * 100
#             progress.mastery_percentage = round(mastery, 2)
        
#         progress.completed_activities = completed_activities
#         progress.save()
        
#         # Return updated progress
#         serializer = ChildProgressSerializer(progress)
#         return Response(serializer.data)

# class DashboardView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         # Parent dashboard summary
#         parent = request.user
#         children = Child.objects.filter(parent=parent)
        
#         # Cache key for this parent's dashboard
#         cache_key = f'dashboard_{parent.id}'
#         cached_data = cache.get(cache_key)
        
#         if cached_data:
#             return Response(cached_data)
        
#         # Collect summary data
#         children_data = []
        
#         for child in children:
#             # Get progress data
#             progress_records = ChildProgress.objects.filter(child=child)
#             avg_mastery = progress_records.aggregate(Avg('mastery_percentage'))['mastery_percentage__avg'] or 0
            
#             # Get language data
#             primary_language = None
#             try:
#                 primary_language = Language.objects.get(code=child.primary_language).name
#             except Language.DoesNotExist:
#                 primary_language = child.primary_language
            
#             # Build child summary
#             child_summary = {
#                 'id': child.id,
#                 'name': f"{child.first_name} {child.last_name}",
#                 'avatar': child.avatar,
#                 'primary_language': primary_language,
#                 'level': child.language_level,
#                 'points': child.total_points,
#                 'streak_days': child.streak_days,
#                 'average_mastery': round(avg_mastery, 2),
#                 'last_activity': child.last_activity,
#                 'languages_progress': {}
#             }
            
#             # Add language-specific progress
#             languages_progress = {}
            
#             for record in progress_records:
#                 lang_name = record.language.name
#                 if lang_name not in languages_progress:
#                     languages_progress[lang_name] = {
#                         'modules_count': 0,
#                         'average_mastery': 0,
#                         'activities_completed': 0
#                     }
                
#                 languages_progress[lang_name]['modules_count'] += 1
#                 languages_progress[lang_name]['activities_completed'] += len(record.completed_activities)
                
#                 # Update average mastery for this language
#                 current_avg = languages_progress[lang_name]['average_mastery']
#                 new_count = languages_progress[lang_name]['modules_count']
#                 languages_progress[lang_name]['average_mastery'] = (
#                     current_avg * (new_count - 1) + record.mastery_percentage
#                 ) / new_count
            
#             child_summary['languages_progress'] = languages_progress
#             children_data.append(child_summary)
        
#         # Overall metrics
#         total_children = len(children)
#         total_points = sum(child.total_points for child in children)
#         active_children = len([c for c in children if c.last_activity is not None])
        
#         dashboard_data = {
#             'parent_name': f"{parent.first_name} {parent.last_name}",
#             'total_children': total_children,
#             'active_children': active_children,
#             'total_family_points': total_points,
#             'children': children_data
#         }
        
#         # Cache the dashboard for 30 minutes
#         cache.set(cache_key, dashboard_data, 1800)
        
#         return Response(dashboard_data)
