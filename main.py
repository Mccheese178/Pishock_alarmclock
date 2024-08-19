from datetime import datetime, timedelta
from time import sleep
from Pyshock import PishockAPI


#change these variable:
username = "" #Your username on the PiShock website
api_key = "" #Your api key from the PiShock website
share_code = "" #code that you want the alarm to use 
app_name = "" #What you want to name the app

pishock = PishockAPI(api_key, username, share_code, app_name)

test_mode = False

def get_user_input():
    alarm_time_str = input("Enter the alarm time (in 24 hour HH:MM format): ")
    intensity = int(input("Enter the shock intensity, 1-100: "))
    shockduration = int(input("Enter the shock duration (in seconds, 1-15): "))
    return alarm_time_str, intensity, shockduration

def calculate_time_until_alarm(alarm_time_str):
    now = datetime.now()
    alarm_time = datetime.strptime(alarm_time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)

    if alarm_time < now:
        alarm_time += timedelta(days=1)

    time_until_alarm = (alarm_time - now).total_seconds()
    return time_until_alarm, alarm_time.strftime("%H:%M")

def execute_shock():
    alarm_time_str, shock_intensity, shock_duration = get_user_input()
    
    time_until_alarm, formatted_alarm_time = calculate_time_until_alarm(alarm_time_str)
    
    print(f"Alarm is set for {formatted_alarm_time}.")
    print(f"Shock intensity set to {shock_intensity}")
    print(f"Shock duration set to {shock_duration}")
    
    if test_mode:
        print("Test mode activated, sending shock now.")
    else:
        print(f"Waiting for {int(time_until_alarm)} seconds until the alarm goes off.")
        sleep(time_until_alarm)
    
    pishock.shock(shock_intensity, shock_duration)
    print("What a shocking suprise! Shock delivered!")
    

if __name__ == "__main__":
    execute_shock()
