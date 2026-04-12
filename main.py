import argparse
import json

from agent.planner import generate_blueprint
from agent.generator import generate_spring_boot_templates, export_templates


def parse_args():
    parser = argparse.ArgumentParser(
        description="Backend API Builder Agent"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Backend feature description to generate from",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="generated",
        help="Directory where generated files will be written",
    )
    parser.add_argument(
        "--no-schema",
        action="store_true",
        help="Skip schema.sql generation",
    )
    parser.add_argument(
        "--no-auth",
        action="store_true",
        help="Skip authentication-specific files even for auth prompts",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("=== Backend API Builder Agent ===")

    feature_request = args.prompt
    if not feature_request:
        feature_request = input("Describe the backend feature: ").strip()

    blueprint = generate_blueprint(feature_request)

    print("\nGenerated Blueprint:\n")
    print(json.dumps(blueprint.model_dump(), indent=2))

    generated_files = generate_spring_boot_templates(
        blueprint=blueprint,
        include_schema=not args.no_schema,
        include_auth_support=not args.no_auth,
    )

    saved_files = export_templates(
        generated_files=generated_files,
        output_dir=args.output_dir,
    )

    print("\nSaved Generated Files:\n")
    for file_path in saved_files:
        print(f"- {file_path}")


if __name__ == "__main__":
    main()