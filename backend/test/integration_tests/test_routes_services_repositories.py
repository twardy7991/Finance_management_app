from operator import attrgetter
from pathlib import Path
from requests import Response

def test_get_user_operations(client):
    
    response = client.get("/user/data?user_id=2")
        
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

def test_save_user_operations(client):
    
    filepath = Path(__file__).parent
    
    with open(f"{filepath}/data/lista_operacji_small.csv", "rb") as f: 
        
        response = client.post(
            url="user/upload",
            data={"user_id": "2"},  
            files={"uploaded_file": ("lista_operacji_small.csv", f, "text/csv")} 
        )

    assert response.status_code == 200
    
    saved_operations : Response = client.get("/user/data?user_id=2")
    
    assert saved_operations.status_code == 200
    
    print(saved_operations.json())
    
    assert saved_operations.json() == [{'operation_date': '2025-02-21', 'category': 'BLIK', 'description': 'ALLEGRO.PL PŁATNOŚĆ BLIK P2P', 'value': -125.0, 'currency': 'PLN'},
                                        {'operation_date': '2025-02-22', 'category': 'Transport i paliwo', 'description': 'SHELL STACJA PALIW 1234  ZAKUP PRZY UŻYCIU KARTY W KRAJU', 'value': -239.99, 'currency': 'PLN'}, 
                                        {'operation_date': '2025-02-23', 'category': 'PRZELEW', 'description': 'ZUS ODDZIAŁ ŁÓDŹ  PRZELEW PRZYCHODZĄCY', 'value': 3500.0, 'currency': 'PLN'}, 
                                        {'operation_date': '2025-05-18', 'category': 'Utilities', 'description': 'Electricity bill', 'value': -65.75, 'currency': 'USD'},
                                        {'operation_date': '2025-05-19', 'category': 'Dining', 'description': "Dinner at Luigi's", 'value': -45.0, 'currency': 'USD'}, 
                                        {'operation_date': '2025-05-22', 'category': 'Health', 'description': 'Pharmacy purchase', 'value': -22.1, 'currency': 'USD'}]