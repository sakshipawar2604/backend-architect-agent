from pathlib import Path

from agent.generator import (
    generate_spring_boot_templates,
    export_templates,
    generate_schema_sql,
)
from agent.planner import generate_blueprint


def test_generate_templates_for_product_blueprint():
    blueprint = generate_blueprint("Create CRUD API for products")
    templates = generate_spring_boot_templates(blueprint)

    assert "Product.java" in templates
    assert "ProductController.java" in templates
    assert "ProductService.java" in templates
    assert "ProductRepository.java" in templates
    assert "ProductRequestDto.java" in templates
    assert "ProductResponseDto.java" in templates
    assert "schema.sql" in templates


def test_generated_entity_contains_expected_fields_and_annotations():
    blueprint = generate_blueprint("Create CRUD API for products")
    templates = generate_spring_boot_templates(blueprint)

    package_type, content = templates["Product.java"]

    assert package_type == "entity"
    assert "class Product" in content
    assert "@Entity" in content
    assert "@Id" in content
    assert "@GeneratedValue(strategy = GenerationType.IDENTITY)" in content
    assert 'Table(name = "products")' in content
    assert "private String name;" in content
    assert "private BigDecimal price;" in content


def test_generated_entity_contains_relationship_annotations():
    blueprint = generate_blueprint("Build order and payment management backend")
    templates = generate_spring_boot_templates(blueprint)

    _, order_entity = templates["Order.java"]
    _, payment_entity = templates["Payment.java"]

    assert "@ManyToOne" in order_entity
    assert '@JoinColumn(name = "user_id")' in order_entity
    assert "private User user;" in order_entity

    assert "@ManyToOne" in payment_entity
    assert '@JoinColumn(name = "order_id")' in payment_entity
    assert "private Order order;" in payment_entity


def test_generated_controller_uses_dtos():
    blueprint = generate_blueprint("Create CRUD API for products")
    templates = generate_spring_boot_templates(blueprint)

    package_type, content = templates["ProductController.java"]

    assert package_type == "controller"
    assert "import com.example.generated.dto.ProductRequestDto;" in content
    assert "import com.example.generated.dto.ProductResponseDto;" in content
    assert "public List<ProductResponseDto> getAll()" in content
    assert "public ProductResponseDto create(@RequestBody ProductRequestDto request)" in content


def test_generated_service_uses_repository_and_dtos():
    blueprint = generate_blueprint("Create CRUD API for products")
    templates = generate_spring_boot_templates(blueprint)

    package_type, content = templates["ProductService.java"]

    assert package_type == "service"
    assert "import com.example.generated.repository.ProductRepository;" in content
    assert "import com.example.generated.dto.ProductRequestDto;" in content
    assert "import com.example.generated.dto.ProductResponseDto;" in content
    assert "public ProductResponseDto create(ProductRequestDto request)" in content
    assert "productRepository.deleteById(id);" in content


def test_generate_schema_sql_includes_foreign_keys():
    blueprint = generate_blueprint("Build order and payment management backend")
    schema = generate_schema_sql(blueprint)

    assert "CREATE TABLE orders" in schema
    assert "user_id BIGINT" in schema
    assert "FOREIGN KEY (user_id) REFERENCES users(id)" in schema
    assert "CREATE TABLE payments" in schema
    assert "order_id BIGINT" in schema
    assert "FOREIGN KEY (order_id) REFERENCES orders(id)" in schema


def test_export_templates_creates_files(tmp_path: Path):
    blueprint = generate_blueprint("Create CRUD API for products")
    templates = generate_spring_boot_templates(blueprint)

    saved_files = export_templates(templates, output_dir=str(tmp_path))

    assert saved_files

    product_entity_path = (
        tmp_path
        / "src"
        / "main"
        / "java"
        / "com"
        / "example"
        / "generated"
        / "entity"
        / "Product.java"
    )

    product_controller_path = (
        tmp_path
        / "src"
        / "main"
        / "java"
        / "com"
        / "example"
        / "generated"
        / "controller"
        / "ProductController.java"
    )

    schema_path = tmp_path / "schema.sql"

    assert product_entity_path.exists()
    assert product_controller_path.exists()
    assert schema_path.exists()
    assert "class Product" in product_entity_path.read_text(encoding="utf-8")
    
def test_auth_generation():
    blueprint = generate_blueprint("Build user authentication system")
    templates = generate_spring_boot_templates(blueprint)

    assert "AuthController.java" in templates
    assert "AuthService.java" in templates
    assert "JwtService.java" in templates
    assert "LoginRequestDto.java" in templates
    assert "RegisterRequestDto.java" in templates
    assert "AuthResponseDto.java" in templates
    
def test_mapper_generation():
    blueprint = generate_blueprint("Create CRUD API for products")
    templates = generate_spring_boot_templates(blueprint)

    assert "ProductMapper.java" in templates

    _, content = templates["ProductMapper.java"]

    assert "class ProductMapper" in content
    assert "toResponseDto" in content
    assert "toEntity" in content
    
def test_service_uses_mapper():
    blueprint = generate_blueprint("Create CRUD API for products")
    templates = generate_spring_boot_templates(blueprint)

    _, service = templates["ProductService.java"]

    assert "ProductMapper" in service
    assert "toResponseDto" in service