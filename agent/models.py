from pydantic import BaseModel
from typing import List


class EndpointSpec(BaseModel):
    method: str
    path: str
    description: str


class EntitySpec(BaseModel):
    name: str
    fields: List[str]


class Blueprint(BaseModel):
    feature_name: str
    entities: List[EntitySpec]
    endpoints: List[EndpointSpec]
    services: List[str]
    database_tables: List[str]