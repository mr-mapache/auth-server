class NotFoundError(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)

class AlreadyExistsError(Exception):
    def __init__(self, message: str = "Resource already exists"):
        self.message = message
        super().__init__(self.message)