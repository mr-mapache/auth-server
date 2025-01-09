from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response, status
from auth.services.messagebus import Messagebus
from auth.services.messages import Command, Query

router = APIRouter()

async def messagebus_port(*args, **kwargs) -> Messagebus:
    raise NotImplementedError("Override this port with a concrete implementation")

@router.post('/command')
async def handle_command(command: Command, messagebus: Annotated[Messagebus, Depends(messagebus_port)]):
    command = messagebus.validate(command.type, command.payload)
    await messagebus.handle(command)
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.post('/query')
async def handle_query(query: Query, messagebus: Annotated[Messagebus, Depends(messagebus_port)]):
    query = messagebus.validate(query.type, query.parameters)
    return await messagebus.handle(query)