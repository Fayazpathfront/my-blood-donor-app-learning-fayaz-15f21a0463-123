import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Mock get_db so tests don't need a real PostgreSQL connection
@pytest.fixture(autouse=True)
def mock_db():
    with patch('app.get_db') as mock:
        conn = MagicMock()
        cursor = MagicMock()

        # Default cursor returns for COUNT queries
        cursor.fetchone.return_value = [0]
        cursor.fetchall.return_value = []
        conn.cursor.return_value = cursor
        mock.return_value = conn

        yield mock


# Test 1: Home page loads
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


# Test 2: Donors page loads
def test_donors_page(client):
    response = client.get('/donors')
    assert response.status_code == 200


# Test 3: Register page loads
def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200


# Test 4: Request blood page loads
def test_request_page(client):
    response = client.get('/request-blood')  # ← correct route from app.py
    assert response.status_code == 200


# Test 5: Register a donor (POST)
def test_register_donor(client):
    response = client.post('/register', data={
        'name': 'John',
        'blood_group': 'A+',
        'phone': '9999999999',
        'city': 'Hyderabad'
    })
    assert response.status_code in [200, 302]