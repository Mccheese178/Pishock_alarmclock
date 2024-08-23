from datetime import datetime, timedelta
from time import sleep
from threading import Thread
from Pyshock import PishockAPI

#change these variables:
username = "" #Your username on the PiShock website
api_key = "" #Your api key from the PiShock website
share_code = "" #code that you want the alarm to use 
app_name = "" #What you want to name the app
test_mode = False  # Set to true if you want to bypass setting an alarm


# Do not change anything below or the code will not run properly
pishock = PishockAPI(api_key, username, share_code, app_name)
alarm_triggered = False

def periodic_vibration():
    while not alarm_triggered:
        pishock.vibrate(0, 1)
        sleep(120)

def get_user_input():
    if test_mode:
        intensity = int(input("Enter the action intensity, 1-100: "))
        shock_duration = int(input("Enter the action duration (in seconds, 1-15): "))
        alarm_time_str = None
    else:
        alarm_time_str = input("Enter the alarm time (in 24 hour HH:MM format): ")
        intensity = int(input("Enter the action intensity 1-100: "))
        shock_duration = int(input("Enter the action duration (in seconds, 1-15): "))

    return alarm_time_str, intensity, shock_duration

def calculate_time_until_alarm(alarm_time_str):
    now = datetime.now()
    alarm_time = datetime.strptime(alarm_time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)

    if alarm_time < now:
        alarm_time += timedelta(days=1)

    time_until_alarm = (alarm_time - now).total_seconds()
    return time_until_alarm, alarm_time

def execute_action(action, intensity, duration):
    global alarm_triggered
    if action == 's':
        pishock.shock(intensity, duration)
        print("\nShock delivered!")
    elif action == 'v':
        pishock.vibrate(intensity, duration)
        print("\nVibration delivered!")
    alarm_triggered = True

def check_for_time_left(alarm_time):
    while not alarm_triggered:
        user_input = input("Type 'time left' to check the remaining time: ").strip().lower()
        if user_input == 'time left':
            now = datetime.now()
            remaining_time = (alarm_time - now).total_seconds()
            print(f"Time remaining: {int(remaining_time)} seconds.")

def execute_shock():
    global alarm_triggered
    alarm_time_str, intensity, duration = get_user_input()

    print(f"Intensity set to {intensity}")
    print(f"Duration set to {duration}")

    action = input("Would you like to Shock or Vibrate? (s for shock, v for vibrate): ").strip().lower()

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
        print(f"Alarm is set for {alarm_time.strftime('%H:%M')}.")

        vibration_thread = Thread(target=periodic_vibration)
        vibration_thread.start()

        time_thread = Thread(target=check_for_time_left, args=(alarm_time,))
        time_thread.start()

        sleep(time_until_alarm)

        execute_action(action, intensity, duration)
        alarm_triggered = True

        vibration_thread.join()

if __name__ == "__main__":
    execute_shock()
