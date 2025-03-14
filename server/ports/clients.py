from typing import Protocol
from typing import Literal
from typing import Optional

from server.ports.credentials import Secret

class Client(Protocol):
    """
    An application making protected resource requests on behalf of the
    resource owner and with its authorization.  The term "client" does
    not imply any particular implementation characteristics.
    """  
    @property
    def id(self) -> str:
        """
        The authorization server issues the registered client a client
        identifier -- a unique string representing the registration
        information provided by the client.  The client identifier is not a
        secret; it is exposed to the resource owner and MUST NOT be used
        alone for client authentication.  The client identifier is unique to
        the authorization server.
        """


    @property
    def type(self) -> Literal['confidential', 'public']:
        """
        OAuth defines two client types, based on their ability to
        authenticate securely with the authorization server (i.e., ability to
        maintain the confidentiality of their client credentials):

        confidential
            Clients capable of maintaining the confidentiality of their
            credentials (e.g., client implemented on a secure server with
            restricted access to the client credentials), or capable of secure
            client authentication using other means.

        public
            Clients incapable of maintaining the confidentiality of their
            credentials (e.g., clients executing on the device used by the
            resource owner, such as an installed native application or a web
            browser-based application), and incapable of secure client
            authentication via any other means.
        """

class Clients(Protocol):

    async def register(id: str, secret: Secret) -> Client:
        """
        Before initiating the protocol, the client registers with the
        authorization server. 

        Args:
            id (str): The client identifier issued to the client during
            the registration process.

            secret (Secret): The client secret. The client MAY omit the
            parameter if the client secret is an empty string.

        Returns:
            Client: The client is the application that is attempting to get access to the user's account. 
            It needs to get permission from the user before it can do so.
        """

    async def authenticate(id: str, secret: Secret) -> Optional[Client]:
        """ 
        If the client type is confidential, the client and authorization
        server establish a client authentication method suitable for the
        security requirements of the authorization server.  The authorization
        server MAY accept any form of client authentication meeting its
        security requirements.

        Args:
            id (str): The client ID you received when you first created the application.

            secret (Secret): The client MAY omit the
            parameter if the client secret is an empty string.

        Returns:
            Client: The authenticated client. Client authentication ensures that only authorized 
            clients can interact with the authorization server and access protected resources.  
        """

    async def delete(self, id: str) -> None:
        """
        Deletes a client from the server. 
        """