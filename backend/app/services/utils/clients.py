### CLIENT RESPONSIBLE FOR CONNECTING TO COMPUTING SERVER ###

import requests

class ComputeClient:
    
    def __init__(self, base_url : str):
        self.base_url = base_url
    
    def send_request(self, data):

        payload : dict = {
            "data" : data
        }

        response = requests.post(f"{self.base_url}/models/lr", json=payload)

        response.raise_for_status()
        
        return response.json()
        
        