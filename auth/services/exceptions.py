class HandlerNotFound(Exception):
    def __init__(self, message: str = "Handler not implemented"):
        self.message = message
        super().__init__(self.message)