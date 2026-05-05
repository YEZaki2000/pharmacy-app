from django.shortcuts import render
from django.db import models
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Category, Supplier, Medicine
from .serializers import CategorySerializer, SupplierSerializer, MedicineSerializer

from core.permissions import IsPharmacistOrReadOnly
# Create your views here.


# Medicine viewset
class MedicineViewSet(viewsets.ModelViewSet):
    """
    ViewSet voor medicijnbeheer.
    
    list: Haal alle medicijnen op (met paginering, zoeken en filteren)
    create: Maak een nieuw medicijn aan (alleen apothekers)
    retrieve: Haal een specifiek medicijn op
    update: Werk een medicijn bij (alleen apothekers)
    destroy: Verwijder een medicijn (alleen apothekers)
    low_stock: Haal medicijnen met lage voorraad op
    add_stock: Verhoog de voorraad van een medicijn
    """
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsPharmacistOrReadOnly]

    # Filters
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categorie', 'vereist_recept', 'leverancier']
    search_fields = ['naam', 'dosering', 'omschrijving']
    ordering_fields = ['naam', 'prijs', 'voorraad', 'aangemaakt_op']
    ordering = ['naam']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        GET api/inventory/medicines/low_stock/
        Retourneert medicijnen waarvan de voorraad onder het minimum is.
        """
        low_stock_medicines = self.request.filter(
            voorraad__lte=models.F('minimum_voorraad')
        )
        serializer = self.get_serializer(low_stock_medicines, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_stock(self, request, pk=None):
        """
        POST api/inventory/medicines/{id}/add_stock/
        body: {hoeveelheid: 50}
        Verhoog de voorraad van een medicijn
        """
        medicine = self.get_object()
        hoeveelheid = request.data.get('hoeveelheid')
        if not hoeveelheid or int(hoeveelheid) <= 0:
            return Response(
                {"error": "Geef een geldige hoeveelheid op"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        medicine.voorraad += int(hoeveelheid)
        medicine.save()

        serializer = self.get_serializer(medicine)
        return Response(serializer.data)


# Supplier viewset
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['naam', 'contactpersoon']



# Category viewset
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
