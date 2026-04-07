import json
from agent.planner import generate_blueprint
from agent.generator import generate_spring_boot_templates


def main():
    print("=== Backend API Builder Agent ===")
    feature_request = input("Describe the backend feature: ").strip()

    blueprint = generate_blueprint(feature_request)

    print("\nGenerated Blueprint:\n")
    print(json.dumps(blueprint.model_dump(), indent=2))

    generated_files = generate_spring_boot_templates(blueprint)

    print("\nGenerated Spring Boot Templates:\n")
    for filename, content in generated_files.items():
        print(f"--- {filename} ---")
        print(content)


if __name__ == "__main__":
    main()