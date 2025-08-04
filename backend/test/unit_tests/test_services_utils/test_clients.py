from app.services.utils.clients import ComputeClient
import pytest
import yaml

def test_send_request():
    
    with open("config/config.yml", "r") as f:
        config = yaml.safe_load(f) 

    base_url=config["compute"]["url"]
    
    compute_client = ComputeClient(base_url=base_url)
    
    data = [[1.0, 11.10],[2, 51.09],[5, 20.0],[4.0, 310.99]] 
            
    
    assert compute_client.send_request(data=data) == [[[0.0]],
                                                      [2.6],
                                                      [[2.6],[2.8],[2.6],[4.0]]]


    
        
