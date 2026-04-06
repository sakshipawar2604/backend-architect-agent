import json
from agent.planner import generate_blueprint


def main():
    print("=== Backend API Builder Agent ===")
    feature_request = input("Describe the backend feature: ").strip()

    blueprint = generate_blueprint(feature_request)

    print("\nGenerated Blueprint:\n")
    print(json.dumps(blueprint.model_dump(), indent=2))


if __name__ == "__main__":
    main()