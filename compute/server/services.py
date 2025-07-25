from models import Regression
from dependency_injector.wiring import inject, Provide
from typing import List
from exceptions import RegressionError

class ModelService:
    
    def __init__(self,lr : Regression):
        self.lr = lr
    
    def compute_lr(self, data) -> dict[float, float, List[float]]:
        
        self.lr.add_data(data=data)
        
        try:
            coef, intercept, prediction = self.lr.fit()
        
            response = {
                "coef" : coef[0][0],
                "intercept" : intercept[0],
                "prediction" : [p[0] for p in prediction]
            }
            
            return response
        except Exception as e:
            print(e)
            raise RegressionError from e
