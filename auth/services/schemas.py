from pydantic import BaseModel

class Command(BaseModel):
    type: str
    payload: dict

class Query(BaseModel):
    type: str
    parameters: dict

def validator(type: BaseModel, payload: dict) -> Command | Query:
    return type.model_validate(payload)