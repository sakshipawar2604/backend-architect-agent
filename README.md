# Backend API Builder Agent

A simple AI-inspired backend planning tool that converts plain English feature requests into a structured backend blueprint and starter Spring Boot templates.

## Example Inputs

- Build user auth system
- Create CRUD API for products
- Build order and payment management backend

## Output Includes

- Suggested entities
- API endpoints
- Service classes
- Repository classes
- Database tables
- Detected backend intent
- Generated JPA entities
- Generated request/response DTOs
- Generated Spring Boot controller/service/repository templates
- Exported Java files in a generated project structure
- Generated SQL schema (schema.sql)

## Current MVP

- Accepts a backend feature description
- Detects authentication, CRUD, or general backend intent
- Extracts known entities from prompts
- Generates a structured backend blueprint
- Produces starter Spring Boot templates
- Generates entity and DTO classes
- Writes generated files into a local output directory
- Includes unit tests for planner and generator logic
- Uses DTO-aware controller and service signatures
- Adds basic JPA annotations for generated entities

## Output Structure

```text
generated/
└── src/main/java/com/example/generated/
    ├── controller/
    ├── dto/
    ├── entity/
    ├── repository/
    └── service/
```

## Generated Database Schema

The tool generates a basic SQL schema based on detected entities.

Example:

```sql
CREATE TABLE products (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    description VARCHAR(255),
    price DECIMAL(10,2)
);
```

## Authentication Support

For authentication-related prompts, the generator produces:

- AuthController
- AuthService
- JwtService
- Login/Register DTOs
- AuthResponse DTO

Example:

Input:

- Build user authentication system

Output:

- /api/auth/login
- /api/auth/register
- JWT scaffolding

## Mapper Layer

The generator now includes a mapper layer for converting:

- Entity → Response DTO
- Request DTO → Entity

Example:

- ProductMapper.java
- UserMapper.java

This reflects real-world backend architecture practices.
