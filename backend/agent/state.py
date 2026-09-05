from typing import TypedDict


class AgentState(TypedDict):
    user_input: str
    thought: str
    action: str
    action_input: str
    observation: str
    final_answer: str