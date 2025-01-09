from typing import Callable
from typing import Any
from typing import Awaitable
from inspect import signature

from fast_depends import inject
from fast_depends import Provider
from fast_depends import Depends as Depends

from typing import Callable
from typing import Any
from typing import Protocol

class Message(Protocol):

    def model_validate(self, payload: dict) -> None:...

class Messagebus:
    def __init__(self, key_generator: Callable[[str], str] = lambda name: name):
        self.key_generator = key_generator
        self.mapper = dict[str, type[Message]]()
        self.handlers = dict[str, Callable[[Message], Awaitable[Any]]]()
        self.provider = Provider()

    @property
    def dependency_overrides(self) -> dict[Callable, Callable]:
        return self.provider.dependency_overrides

    def validate(self, message_type: str, payload: dict[str, Any]) -> Message:
        message_class = self.mapper.get(message_type, None)
        if not message_class:
            raise NotImplementedError(f'Message {message_type} not found')
        return message_class.model_validate(payload)

    def handler(self, function: Callable[[Message], Awaitable[Any]]):
        function_signature = signature(function)
        parameter = next(iter(function_signature.parameters.values()))
        message_type = parameter.annotation
        key = self.key_generator(message_type.__name__)
        injected_handler = inject(function, cast=False, dependency_overrides_provider=self.provider)
        self.mapper[key] = message_type
        self.handlers[key] = injected_handler
        return function
    
    async def handle(self, message: Message) -> Any:
        key = self.key_generator(type(message).__name__)
        handler = self.handlers.get(key, None)
        if not handler:
            raise NotImplementedError(f'Handler for {key} not found')
        return await handler(message)