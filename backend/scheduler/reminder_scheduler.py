import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from tools.medicine_reminder import load_reminders


def check_reminders():
    now = datetime.now().strftime("%H:%M")

    reminders = load_reminders()

    for reminder in reminders:
        if reminder["status"] != "active":
            continue

        if reminder["time"] == now:
            print(
                f"\n MEDICATION REMINDER: "
                f"Time to take {reminder['medicine']}!"
            )


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        check_reminders,
        "interval",
        minutes=1
    )

    scheduler.start()

    print("Medication reminder scheduler started.")

    try:
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        scheduler.shutdown()
        print("Scheduler stopped.")


if __name__ == "__main__":
    start_scheduler()