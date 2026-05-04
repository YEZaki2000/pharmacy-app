from django.urls import path, include
from .views import CustomerProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('customers', CustomerProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
