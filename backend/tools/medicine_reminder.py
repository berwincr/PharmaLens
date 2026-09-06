import json
import os
from datetime import datetime


REMINDER_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "reminders.json"
)


def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        return []

    with open(REMINDER_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_reminders(reminders):
    with open(REMINDER_FILE, "w", encoding="utf-8") as file:
        json.dump(reminders, file, indent=4)


def create_medication_reminder(
    medicine_name,
    reminder_time,
    frequency
):
    """
    Create a reminder using the schedule explicitly
    provided by the user.
    """

    reminders = load_reminders()

    reminder = {
        "id": len(reminders) + 1,
        "medicine": medicine_name,
        "time": reminder_time,
        "frequency": frequency,
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }

    reminders.append(reminder)

    save_reminders(reminders)

    return {
        "success": True,
        "message": "Medication reminder created successfully.",
        "reminder": reminder
    }

def list_medication_reminders():
    """
    Return all stored medication reminders.
    """

    reminders = load_reminders()

    return {
        "success": True,
        "reminders": reminders
    }

def cancel_medication_reminder(reminder_id):
    """
    Cancel an active medication reminder by its ID.
    """

    reminders = load_reminders()

    for reminder in reminders:
        if reminder["id"] == reminder_id:
            if reminder["status"] == "cancelled":
                return {
                    "success": False,
                    "message": "Reminder is already cancelled."
                }

            reminder["status"] = "cancelled"
            save_reminders(reminders)

            return {
                "success": True,
                "message": "Medication reminder cancelled successfully.",
                "reminder": reminder
            }

    return {
        "success": False,
        "message": "Reminder not found."
    }

if __name__ == "__main__":

    print(cancel_medication_reminder(1))
    print(list_medication_reminders())

