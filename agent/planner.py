import re
from agent.models import Blueprint, EntitySpec, EndpointSpec


KNOWN_ENTITIES = {
    "user": ["id: Long", "name: String", "email: String", "password: String", "createdAt: LocalDateTime"],
    "product": ["id: Long", "name: String", "description: String", "price: BigDecimal", "createdAt: LocalDateTime"],
    "order": ["id: Long", "orderNumber: String", "status: String", "totalAmount: BigDecimal", "createdAt: LocalDateTime"],
    "payment": ["id: Long", "amount: BigDecimal", "status: String", "paymentMethod: String", "createdAt: LocalDateTime"],
    "role": ["id: Long", "name: String", "description: String"],
    "category": ["id: Long", "name: String", "description: String"],
    "inventory": ["id: Long", "sku: String", "quantity: Integer", "updatedAt: LocalDateTime"],
}


def to_class_name(word: str) -> str:
    return word.strip().capitalize()


def to_table_name(word: str) -> str:
    base = word.strip().lower()
    if base.endswith("y"):
        return base[:-1] + "ies"
    if base.endswith("s"):
        return base + "es"
    return base + "s"


def detect_intent(feature_request: str) -> str:
    request = feature_request.lower()

    if any(keyword in request for keyword in ["auth", "authentication", "login", "register", "jwt"]):
        return "authentication"

    if any(keyword in request for keyword in ["crud", "create", "update", "delete", "list", "manage"]):
        return "crud"

    return "general"


def detect_entities(feature_request: str) -> list[str]:
    request = feature_request.lower()
    detected = [entity for entity in KNOWN_ENTITIES.keys() if entity in request]

    if detected:
        return detected

    matches = re.findall(r"\bfor\s+([a-zA-Z]+)", request)
    if matches:
        return [matches[0].lower()]

    return ["resource"]


def build_entity_specs(entity_names: list[str]) -> list[EntitySpec]:
    specs = []

    for entity in entity_names:
        fields = KNOWN_ENTITIES.get(
            entity,
            ["id: Long", "name: String", "createdAt: LocalDateTime"]
        )
        specs.append(
            EntitySpec(
                name=to_class_name(entity),
                fields=fields
            )
        )

    return specs


def build_crud_endpoints(entity_names: list[str]) -> list[EndpointSpec]:
    endpoints = []

    for entity in entity_names:
        plural = to_table_name(entity)

        endpoints.extend([
            EndpointSpec(
                method="GET",
                path=f"/api/{plural}",
                description=f"List all {plural}"
            ),
            EndpointSpec(
                method="GET",
                path=f"/api/{plural}" + "/{id}",
                description=f"Get {entity} by id"
            ),
            EndpointSpec(
                method="POST",
                path=f"/api/{plural}",
                description=f"Create a new {entity}"
            ),
            EndpointSpec(
                method="PUT",
                path=f"/api/{plural}" + "/{id}",
                description=f"Update an existing {entity}"
            ),
            EndpointSpec(
                method="DELETE",
                path=f"/api/{plural}" + "/{id}",
                description=f"Delete a {entity}"
            ),
        ])

    return endpoints


def build_auth_blueprint() -> Blueprint:
    entities = [
        EntitySpec(
            name="User",
            fields=[
                "id: Long",
                "name: String",
                "email: String",
                "password: String",
                "role: String",
                "createdAt: LocalDateTime",
            ],
        ),
        EntitySpec(
            name="Role",
            fields=[
                "id: Long",
                "name: String",
                "description: String",
            ],
        ),
    ]

    endpoints = [
        EndpointSpec(
            method="POST",
            path="/api/auth/register",
            description="Register a new user",
        ),
        EndpointSpec(
            method="POST",
            path="/api/auth/login",
            description="Authenticate user and return token",
        ),
        EndpointSpec(
            method="POST",
            path="/api/auth/refresh",
            description="Refresh access token",
        ),
        EndpointSpec(
            method="GET",
            path="/api/users/{id}",
            description="Fetch user profile by id",
        ),
    ]

    return Blueprint(
        feature_name="User Authentication System",
        detected_intent="authentication",
        entities=entities,
        endpoints=endpoints,
        services=["AuthService", "UserService", "JwtService", "RoleService"],
        repositories=["UserRepository", "RoleRepository"],
        database_tables=["users", "roles"],
    )


def build_crud_blueprint(feature_request: str, entity_names: list[str]) -> Blueprint:
    class_names = [to_class_name(entity) for entity in entity_names]

    services = [f"{name}Service" for name in class_names]
    repositories = [f"{name}Repository" for name in class_names]
    tables = [to_table_name(entity) for entity in entity_names]

    return Blueprint(
        feature_name=feature_request.title(),
        detected_intent="crud",
        entities=build_entity_specs(entity_names),
        endpoints=build_crud_endpoints(entity_names),
        services=services,
        repositories=repositories,
        database_tables=tables,
    )


def build_general_blueprint(feature_request: str, entity_names: list[str]) -> Blueprint:
    class_names = [to_class_name(entity) for entity in entity_names]
    tables = [to_table_name(entity) for entity in entity_names]

    return Blueprint(
        feature_name=feature_request.title(),
        detected_intent="general",
        entities=build_entity_specs(entity_names),
        endpoints=[
            EndpointSpec(
                method="GET",
                path="/api/health",
                description="Health check endpoint",
            )
        ],
        services=[f"{name}Service" for name in class_names],
        repositories=[f"{name}Repository" for name in class_names],
        database_tables=tables,
    )


def generate_blueprint(feature_request: str) -> Blueprint:
    intent = detect_intent(feature_request)
    entities = detect_entities(feature_request)

    if intent == "authentication":
        return build_auth_blueprint()

    if intent == "crud":
        return build_crud_blueprint(feature_request, entities)

    return build_general_blueprint(feature_request, entities)