#This is a general exception for the Service class.

class HandlerNotFound(Exception):
    def __init__(self, message: str = "Handler not implemented"):
        self.message = message
        super().__init__(self.message)


#This are specific exceptions for the auth service

class NotFoundError(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)

class AlreadyExistsError(Exception):
    def __init__(self, message: str = "Resource already exists"):
        self.message = message
        super().__init__(self.message)