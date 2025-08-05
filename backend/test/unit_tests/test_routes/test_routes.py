from app.main import create_app
from app.services.data_service import DataService
from app.database.models import Operation
from unittest import mock

# SIMPLE ROUTES TESTS
def test_get_user_operations(client):
    
    service_mock = mock.Mock(spec=DataService)
    service_mock.get_user_operations.return_value = [
        Operation(operation_id=2, user_id=1, operation_date="2025-04-19", category="education", description="Online course payment", value=36.20, currency="PLN"),
        Operation(operation_id=3, user_id=1, operation_date="2025-05-19", category="education", description="Online course payment", value=36.20, currency="PLN"),
        Operation(operation_id=14, user_id=1, operation_date="2025-06-19", category="education", description="Online course payment", value=36.20, currency="PLN")
    ]

    app = create_app()
    with app.container.data_service.override(service_mock):
        response = client.get("/user/data?user_id=2")
        
    assert response.status_code == 200
    data = response.json()
     
    assert data == [
        {"operation_date" : "2025-04-19", "category" : "education", "description" : "Online course payment" , "value" : 36.20, "currency" : "PLN"},
        {"operation_date" : "2025-05-19", "category" : "education", "description" : "Online course payment" , "value" : 36.20, "currency" : "PLN"},
        {"operation_date" : "2025-06-19", "category" : "education", "description" : "Online course payment" , "value" : 36.20, "currency" : "PLN"}
    ]   
    
