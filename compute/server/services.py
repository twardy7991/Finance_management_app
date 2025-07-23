from models import Regression
from dependency_injector.wiring import inject, Provide
from typing import Annotated

class RegressionError(BaseException):
    pass

class ModelService:
    
    def __init__(self,lr : Regression):
        self.lr = lr
    
    def compute_lr(self,data):
        
        self.lr.add_data(data=data)
        
        try:
            return self.lr.fit()
        except Exception as e:
            print(e)
            raise RegressionError from e
