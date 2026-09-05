import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from agent.prompts import SYSTEM_PROMPT
from tools.medical_search import medical_information_search
from tools.medical_search import medical_information_search
from tools.pharmacy_search import pharmacy_availability_search

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

# Map tool names to actual Python functions
TOOL_MAPPING = {
    "medical_information_search": medical_information_search,
    "pharmacy_availability_search": pharmacy_availability_search
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
    PHARMACY_SEARCH_TOOL
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
    PHARMACY_SEARCH_TOOL
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