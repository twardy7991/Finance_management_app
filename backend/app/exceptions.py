### EXCEPTIONS FOR MAIN ###

class ConfigError(Exception):
    
    def __init__(self, message : str):
        super().__init__(f"config is incomplete: {message}")
        
class DatabaseURLMissingError(ConfigError):
    
    def __init__(self):
        super().__init__("database url is missing")