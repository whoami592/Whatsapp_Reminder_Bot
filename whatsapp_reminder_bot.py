import pywhatkit
import schedule
import time
import json
import pyfiglet
from datetime import datetime
import os

# Print stylish banner
banner = pyfiglet.figlet_format("Daily Reminder Bot", font="slant")
print(banner)
print("Coded by Pakistani Ethical Hacker Mr Sabaz Ali Khan 2025\n")

# File to store reminders
REMINDER_FILE = "reminders.json"

# Load existing reminders
def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, 'r') as file:
            return json.load(file)
    return []

# Save reminders to file
def save_reminders(reminders):
    with open(REMINDER_FILE, 'w') as file:
        json.dump(reminders, file, indent=4)

# Send WhatsApp message
def send_whatsapp_message(phone_number, message, hour, minute):
    try:
        pywhatkit.sendwhatmsg(phone_number, message, hour, minute)
        print(f"Message scheduled for {phone_number} at {hour}:{minute} - {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Schedule a daily reminder
def schedule_reminder(phone_number, message, time_str):
    reminders = load_reminders()
    reminders.append({
        "phone_number": phone_number,
        "message": message,
        "time": time_str
    })
    save_reminders(reminders)
    
    schedule.every().day.at(time_str).do(
        send_whatsapp_message, phone_number=phone_number, message=message,
        hour=int(time_str.split(":")[0]), minute=int(time_str.split(":")[1])
    )
    print(f"Reminder set for {phone_number} at {time_str}: {message}")

# Load saved reminders on startup
def load_saved_reminders():
    reminders = load_reminders()
    for reminder in reminders:
        schedule.every().day.at(reminder["time"]).do(
            send_whatsapp_message,
            phone_number=reminder["phone_number"],
            message=reminder["message"],
            hour=int(reminder["time"].split(":")[0]),
            minute=int(reminder["time"].split(":")[1])
        )
        print(f"Loaded reminder for {reminder['phone_number']} at {reminder['time']}")

# Main function
def main():
    load_saved_reminders()
    
    while True:
        print("\n1. Add new reminder")
        print("2. Exit")
        choice = input("Enter choice (1/2): ")
        
        if choice == "1":
            phone_number = input("Enter phone number (with country code, e.g., +923001234567): ")
            message = input("Enter reminder message: ")
            time_str = input("Enter time for reminder (HH:MM, 24-hour format): ")
            
            try:
                datetime.strptime(time_str, "%H:%M")  # Validate time format
                schedule_reminder(phone_number, message, time_str)
            except ValueError:
                print("Invalid time format! Use HH:MM (e.g., 14:30)")
        
        elif choice == "2":
            print("Exiting bot...")
            break
        
        else:
            print("Invalid choice! Try again.")
        
        # Run scheduled tasks
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()