from abc import ABC, abstractmethod
from sklearn.linear_model import LinearRegression
import numpy as np
from typing import List, Tuple

class AbstractModel(ABC):
    
    def __init__(self):
        pass
            
    def add_data(self, data : List[List[int]]):

        self.X : np.ndarray = np.array(data)[:, 1:]
        self.Y : np.ndarray = np.array(data)[:, 0].reshape(-1,1)
        
    @abstractmethod
    def fit(self):
        pass

class Regression(AbstractModel):

    def fit(self) -> Tuple[List[List[float]], float, List[List[float]]]:
        
        lr = LinearRegression().fit(X=self.X, y=self.Y)
        
        return (lr.coef_.round(1).tolist(), 
                lr.intercept_.round(1).tolist(), 
                lr.predict(self.X).round(1).tolist())