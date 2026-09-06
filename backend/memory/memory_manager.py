import json
import os
from datetime import datetime


MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "memory.json"
)


def load_memory():
    """Load saved user memory."""

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_memory(memory):
    """Save memory to the JSON file."""

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


def add_memory(key, value):
    """Store a piece of user-provided information."""

    memory = load_memory()

    entry = {
        "key": key,
        "value": value,
        "created_at": datetime.now().isoformat()
    }

    memory.append(entry)

    save_memory(memory)

    return {
        "success": True,
        "message": "Memory saved successfully.",
        "memory": entry
    }


def get_memory():
    """Return all stored memories."""

    return {
        "success": True,
        "memory": load_memory()
    }


if __name__ == "__main__":
    print(add_memory("preferred_language", "Tamil"))
    print(get_memory())