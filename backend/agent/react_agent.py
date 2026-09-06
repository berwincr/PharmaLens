import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from agent.prompts import SYSTEM_PROMPT
from tools.medical_search import medical_information_search
from tools.pharmacy_search import pharmacy_availability_search
from tools.medicine_reminder import (
    create_medication_reminder,
    list_medication_reminders,
    cancel_medication_reminder
)
from memory.memory_manager import add_memory, get_memory

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


# =========================
# TOOL 1: Medical Search
# =========================

MEDICAL_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "medical_information_search",
        "description": (
            "Search for general medical information about a medicine "
            "using trusted medical sources."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "medicine_name": {
                    "type": "string",
                    "description": "The name of the medicine to search for."
                }
            },
            "required": ["medicine_name"]
        }
    }
}


PHARMACY_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "pharmacy_availability_search",
        "description": (
            "Search the web for pharmacy listings, online pharmacy pages, "
            "and medicine availability information for a specific medicine "
            "and location. Search results are not guaranteed to represent "
            "real-time stock. Never claim that a medicine is currently in "
            "stock unless the search result explicitly confirms current availability."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "medicine_name": {
                    "type": "string",
                    "description": "The name of the medicine."
                },
                "location": {
                    "type": "string",
                    "description": "The city or location where the medicine is needed."
                }
            },
            "required": ["medicine_name", "location"]
        }
    }
}

MEDICATION_REMINDER_TOOL = {
    "type": "function",
    "function": {
        "name": "create_medication_reminder",
        "description": (
            "Create a medication reminder using the medicine, time, and "
            "frequency explicitly provided by the user. "
            "Do not decide or recommend when a medicine should be taken."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "medicine_name": {
                    "type": "string",
                    "description": "The name of the medicine."
                },
                "reminder_time": {
                    "type": "string",
                    "description": (
                        "The time explicitly specified by the user, "
                        "preferably in HH:MM 24-hour format."
                    )
                },
                "frequency": {
                    "type": "string",
                    "description": (
                        "The reminder frequency explicitly specified by "
                        "the user, such as every day or every Sunday."
                    )
                }
            },
            "required": [
                "medicine_name",
                "reminder_time",
                "frequency"
            ]
        }
    }
}

LIST_MEDICATION_REMINDERS_TOOL = {
    "type": "function",
    "function": {
        "name": "list_medication_reminders",
        "description": (
            "Retrieve all medication reminders currently stored for the user."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}


CANCEL_MEDICATION_REMINDER_TOOL = {
    "type": "function",
    "function": {
        "name": "cancel_medication_reminder",
        "description": (
            "Cancel an existing medication reminder using its reminder ID. "
            "Only cancel a reminder when the user explicitly asks to cancel it."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "reminder_id": {
                    "type": "integer",
                    "description": "The ID of the reminder to cancel."
                }
            },
            "required": ["reminder_id"]
        }
    }
}

SAVE_MEMORY_TOOL = {
    "type": "function",
    "function": {
        "name": "save_memory",
        "description": "Save user-provided preferences or non-sensitive information for future conversations.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "The name of the information to remember."
                },
                "value": {
                    "type": "string",
                    "description": "The value provided by the user."
                }
            },
            "required": ["key", "value"]
        }
    }
}


RECALL_MEMORY_TOOL = {
    "type": "function",
    "function": {
        "name": "recall_memory",
        "description": "Retrieve previously saved user preferences or information.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}

# Map tool names to actual Python functions
TOOL_MAPPING = {
    "medical_information_search": medical_information_search,
    "pharmacy_availability_search": pharmacy_availability_search,
    "create_medication_reminder": create_medication_reminder,
    "list_medication_reminders": list_medication_reminders,
    "cancel_medication_reminder": cancel_medication_reminder,
    "save_memory": add_memory,
    "recall_memory": get_memory
}

def run_agent(user_input):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    # =========================
    # STEP 1: Ask the LLM
    # =========================

    response = client.chat.completions.create(
        model="openai/gpt-5-nano",
        messages=messages,
       tools=[
    MEDICAL_SEARCH_TOOL,
    PHARMACY_SEARCH_TOOL,
    MEDICATION_REMINDER_TOOL,
    LIST_MEDICATION_REMINDERS_TOOL,
    CANCEL_MEDICATION_REMINDER_TOOL,
    SAVE_MEMORY_TOOL,
    RECALL_MEMORY_TOOL
],
        tool_choice="auto"
    )

    message = response.choices[0].message

    # =========================
    # STEP 2: Check for tool call
    # =========================

    if message.tool_calls:

        # Add the assistant's tool-call message
        messages.append(message)

        for call in message.tool_calls:

            tool_name = call.function.name

            arguments = json.loads(
                call.function.arguments
            )

            # Find the Python function
            tool_function = TOOL_MAPPING.get(tool_name)

            if not tool_function:
                raise ValueError(
                    f"Unknown tool: {tool_name}"
                )

            # =========================
            # STEP 3: Execute the tool
            # =========================

            tool_result = tool_function(**arguments)

            # =========================
            # STEP 4: Send observation
            # back to the LLM
            # =========================

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(tool_result)
            })

    # =========================
    # STEP 5: Ask LLM for final answer
    # =========================

    final_response = client.chat.completions.create(
        model="openai/gpt-5-nano",
        messages=messages,
        tools=[
    MEDICAL_SEARCH_TOOL,
    PHARMACY_SEARCH_TOOL,
    MEDICATION_REMINDER_TOOL,
    LIST_MEDICATION_REMINDERS_TOOL,
    CANCEL_MEDICATION_REMINDER_TOOL,
    SAVE_MEMORY_TOOL,
    RECALL_MEMORY_TOOL
],
        tool_choice="auto"
    )

    return final_response.choices[0].message.content


# =========================
# Interactive Mode
# =========================

if __name__ == "__main__":

    print("Medicine Agent")
    print("Type 'exit' to quit.")
    print()

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        result = run_agent(user_input)

        print("Agent:", result)
        print()