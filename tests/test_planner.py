from agent.planner import (
    detect_intent,
    detect_entities,
    detect_relationships,
    generate_blueprint,
)


def test_detect_intent_for_auth_requests():
    assert detect_intent("Build user authentication system") == "authentication"
    assert detect_intent("Add login and jwt support") == "authentication"


def test_detect_intent_for_crud_requests():
    assert detect_intent("Create CRUD API for products") == "crud"
    assert detect_intent("Manage orders with create update delete support") == "crud"


def test_detect_intent_for_general_requests():
    assert detect_intent("Build backend for notifications") == "general"


def test_detect_entities_from_known_keywords():
    entities = detect_entities("Build order and payment management backend")
    assert "order" in entities
    assert "payment" in entities


def test_detect_entities_falls_back_to_resource():
    entities = detect_entities("Build backend platform")
    assert entities == ["resource"]


def test_detect_relationships_for_order_and_payment_domain():
    relationships = detect_relationships(["order", "payment", "user"])

    assert any(
        rel.source_entity == "order" and rel.target_entity == "user"
        for rel in relationships
    )
    assert any(
        rel.source_entity == "payment" and rel.target_entity == "order"
        for rel in relationships
    )


def test_generate_auth_blueprint():
    blueprint = generate_blueprint("Build user auth system")

    assert blueprint.detected_intent == "authentication"
    assert blueprint.feature_name == "User Authentication System"
    assert "AuthService" in blueprint.services
    assert "users" in blueprint.database_tables
    assert any(rel.target_entity == "role" for rel in blueprint.relationships)


def test_generate_crud_blueprint_for_products():
    blueprint = generate_blueprint("Create CRUD API for products")

    assert blueprint.detected_intent == "crud"
    assert "products" in blueprint.database_tables
    assert "ProductService" in blueprint.services
    assert any(endpoint.path == "/api/products" for endpoint in blueprint.endpoints)
    

def test_detect_entities_from_natural_language():
    entities = detect_entities("I need backend for managing products and categories")

    assert "product" in entities
    assert "category" in entities


def test_detect_entities_with_service_phrase():
    entities = detect_entities("Create inventory service with product tracking")

    assert "inventory" in entities
    assert "product" in entities


def test_detect_auth_intent_from_login_signup():
    assert detect_intent("Build login and signup system") == "authentication"