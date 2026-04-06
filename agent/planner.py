from agent.models import Blueprint, EntitySpec, EndpointSpec


def generate_blueprint(feature_request: str) -> Blueprint:
    request = feature_request.lower().strip()

    if "auth" in request or "authentication" in request:
        return Blueprint(
            feature_name="User Authentication System",
            entities=[
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
                )
            ],
            endpoints=[
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
                    method="GET",
                    path="/api/users/{id}",
                    description="Fetch user profile by id",
                ),
            ],
            services=[
                "AuthService",
                "UserService",
                "JwtService",
            ],
            database_tables=[
                "users",
            ],
        )

    return Blueprint(
        feature_name=feature_request.title(),
        entities=[
            EntitySpec(
                name="MainEntity",
                fields=[
                    "id: Long",
                    "name: String",
                    "createdAt: LocalDateTime",
                ],
            )
        ],
        endpoints=[
            EndpointSpec(
                method="GET",
                path="/api/main",
                description="List records",
            ),
            EndpointSpec(
                method="POST",
                path="/api/main",
                description="Create record",
            ),
        ],
        services=[
            "MainService",
        ],
        database_tables=[
            "main_entities",
        ],
    )