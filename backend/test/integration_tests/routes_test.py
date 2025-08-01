from app.main import app
from app.services.data_service import DataService
from app.database.models import Operation

from unittest import mock

# SIMPLE ROUTES TESTS
def test_get_user_operations(client):
    
    response = client.post("/user/data", json={"user_id" : 2})
        
    assert response.status_code == 200
    data = response.json()
     
    assert data == [
        {
            "operation_date": "2025-05-18",
            "category": "Utilities",
            "description": "Electricity bill",
            "value": -65.75,
            "currency": "USD"
        },
        {
            "operation_date": "2025-05-19",
            "category": "Dining",
            "description": "Dinner at Luigi's",
            "value": -45.00,
            "currency": "USD"
        },
        {
            "operation_date": "2025-05-22",
            "category": "Health",
            "description": "Pharmacy purchase",
            "value": -22.10,
            "currency": "USD"
        }
    ]
    
def test_get_user_operations(client):
    
    response = client.post("/user/data", json={"user_id" : 2})
        
    assert response.status_code == 200
    data = response.json()
     
    assert data == [
        {
            "operation_date": "2025-05-18",
            "category": "Utilities",
            "description": "Electricity bill",
            "value": -65.75,
            "currency": "USD"
        },
        {
            "operation_date": "2025-05-19",
            "category": "Dining",
            "description": "Dinner at Luigi's",
            "value": -45.00,
            "currency": "USD"
        },
        {
            "operation_date": "2025-05-22",
            "category": "Health",
            "description": "Pharmacy purchase",
            "value": -22.10,
            "currency": "USD"
        }
    ]

def test_chart(client):
    response = client.get("/chart?user_id=2")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data == {
        "coef": 0.1,
        "intercept": 5.8,
        "prediction": [
            -0.3,
            1.6,
            3.7
        ]
        
    }

def test_app_status(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {
        "status": "OK"
    }
