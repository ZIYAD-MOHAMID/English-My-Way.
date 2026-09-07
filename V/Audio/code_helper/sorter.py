import json
import sys
import os


def clean_json_format(json_path):
    """Reads JSON, removes metadata, and saves only term and def."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("Error: JSON structure must be a list.")
        return

    # Create a new, clean list with only the fields you want
    cleaned_data = []
    for item in data:
        cleaned_item = {
            "term": item.get("term", ""),
            "def": item.get("def", "")
        }
        cleaned_data.append(cleaned_item)

    # Save the cleaned data back to the same file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print(f"Success! Stripped metadata from {len(cleaned_data)} items.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        if os.path.exists(target_file):
            clean_json_format(target_file)
        else:
            print(f"Error: File '{target_file}' not found.")
    else:
        print("Usage: python fix_json.py <your_file.json>")
