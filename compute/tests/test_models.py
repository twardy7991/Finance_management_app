from server.models import Regression
import pytest

@pytest.fixture
def linear_model():
    yield Regression()
    
def test_fit_lr(linear_model : Regression):
    
    data = [[1,0],[2,1],[3,2],[4,3]]
    
    linear_model.add_data(data=data)
    
    assert linear_model.fit() == ([[1.0]], 
                                  [-1.0], 
                                  [[0.0],[1.0],[2.0],[3.0]])
    

    
    
