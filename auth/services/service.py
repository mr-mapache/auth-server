from typing import Callable
from typing import Union
from typing import Any
from typing import Awaitable
from inspect import signature
from auth.services.exceptions import HandlerNotFound

class Service:
    def __init__(
        self, 
        generator: Callable[[str], str] = lambda name: name,
        validator: Callable[[Any, Any], Any] = lambda type, payload: type(**payload)
    ):
        self.handlers = dict[str, Callable[..., Awaitable[Any]]]()
        self.exceptions: dict[type[Exception], Callable[[Exception], None]] = {}
        self.types = dict[str, Any]()
        self.generator = generator
        self.validator = validator
    
    def on(self, exception_type: type[Exception]):
        """
        Decorator for registering a handler for a given exception type. The handler is called when an exception of
        the given type is raised.

        Args:
            exception_type (type[Exception]): The type of the exception to be handled.
        
        Returns:
            The handler function.
        """
        def wrapper(handler: Callable[[Any, Exception], Awaitable[Any]]):
            self.exceptions[exception_type] = handler
            return handler
        return wrapper

    def validate(self, type: str, payload: Any):
        """
        Validate the payload associated with the given type. The type is used to determine the validator function to be used.
        The validator function defaults to the constructor of the type class. If you are using a validation library like pydantic,
        you can override the validator function to use the pydantic model_validate function.

        Args:
            type (str): The type of the payload to be validated.
            payload (Any): The payload to be validated.

        Raises:
            HandlerNotFound: If no handler is registered for the given type.

        Returns:
            The validated payload as an instance of the type class.
        """
        if type not in self.types.keys():
            raise HandlerNotFound(f"No handler registered for type: {type}")
        return self.validator(self.types[type], payload)

    @property
    def dependency_overrides(self) -> dict:
        return self.provider.dependency_overrides

    def register(self, annotation: Any, handler: Callable) -> None:
        """
        Register a handler for a given annotation. This method is called recursively to handle nested annotations.
        Don't call this method directly, use the handler decorator instead. This method is called by the handler decorator.

        Args:
            annotation (Any): The annotation to be registered.
            handler (Callable): The handler to be registered.
        """
        if hasattr(annotation, '__origin__'):
            origin = getattr(annotation, '__origin__')
            if isinstance(origin, type(Union)):
                for arg in getattr(annotation, '__args__'):
                    self.register(arg if not hasattr(arg, '__origin__') else getattr(arg, '__origin__'), handler)
            else:
                self.register(origin, handler)

        elif hasattr(annotation, '__args__'):
            for arg in getattr(annotation, '__args__'):
                self.register(arg if not hasattr(arg, '__origin__') else getattr(arg, '__origin__'), handler)
        else:
            key = self.generator(annotation.__name__)
            self.types[key] = annotation
            self.handlers[key] = handler
    
    def handler(self, wrapped: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        """
        Decorator for registering a function as a handler for a command or query type.

        Args:
            wrapped: The function to be registered as a handler.

        Returns:
            The original function, unmodified.
        """
        parameter = next(iter(signature(wrapped).parameters.values()))
        self.register(parameter.annotation, wrapped)
        return wrapped
    
    async def handle(self, request: Any, *args) -> Any:
        """
        Executes the handler associated with the given request.
        Args:
            request (Any): The request to be handled. The name of the request class is used to determine the handler to be executed
            using the generator function provided by the user. The generator functions defaults to the name of the request class.

        Raises:
            HandlerNotFound: If no handler is registered for the given request type.

        Returns:
            Any: The result of the handler function.
        """
        action = self.generator(request.__class__.__name__)
        handler = self.handlers.get(action, None)
        if not handler:
            raise HandlerNotFound(f"No handler registered for type: {action}")
        try:
            return await handler(request, *args)
        except Exception as exception:
            if type(exception) in self.exceptions:
                return await self.exceptions[type(exception)](request, exception)
            else:
                raise exception

    async def execute(self, action: str, payload: Any, *args) -> Any:
        """
        Executes the handler associated with the given request action and it's payload. It validates the payload
        asoociated with the action using the validator function provided by the user. The validator function defaults
        to the constructor of the action class. If you are using a validation library like pydantic, you can override
        the validator function to use the pydantic model_validate function.

        Args:
            action: to be executed
            payload: the payload to be passed to the handler
        Returns:
            The result of the handler function, if any.

        Raises:
            ValueError: If no handler is registered for the given command or query type.
        """
        request = self.validate(action, payload)
        return await self.handle(request, *args)