import json


def load_logs(file_path):
    """
    Load API logs from a JSON file.
    """

    try:
        with open(file_path, "r") as file:
            logs = json.load(file)

        print(f"✅ Successfully loaded {len(logs)} log entries.")

        return logs

    except Exception as e:
        print(f"❌ Error loading logs: {e}")

        return []