class AuthError(Exception): pass

class UserNotFoundError(AuthError):
    super().__init__("user was not found in database")

class PasswordIncorrectError(AuthError):
    super().__init__("password is incorrect")
    
class TokenNotValidError(AuthError):
    super().__init__("could not validate the token")