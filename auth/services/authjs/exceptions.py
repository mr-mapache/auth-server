from auth.services.exceptions import AlreadyExistsError, NotFoundError

class UserAlreadyExists(AlreadyExistsError):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message)

class EmailAlreadyExists(AlreadyExistsError):
    def __init__(self, message: str = "Email already exists"):
        super().__init__(message)

class EmailNotFound(NotFoundError):
    def __init__(self, message: str = "Email not found"):
        super().__init__(message)

class UserNotFound(NotFoundError):
    def __init__(self, message: str = "User not found"):
        super().__init__(message)

class AccountNotFound(NotFoundError):
    def __init__(self, message: str = "Account not found"):
        super().__init__(message)
        
class SessionNotFound(NotFoundError):
    def __init__(self, message: str = "Session not found"):
        super().__init__(message)
