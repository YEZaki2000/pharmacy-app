from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import CustomerProfile
from .serializers import CustomerProfileSerializer

from core.permissions import IsOwnerOrPharmacist

# Create your views here.
class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsOwnerOrPharmacist]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'telefoon']

    action(detail=False, methods=['get'])
    def me(self):
        """
        GET /api/customers/me/
        Retourneert profiel van ingelogde gebruiker
        """

        try:
            profile = CustomerProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer)
        except CustomerProfile.DoesNotExist:
            return Response(
                {"detail": "Profiel niet gevonden"},
                status=404
            )
            
