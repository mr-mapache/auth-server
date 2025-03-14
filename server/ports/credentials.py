from typing import Protocol

class Secret(Protocol):
    """
    The 'Secret' protocol is a placeholder for any type representing a secret, such as a password,
    API key, or token. It allows for flexibility in the types of secrets that can be handled by
    the application, without enforcing a specific implementation.
    """

class Credentials(Protocol):
    """
    The 'Credentials' protocol outlines the structure for verifying user credentials.
    
    It requires the implementation of the 'verify' method, which will check the validity of a }
    given username and password. Implementations of this protocol should define how the verification 
    occurs, such as checking against a database or an external service.
    
    Methods:
        verify(username: Secret, password: Secret) -> bool:
            Verifies if the provided username and password combination is valid. 
            Returns True if valid, False otherwise.
    """
    async def add(self, username: Secret, password: Secret) -> None:
        """
        Adds a username-passowrd pair to a given user. This pair
        behaves as a single unit. Users should NOT be allowed to set a
        password without setting an username. 

        Args:
            username (Secret): A locally unique identifier for the user.
            password (Secret): A password for the user.
        """
    async def update(self, username: Secret, password: Secret) -> None:
        """
        Updates both the username and the password of a given user.

        Args:
            username (Secret): _description_
            password (Secret): _description_
        """
    
    async def verify(self, username: Secret, password: Secret) -> bool:
        """
        Verifies the username and password.
        
        Args:
            username (Secret): The username to be verified. 
            password (Secret): The password to be verified.
        
        Returns:
            bool: True if the credentials are valid, False otherwise.
        """