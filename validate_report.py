import json
import sys

def validate_json_report(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {filepath}: {e}")
        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    if not isinstance(data, list):
        print("Error: JSON root must be an array (list).")
        return False

    if len(data) == 0:
        print("Warning: JSON array is empty. This might indicate no TODOs were found, or an issue with parsing.")
    elif len(data) > 20:
        print(f"Error: JSON array contains {len(data)} items, which exceeds the limit of 20.")
        return False

    required_keys = {
        "title": str,
        "description": str,
        "deepLink": str,
        "filePath": str,
        "lineNumber": int,
        "confidence": int,
        "rationale": str,
        "context": str,
        "language": str
    }

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            print(f"Error at index {i}: Item is not a JSON object (dictionary).")
            return False

        for key, expected_type in required_keys.items():
            if key not in item:
                print(f"Error at index {i}: Missing required key '{key}'.")
                return False

            if not isinstance(item[key], expected_type):
                print(f"Error at index {i}: Key '{key}' should be of type {expected_type.__name__}, but got {type(item[key]).__name__}.")
                return False

        if item["confidence"] not in [1, 2, 3]:
            print(f"Error at index {i}: 'confidence' must be an integer between 1 and 3. Got: {item['confidence']}")
            return False

    print("JSON validation passed successfully!")
    return True

if __name__ == "__main__":
    filepath = "todo_report.json"
    if validate_json_report(filepath):
        sys.exit(0)
    else:
        sys.exit(1)
