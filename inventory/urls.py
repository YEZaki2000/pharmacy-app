from django.urls import path, include
from .views import MedicineViewSet, CategoryViewSet, SupplierViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('medicines', MedicineViewSet, basename='medicine')
router.register('categories', CategoryViewSet, basename='category')
router.register('suppliers', SupplierViewSet, basename='supplier')

urlpatterns = [
    path('', include(router.urls)),
]
