# Pharmacy App
Een volledig apothekersysteem gebouwd met Django em Django REST Framework.



## Features
- Voorraadbeheer (medecijnen, leveranciers)
- Receptenbeheer met statusworkflow
- klantenbeheer
- REST API (klaar voor React Native)



## Installatie
```bash
git clone
cd pharmacy_project
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirmemts.txt
cp .env.example .env # Vul je eigen waarden in
python manage.py migrate
python manage.py runserver
```


## Tech stack
- Python 3.x / Django 4.2
- PostgreSQL
- Django REST Framework
- SimpleJWT
