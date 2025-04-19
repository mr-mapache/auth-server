from typing import Protocol

class Secret(Protocol):
    """
    The 'Secret' protocol is a placeholder for any type representing a secret, such as a password,
    API key, or token.
    """

class Credentials(Protocol):
    """
    The 'Credentials' protocol outlines the structure for verifying user credentials.
    
    It requires the implementation of the 'verify' method, which will check the validity of a
    given username and password. Implementations of this protocol should define how the verification 
    occurs, such as checking against a database or an external service.
    
    Methods:
        verify(username: Secret, password: Secret) -> bool:
            Verifies if the provided username and password combination is valid. 
            Returns True if valid, False otherwise.
    """
    async def put(self, password: Secret) -> None:
        """
        Create or update a password to a given user. 

        Args:
            password (Secret): A password for the user.
        """
    
    async def verify(self, username: Secret, password: Secret) -> bool:
        """
        Verifies an username and password pair. 
        
        Args:
            username (Secret): The username to be verified. 
            password (Secret): The password to be verified.
        
        Returns:
            bool: True if the credentials are valid, False otherwise.
        """