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
- Generated Spring Boot controller/service/repository templates

## Current MVP

- Accepts a backend feature description
- Detects authentication, CRUD, or general backend intent
- Extracts known entities from prompts
- Generates a structured backend blueprint
- Produces starter Spring Boot templates as code output

## Next Steps

- Add entity and DTO generation
- Export generated templates into files
- Add automated tests
- Improve package structure and naming rules
