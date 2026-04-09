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

## Current MVP

- Accepts a backend feature description
- Detects authentication, CRUD, or general backend intent
- Extracts known entities from prompts
- Generates a structured backend blueprint
- Produces starter Spring Boot templates
- Generates entity and DTO classes
- Writes generated files into a local output directory
- Includes unit tests for planner and generator logic

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
