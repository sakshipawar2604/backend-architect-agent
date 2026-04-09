from pathlib import Path
from agent.models import Blueprint

SQL_TYPE_MAPPING = {
    "Long": "BIGINT",
    "String": "VARCHAR(255)",
    "BigDecimal": "DECIMAL(10,2)",
    "Integer": "INT",
    "LocalDateTime": "TIMESTAMP",
}

JAVA_TYPE_IMPORTS = {
    "LocalDateTime": "import java.time.LocalDateTime;",
    "BigDecimal": "import java.math.BigDecimal;",
}


PACKAGE_PATHS = {
    "entity": "entity",
    "dto": "dto",
    "controller": "controller",
    "service": "service",
    "repository": "repository",
    "root": "",  # for schema.sql
}


def to_base_entity_name(table_name: str) -> str:
    if table_name.endswith("ies"):
        return table_name[:-3] + "y"
    if table_name.endswith("es") and not table_name.endswith("ses"):
        return table_name[:-2]
    if table_name.endswith("s"):
        return table_name[:-1]
    return table_name


def to_class_name(name: str) -> str:
    return "".join(part.capitalize() for part in name.replace("-", "_").split("_"))


def to_variable_name(name: str) -> str:
    class_name = to_class_name(name)
    return class_name[0].lower() + class_name[1:]


def to_table_name(entity_name: str) -> str:
    base = entity_name.lower()
    if base.endswith("y"):
        return base[:-1] + "ies"
    if base.endswith("s"):
        return base + "es"
    return base + "s"


def parse_fields(fields: list[str]) -> list[tuple[str, str]]:
    parsed = []

    for field in fields:
        if ":" not in field:
            continue
        name, field_type = field.split(":", 1)
        parsed.append((name.strip(), field_type.strip()))

    return parsed


def build_import_block(field_specs: list[tuple[str, str]]) -> str:
    imports = sorted(
        {
            JAVA_TYPE_IMPORTS[field_type]
            for _, field_type in field_specs
            if field_type in JAVA_TYPE_IMPORTS
        }
    )

    if not imports:
        return ""

    return "\n".join(imports) + "\n"


def generate_entity(entity_name: str, field_specs: list[tuple[str, str]]) -> str:
    class_name = to_class_name(entity_name)
    table_name = to_table_name(entity_name)
    import_block = build_import_block(field_specs)

    field_lines = []
    for field_name, field_type in field_specs:
        if field_name == "id":
            field_lines.append("    @Id")
            field_lines.append("    @GeneratedValue(strategy = GenerationType.IDENTITY)")
        field_lines.append(f"    private {field_type} {field_name};")
        field_lines.append("")

    fields_block = "\n".join(field_lines).rstrip()

    return f"""package com.example.generated.entity;

import jakarta.persistence.*;
{import_block}
@Entity
@Table(name = "{table_name}")
public class {class_name} {{

{fields_block}
}}
"""


def generate_request_dto(entity_name: str, field_specs: list[tuple[str, str]]) -> str:
    class_name = to_class_name(entity_name)
    import_block = build_import_block(field_specs)

    dto_fields = [(name, field_type) for name, field_type in field_specs if name != "id"]
    fields_block = "\n".join(
        f"    private {field_type} {field_name};"
        for field_name, field_type in dto_fields
    )

    return f"""package com.example.generated.dto;

{import_block}public class {class_name}RequestDto {{

{fields_block}
}}
"""


def generate_response_dto(entity_name: str, field_specs: list[tuple[str, str]]) -> str:
    class_name = to_class_name(entity_name)
    import_block = build_import_block(field_specs)

    fields_block = "\n".join(
        f"    private {field_type} {field_name};"
        for field_name, field_type in field_specs
    )

    return f"""package com.example.generated.dto;

{import_block}public class {class_name}ResponseDto {{

{fields_block}
}}
"""


def generate_controller(entity_name: str) -> str:
    class_name = to_class_name(entity_name)
    variable_name = to_variable_name(entity_name)

    return f"""package com.example.generated.controller;

import com.example.generated.dto.{class_name}RequestDto;
import com.example.generated.dto.{class_name}ResponseDto;
import com.example.generated.service.{class_name}Service;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/{to_table_name(entity_name)}")
public class {class_name}Controller {{

    private final {class_name}Service {variable_name}Service;

    public {class_name}Controller({class_name}Service {variable_name}Service) {{
        this.{variable_name}Service = {variable_name}Service;
    }}

    @GetMapping
    public List<{class_name}ResponseDto> getAll() {{
        return {variable_name}Service.getAll();
    }}

    @GetMapping("/{{id}}")
    public {class_name}ResponseDto getById(@PathVariable Long id) {{
        return {variable_name}Service.getById(id);
    }}

    @PostMapping
    public {class_name}ResponseDto create(@RequestBody {class_name}RequestDto request) {{
        return {variable_name}Service.create(request);
    }}

    @PutMapping("/{{id}}")
    public {class_name}ResponseDto update(@PathVariable Long id, @RequestBody {class_name}RequestDto request) {{
        return {variable_name}Service.update(id, request);
    }}

    @DeleteMapping("/{{id}}")
    public void delete(@PathVariable Long id) {{
        {variable_name}Service.delete(id);
    }}
}}
"""


def generate_service(entity_name: str) -> str:
    class_name = to_class_name(entity_name)
    variable_name = to_variable_name(entity_name)

    return f"""package com.example.generated.service;

import com.example.generated.dto.{class_name}RequestDto;
import com.example.generated.dto.{class_name}ResponseDto;
import com.example.generated.repository.{class_name}Repository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class {class_name}Service {{

    private final {class_name}Repository {variable_name}Repository;

    public {class_name}Service({class_name}Repository {variable_name}Repository) {{
        this.{variable_name}Repository = {variable_name}Repository;
    }}

    public List<{class_name}ResponseDto> getAll() {{
        return List.of();
    }}

    public {class_name}ResponseDto getById(Long id) {{
        return new {class_name}ResponseDto();
    }}

    public {class_name}ResponseDto create({class_name}RequestDto request) {{
        return new {class_name}ResponseDto();
    }}

    public {class_name}ResponseDto update(Long id, {class_name}RequestDto request) {{
        return new {class_name}ResponseDto();
    }}

    public void delete(Long id) {{
        {variable_name}Repository.deleteById(id);
    }}
}}
"""


def generate_repository(entity_name: str) -> str:
    class_name = to_class_name(entity_name)

    return f"""package com.example.generated.repository;

import com.example.generated.entity.{class_name};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface {class_name}Repository extends JpaRepository<{class_name}, Long> {{
}}
"""


def generate_spring_boot_templates(blueprint: Blueprint) -> dict[str, tuple[str, str]]:
    generated_files = {}

    entity_map = {entity.name.lower(): entity for entity in blueprint.entities}

    for table_name in blueprint.database_tables:
        entity_name = to_base_entity_name(table_name)
        class_name = to_class_name(entity_name)

        entity_spec = entity_map.get(entity_name.lower())
        field_specs = parse_fields(entity_spec.fields) if entity_spec else [
            ("id", "Long"),
            ("name", "String"),
            ("createdAt", "LocalDateTime"),
        ]

        generated_files[f"{class_name}.java"] = ("entity", generate_entity(entity_name, field_specs))
        generated_files[f"{class_name}RequestDto.java"] = ("dto", generate_request_dto(entity_name, field_specs))
        generated_files[f"{class_name}ResponseDto.java"] = ("dto", generate_response_dto(entity_name, field_specs))
        generated_files[f"{class_name}Controller.java"] = ("controller", generate_controller(entity_name))
        generated_files[f"{class_name}Service.java"] = ("service", generate_service(entity_name))
        generated_files[f"{class_name}Repository.java"] = ("repository", generate_repository(entity_name))
        generated_files["schema.sql"] = ("root", generate_schema_sql(blueprint))

    return generated_files


def export_templates(
    generated_files: dict[str, tuple[str, str]],
    output_dir: str = "generated"
) -> list[str]:
    base_path = Path(output_dir) / "src" / "main" / "java" / "com" / "example" / "generated"
    saved_files = []

    for filename, (package_type, content) in generated_files.items():
        package_folder = PACKAGE_PATHS[package_type]
        file_path = base_path / package_folder / filename if package_folder else Path(output_dir) / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        saved_files.append(str(file_path))

    return saved_files

def generate_schema_sql(blueprint: Blueprint) -> str:
    statements = []

    entity_map = {entity.name.lower(): entity for entity in blueprint.entities}

    for table_name in blueprint.database_tables:
        entity_name = to_base_entity_name(table_name)
        entity_spec = entity_map.get(entity_name.lower())

        field_specs = parse_fields(entity_spec.fields) if entity_spec else [
            ("id", "Long"),
            ("name", "String"),
        ]

        column_lines = []

        for field_name, field_type in field_specs:
            sql_type = SQL_TYPE_MAPPING.get(field_type, "VARCHAR(255)")

            if field_name == "id":
                column_lines.append("    id BIGINT PRIMARY KEY AUTO_INCREMENT")
            else:
                column_lines.append(f"    {field_name} {sql_type}")

        table_sql = f"""CREATE TABLE {table_name} (
{",\n".join(column_lines)}
);"""

        statements.append(table_sql)

    return "\n\n".join(statements)