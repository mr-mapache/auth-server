class UserAlreadyExists(Exception):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message)

class EmailAlreadyExists(Exception):
    def __init__(self, message: str = "Email already exists"):
        super().__init__(message)

class EmailNotFound(Exception):
    def __init__(self, message: str = "Email not found"):
        super().__init__(message)

class UserNotFound(Exception):
    def __init__(self, message: str = "User not found"):
        super().__init__(message)

class AccountNotFound(Exception):
    def __init__(self, message: str = "Account not found"):
        super().__init__(message)
        
class SessionNotFound(Exception):
    def __init__(self, message: str = "Session not found"):
        super().__init__(message)
