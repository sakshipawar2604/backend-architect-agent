from pydantic import BaseModel
from typing import List


class EndpointSpec(BaseModel):
    method: str
    path: str
    description: str


class EntitySpec(BaseModel):
    name: str
    fields: List[str]


class RelationshipSpec(BaseModel):
    source_entity: str
    target_entity: str
    relationship_type: str
    field_name: str
    join_column: str


class Blueprint(BaseModel):
    feature_name: str
    detected_intent: str
    entities: List[EntitySpec]
    endpoints: List[EndpointSpec]
    services: List[str]
    repositories: List[str]
    database_tables: List[str]
    relationships: List[RelationshipSpec] = []