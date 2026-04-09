from pathlib import Path
from agent.models import Blueprint


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
    import_block = build_import_block(field_specs)

    fields_block = "\n".join(
        f"    private {field_type} {field_name};"
        for field_name, field_type in field_specs
    )

    return f"""package com.example.generated.entity;

import jakarta.persistence.*;

{import_block}@Entity
@Table(name = "{entity_name.lower()}s")
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

import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/{entity_name.lower()}s")
public class {class_name}Controller {{

    private final {class_name}Service {variable_name}Service;

    public {class_name}Controller({class_name}Service {variable_name}Service) {{
        this.{variable_name}Service = {variable_name}Service;
    }}

    @GetMapping
    public List<String> getAll() {{
        return {variable_name}Service.getAll();
    }}

    @GetMapping("/{{id}}")
    public String getById(@PathVariable Long id) {{
        return {variable_name}Service.getById(id);
    }}

    @PostMapping
    public String create() {{
        return {variable_name}Service.create();
    }}

    @PutMapping("/{{id}}")
    public String update(@PathVariable Long id) {{
        return {variable_name}Service.update(id);
    }}

    @DeleteMapping("/{{id}}")
    public String delete(@PathVariable Long id) {{
        return {variable_name}Service.delete(id);
    }}
}}
"""


def generate_service(entity_name: str) -> str:
    class_name = to_class_name(entity_name)
    variable_name = to_variable_name(entity_name)

    return f"""package com.example.generated.service;

import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class {class_name}Service {{

    private final {class_name}Repository {variable_name}Repository;

    public {class_name}Service({class_name}Repository {variable_name}Repository) {{
        this.{variable_name}Repository = {variable_name}Repository;
    }}

    public List<String> getAll() {{
        return List.of("List all {entity_name}");
    }}

    public String getById(Long id) {{
        return "Get {entity_name} by id: " + id;
    }}

    public String create() {{
        return "Create {entity_name}";
    }}

    public String update(Long id) {{
        return "Update {entity_name} by id: " + id;
    }}

    public String delete(Long id) {{
        return "Delete {entity_name} by id: " + id;
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

    return generated_files


def export_templates(
    generated_files: dict[str, tuple[str, str]],
    output_dir: str = "generated"
) -> list[str]:
    base_path = Path(output_dir) / "src" / "main" / "java" / "com" / "example" / "generated"
    saved_files = []

    for filename, (package_type, content) in generated_files.items():
        package_folder = PACKAGE_PATHS[package_type]
        file_path = base_path / package_folder / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        saved_files.append(str(file_path))

    return saved_files