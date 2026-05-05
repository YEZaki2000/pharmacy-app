import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from inventory.models import Medicine, Category, Supplier

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def apotheker_user(db):
    return User.objects.create_user(
        username='apotheker_test',
        password='test123',
        role='pharmacist'
    )


@pytest.fixture
def klant_user(db):
    return User.objects.create_user(
        username='klant_test',
        password='test123',
        role='customer'
    )


@pytest.fixture
def categorie(db):
    return Category.objects.create(naam='Pijnstillers')


@pytest.fixture
def medicijn(db, categorie):
    return Medicine.objects.create(
        naam='Paracetamol',
        dosering='500mg',
        categorie=categorie,
        prijs=5.00,
        voorraad=100,
        minimum_voorraad=20
    )


@pytest.mark.django_db
class TestMedicineAPI:
    
    def test_list_medicines_zonder_auth(self, api_client):
        """Zonder token krijg je 401"""
        response = api_client.get('/api/inventory/medicines/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_medicines_met_auth(self, api_client, apotheker_user, medicijn):
        """Met token zie je medicijnen"""
        api_client.force_authenticate(user=apotheker_user)
        response = api_client.get('/api/inventory/medicines/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['naam'] == 'Paracetamol'
    
    def test_create_medicine_als_apotheker(self, api_client, apotheker_user, categorie):
        """Apotheker kan medicijn aanmaken"""
        api_client.force_authenticate(user=apotheker_user)
        
        data = {
            'naam': 'Ibuprofen',
            'dosering': '400mg',
            'categorie': categorie.id,
            'prijs': 7.50,
            'voorraad': 50,
            'minimum_voorraad': 10,
            'vereist_recept': False
        }
        
        response = api_client.post('/api/inventory/medicines/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Medicine.objects.count() == 1
        assert Medicine.objects.first().naam == 'Ibuprofen'
    
    def test_create_medicine_als_klant(self, api_client, klant_user, categorie):
        """Klant kan GEEN medicijn aanmaken"""
        api_client.force_authenticate(user=klant_user)
        
        data = {
            'naam': 'Ibuprofen',
            'dosering': '400mg',
            'categorie': categorie.id,
            'prijs': 7.50,
            'voorraad': 50,
            'minimum_voorraad': 10,
            'vereist_recept': False
        }
        
        response = api_client.post('/api/inventory/medicines/', data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_low_stock_endpoint(self, api_client, apotheker_user, categorie):
        """Low stock endpoint retourneert alleen medicijnen met lage voorraad"""
        api_client.force_authenticate(user=apotheker_user)
        
        # Medicijn met voldoende voorraad
        Medicine.objects.create(
            naam='Med1',
            dosering='100mg',
            categorie=categorie,
            prijs=5.00,
            voorraad=50,
            minimum_voorraad=20
        )
        
        # Medicijn met lage voorraad
        Medicine.objects.create(
            naam='Med2',
            dosering='200mg',
            categorie=categorie,
            prijs=10.00,
            voorraad=10,
            minimum_voorraad=20
        )
        
        response = api_client.get('/api/inventory/medicines/low_stock/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['naam'] == 'Med2'


@pytest.mark.django_db
class TestMedicineModel:
    
    def test_voorraad_laag_property(self, medicijn):
        """Test voorraad_laag property"""
        assert medicijn.voorraad_laag is False
        
        medicijn.voorraad = 15
        medicijn.save()
        
        assert medicijn.voorraad_laag is True
