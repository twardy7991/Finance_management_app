from abc import ABC, abstractmethod
from typing import List, Tuple

from sklearn.linear_model import LinearRegression
import numpy as np

### ABSTRACT CLASS FOR MODELS ###

class AbstractModel(ABC):
    
    def __init__(self):
        pass
            
    def add_data(self, data : List[List[int]]):

        self.X : np.ndarray = np.array(data)[:, 1:]
        self.Y : np.ndarray = np.array(data)[:, 0].reshape(-1,1)
        
    @abstractmethod
    def fit(self) -> Tuple[List[List[float]], float, List[List[float]]]:
        pass

### LINEAR REGRESSION MODEL ###

class Regression(AbstractModel):

    def fit(self):
        
        lr = LinearRegression().fit(X=self.X, y=self.Y)
        
        prediction = lr.predict(self.X).round(1)
        
        return (lr.intercept_.round(1).tolist()[0], 
                lr.coef_.round(1).tolist()[0], 
                [p[0] for p in prediction.tolist()])