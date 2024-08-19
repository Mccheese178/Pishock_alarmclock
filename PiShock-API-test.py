from datetime import datetime, timedelta
from time import sleep
from Pyshock import PishockAPI

username = "Mccheese178"
api_key = "c47f4806-62e4-4b7f-8e55-c23276001aa4"
share_code = "2DDE5C40490"
app_name = "Test-bot"

pishock = PishockAPI(api_key, username, share_code, app_name)

def get_user_input():
    alarm_time_str = input("Enter the alarm time (in HH:MM format): ")
    intensity = float(input("Enter the shock intensity, .01 being 1% and 1 being 100%: "))
    shockduration = int(input("Enter the shock duration (in seconds, 1-15): "))
    return alarm_time_str, intensity, shockduration

def calculate_time_until_alarm(alarm_time_str):
    now = datetime.now()
    alarm_time = datetime.strptime(alarm_time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)

    if alarm_time < now:
        alarm_time += timedelta(days=1)

    return (alarm_time - now).total_seconds()

def execute_shock():
    alarm_time_str, shock_intensity, shock_duration = get_user_input()
    
    time_until_alarm = calculate_time_until_alarm(alarm_time_str)
    
    print(f"Alarm is set for {alarm_time_str}.")
    print(f"Waiting for {int(time_until_alarm)} seconds until the alarm goes off.")
    
    sleep(time_until_alarm)
    
    pishock.shock(shock_intensity, shock_duration)
    print("Shock delivered!")

if __name__ == "__main__":
    execute_shock()
