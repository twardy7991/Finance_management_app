from models import Regression
from dependency_injector.wiring import inject, Provide
from typing import List
from exceptions import RegressionError

### SERVICE CLASS FOR MODELS ###    
class ModelService:
    
    def __init__(self,lr : Regression):
        self.lr = lr
    
    def compute_lr(self, data) -> dict[float, float, List[float]]:
        
        self.lr.add_data(data=data)
        
        try:
            intercept, coef, prediction = self.lr.fit()
        
            response = {
                "intercept" : intercept,
                "coeff" : coef,
                "prediction" : prediction
            }
            
            return response
        except Exception as e:
            print(e)
            raise RegressionError from e
