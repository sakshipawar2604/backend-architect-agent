from agent.models import Blueprint


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


def generate_controller(entity_name: str) -> str:
    class_name = to_class_name(entity_name)
    variable_name = class_name[0].lower() + class_name[1:]

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
    variable_name = class_name[0].lower() + class_name[1:]

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

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface {class_name}Repository extends JpaRepository<{class_name}, Long> {{
}}
"""


def generate_spring_boot_templates(blueprint: Blueprint) -> dict[str, str]:
    generated_files = {}

    for table_name in blueprint.database_tables:
        entity_name = to_base_entity_name(table_name)
        class_name = to_class_name(entity_name)

        generated_files[f"{class_name}Controller.java"] = generate_controller(entity_name)
        generated_files[f"{class_name}Service.java"] = generate_service(entity_name)
        generated_files[f"{class_name}Repository.java"] = generate_repository(entity_name)

    return generated_files