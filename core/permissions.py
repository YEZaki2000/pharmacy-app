from rest_framework import permissions


class IsPharmacist(permissions.BasePermission):
    """
    Alleen apothekers hebben toegang
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and
            request.user.role == 'pharmacist'
        )


class IsCustomer(permissions.BasePermission):
    """
    Alleen klanten hebben toegang
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and
            request.user.role == 'customer'
        )


class IsPharmacistOrReadOnly(permissions.BasePermission):
    """
    Apothekers kunnen alles, klanten kunnen alleen lezen
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Iedereen mag lezen (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Alleen apothekers mogen schrijven (POST, PUT, PATCH, DELETE)
        return hasattr(request.user, 'role') and request.user.role == 'pharmacist'


class IsOwnerOrPharmacist(permissions.BasePermission):
    """
    Object permissie: eigen data of apotheker
    """
    def has_permission(self, request, view):
        """Check op view-niveau (lijst endpoints)"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Check op object-niveau (detail endpoints)"""
        # Check of user authenticated is
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Apothekers hebben altijd toegang
        if hasattr(request.user, 'role') and request.user.role == 'pharmacist':
            return True
        
        # Klanten alleen tot hun eigen data
        if hasattr(obj, 'user'):
            return obj.user == request.user  # ← Voor CustomerProfile
        if hasattr(obj, 'klant'):
            return obj.klant == request.user  # ← Voor Prescription
        
        return False
