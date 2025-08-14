class AuthError(Exception): pass

class PasswordIncorrectError(AuthError):
    def __init__(self):
        super().__init__("password is incorrect")

class UsernameIncorrectError(AuthError):
    def __init__(self):
        super().__init__("username is incorrect")
    
class TokenNotValidError(AuthError):
    
    def __init__(self):
        super().__init__("could not validate the token")
        
class ServiceError(Exception): pass

class OperationsNotFoundError(ServiceError):
    
    def __init__(self, message) :
        super().__init__(message)
    
class UserNotFoundError(ServiceError):
    
    def __init__(self):
        super().__init__("user was not found in database")

