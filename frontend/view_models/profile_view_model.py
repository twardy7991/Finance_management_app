from models.user_model import UserModel

class ProfileViewModel:
    
    def __init__(self, model : UserModel = None):

        self.model = model
        self.username = "username"
        self.name = "name"
        self.surname = "surname"
        self.telephone = "phone"
        self.address = "address"
        self.email = "email"
        
        self.fetch_user()
        
    def fetch_user(self):
        response = self.model.get_user()
        
        user_data = response.json()
        
        self.name = user_data["name"]
        self.surname = user_data["surname"]
        self.telephone = user_data["telephone"]
        self.address = user_data["address"]
        