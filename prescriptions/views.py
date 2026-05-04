from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status

from .models import Prescription, PrescriptionItem
from .serializers import (
    PrescriptionSerializer,
    PrescriptionCreateSerializer,
    PrescriptionItemSerializer
)
from core.permissions import IsOwnerOrPharmacist


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer  # ← TOEVOEGEN
    permission_classes = [IsOwnerOrPharmacist]  # ← UNCOMMENT

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'klant']
    search_fields = ['arts_naam', 'notities']
    ordering_fields = ['datum', 'aangemaakt_op', 'status']
    ordering = ['-aangemaakt_op']

    def get_queryset(self):
        """Apothekers zien alles, klanten alleen hun eigen recepten"""
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'pharmacist':
            return Prescription.objects.all()  # ← QUERYSET, niet serializer!
        return Prescription.objects.filter(klant=user)  # ← QUERYSET, niet serializer!

    def get_serializer_class(self):
        """Gebruik CreateSerializer voor POST, anders PrescriptionSerializer"""
        if self.action == 'create':
            return PrescriptionCreateSerializer
        return PrescriptionSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOrPharmacist])
    def change_status(self, request, pk=None):
        """
        POST /api/prescriptions/{id}/change_status/
        Body: {"status": "klaar"}
        """
        prescription = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Prescription.Status.choices):  # ← dict() met kleine d
            return Response(
                {"error": "Ongeldige status"},
                status=status.HTTP_400_BAD_REQUEST  # ← één status, niet status.status
            )

        prescription.status = new_status
        prescription.save()

        serializer = self.get_serializer(prescription)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_prescriptions(self, request):
        """
        GET /api/prescriptions/my_prescriptions/
        Retourneert recepten van de ingelogde gebruiker
        """
        prescriptions = self.get_queryset().filter(klant=request.user)  # ← gebruik get_queryset()
        serializer = self.get_serializer(prescriptions, many=True)
        return Response(serializer.data)
