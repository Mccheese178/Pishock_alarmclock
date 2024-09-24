from datetime import datetime, timedelta
from time import sleep
from threading import Thread
from Pyshock import PishockAPI
import random
import os
import sys

# Change these variables:
username = "" # Your username on the PiShock website
api_key = "" # Your api key from the PiShock website
share_code = "" # Code that you want the alarm to use 
app_name = "" # What you want to name the app
test_mode = False  # Set to 'True' if you want to bypass setting an alarm
snooze_duration = "" # Set in minutes how long you want a snooze. If you don't want a snooze, set to '0'

# DO NOT CHANGE ANYTHING BELOW OR THE CODE WILL NOT RUN PROPERLY
pishock = PishockAPI(api_key, username, share_code, app_name)
alarm_triggered = False
alarm_file = "alarm_time.txt"

def periodic_vibration():
    while not alarm_triggered:
        pishock.vibrate(0, 0)
        sleep(120)

def save_alarm_time(alarm_time_str):
    with open(alarm_file, "w") as file:
        file.write(alarm_time_str)

def load_alarm_time():
    if os.path.exists(alarm_file):
        with open(alarm_file, "r") as file:
            return file.read().strip()
    return None

def get_user_input():
    if test_mode:
        intensity = int(input("Enter action intensity (1-100): "))
        shock_duration = int(input("Enter action duration (in seconds, 1-15): "))
        return None, intensity, shock_duration
    else:
        alarm_time_str = input("Enter alarm time (24-hour HH:MM format): ")
        intensity = input("Enter action intensity (1-100 or 'r' for random, '0' for beep): ")
        if intensity == 'r':
            intensity = random.randint(1, 100)
        else:
            intensity = int(intensity)
        shock_duration = int(input("Enter action duration (in seconds, 1-15): "))
        return alarm_time_str, intensity, shock_duration

def calculate_time_until_alarm(alarm_time_str):
    now = datetime.now()
    alarm_time = datetime.strptime(alarm_time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
    if alarm_time < now:
        alarm_time += timedelta(days=1)
    return (alarm_time - now).total_seconds(), alarm_time

def execute_action(action, intensity, duration):
    global alarm_triggered
    if action == 's':
        pishock.shock(intensity, duration)
        print("\nShock delivered!")
    elif action == 'v':
        pishock.vibrate(intensity, duration)
        print("\nVibration delivered!")
    elif action == 'b':
        pishock.beep(duration)
        print("\nBeep sounded!")
    alarm_triggered = True

def check_for_time_left(remaining_seconds):
    while remaining_seconds > 0 and not alarm_triggered:
        sleep(60)
        remaining_seconds -= 60
        if remaining_seconds > 0:
            hours = int(remaining_seconds // 3600)
            minutes = int((remaining_seconds % 3600) // 60)
            seconds = int(remaining_seconds % 60)
            print(f"Time remaining: {hours} hours, {minutes} minutes, and {seconds} seconds.")

def snooze_alarm(action, intensity, duration):
    global alarm_triggered
    alarm_triggered = False
    print(f"Snoozing for {snooze_duration} minutes...")
    
    snooze_seconds = snooze_duration * 60
    time_thread = Thread(target=check_for_time_left, args=(snooze_seconds,))
    time_thread.start()
    vibration_thread = Thread(target=periodic_vibration)
    vibration_thread.start()

    sleep(snooze_seconds)
    execute_action(action, intensity, duration)
    time_thread.join()
    vibration_thread.join()

def execute_shock():
    global alarm_triggered

    saved_alarm_time = load_alarm_time()
    if saved_alarm_time:
        use_saved = input(f"Saved alarm time found ({saved_alarm_time}). Use this time? (y/n): ").strip().lower()
        if use_saved == 'y':
            alarm_time_str = saved_alarm_time
            intensity = input("Enter action intensity (1-100 or 'r' for random, '0' for beep): ")
            if intensity == 'r':
                intensity = random.randint(1, 100)
            else:
                intensity = int(intensity)
            duration = int(input("Enter action duration (in seconds, 1-15): "))
        else:
            alarm_time_str, intensity, duration = get_user_input()
    else:
        alarm_time_str, intensity, duration = get_user_input()

    print(f"Intensity set to {intensity}")
    print(f"Duration set to {duration}")

    action = input("Would you like to Shock or Vibrate? (s for shock, v for vibrate, b for beep): ").strip().lower()

    if test_mode:
        print("Test mode activated.")
        while True:
            execute_action(action, intensity, duration)
            sleep(duration)
            repeat = input("Repeat the action? (y/n): ").strip().lower()
            if repeat != 'y':
                break
    else:
        time_until_alarm, alarm_time = calculate_time_until_alarm(alarm_time_str)

        save_alarm = input("Would you like to save this alarm time for future use? (y/n): ").strip().lower()
        if save_alarm == 'y':
            save_alarm_time(alarm_time_str)
            print("Alarm time saved.")

        print(f"Alarm is set for {alarm_time.strftime('%H:%M')}.")
        
        vibration_thread = Thread(target=periodic_vibration)
        vibration_thread.start()

        time_thread = Thread(target=check_for_time_left, args=(time_until_alarm,))
        time_thread.start()

        sleep(time_until_alarm)

        execute_action(action, intensity, duration)

        alarm_triggered = True
        vibration_thread.join(timeout=1)
        time_thread.join(timeout=1)

        if snooze_duration > 0:
            snooze = input("\nWould you like to snooze the alarm? (y/n): ").strip().lower()
            if snooze == 'y':
                snooze_alarm(action, intensity, duration)
            else:
                print("\nAlarm stopped.")
                print("\nExiting code now...")
                sys.exit()
        else:
            sys.exit()

if __name__ == "__main__":
    execute_shock()
