from django.urls import path, include
from rest_framework.routers import DefaultRouter
from learningCore.views import LanguageViewSet, LearningModuleViewSet
from userAuth.views import ParentRegistrationView
from userProfile.views import ChildProgressViewSet, ChildViewSet, ParentSettingsView, DashboardView
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView

def redirect_to_docs(request):
    return redirect('https://documenter.getpostman.com/view/24232846/2sAYX8KMrD')

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'children', ChildViewSet, basename='child')
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'modules', LearningModuleViewSet, basename='module')
router.register(r'progress', ChildProgressViewSet, basename='progress')

# API v1 patterns
v1_patterns = [
    # Authentication endpoints
    path('register/', ParentRegistrationView.as_view(), name='parent-registration'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Parent settings
    path('settings/', ParentSettingsView.as_view(), name='parent-settings'),
    
    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Include router URLs
    path('', include(router.urls)),
]

urlpatterns = [
    # API Documentation redirect
    path('', redirect_to_docs, name='api-docs'),
    
    # Version 1 API
    path('v1/', include(v1_patterns)),
]