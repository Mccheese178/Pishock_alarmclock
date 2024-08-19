import requests
import json
from typing import Dict

# Constants
PISHOCK_URL = "https://do.pishock.com/api/apioperate/"

# Error messages
ERROR_MESSAGES = {
    "This code doesn't exist.": "The specified share code could not be found. Make sure you create and copy an active share code from the PiShock website.",
    "Not Authorized.": "The specified username or apikey is not correct (or your account has not been activated).",
    "Shocker is Paused, unable to send command.": "The shocker is paused (from the PiShock.com web panel).",
    "Device currently not connected.": "The PiShock is offline.",
    "This share code has already been used by somebody else.": "Someone (or something) else is using the specified share code. Generate a new one.",
    "Unknown Op, use 0 for shock, 1 for vibrate and 2 for beep.": "Invalid Op code specified. Must be 0, 1, or 2.",
    "Intensity must be between 0 and 100": "The specified intensity was outside the permitted range.",
    "Duration must be between 0 and 15": "The specified duration was outside the permitted range."
}


class PishockAPI(object):
    def __init__(self, api_key: str, username: str, sharecode: str, app_name: str):
        self.api_key: str = api_key
        self.username: str = username
        self.app_name: str = app_name
        self.sharecode: str = sharecode
        self.base_url: str = PISHOCK_URL
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "User-Agent": "PishockPy/0.0.4"
        }

    def _check_response(self, response: requests.Response) -> None:
        """Check if a response from the server is valid.
        If the response is not valid, raise an exception."""
        if response.status_code != 200:
            raise ValueError(f"Invalid response from server: {response.text}")
        if response.text == "Operation Succeeded.":
            return
        if response.text in ERROR_MESSAGES:
            raise ValueError(ERROR_MESSAGES[response.text])

    def _send_request(self, data: Dict[str, str]) -> None:
        """Send a request to the PiShock API."""
        response = requests.post(
            self.base_url,
            headers=self.headers,
            data=json.dumps(data)
        )
        self._check_response(response)

    def shock(self, intensity: float, duration: int) -> None:
        """Shock the user with the specified intensity and duration.
        Intensity must be between 0 and 1, duration must be between 0 and 15 (or 300 for 0.5 seconds)."""
        # Sanity checks
        if not 0 <= intensity <= 1:
            raise ValueError("Intensity must be between 0 and 1")
        if not 0 <= duration <= 15 and duration != 300:
            raise ValueError("Duration must be between 0 and 15")
        # Convert intensity to a percentage
        intensity = int(intensity * 100)
        data = {
            "Username": self.username,
            "Name": self.app_name,
            "Code": self.sharecode,
            "Intensity": intensity,
            "Duration": duration,
            "Apikey": self.api_key,
            "Op": "0"
        }
        self._send_request(data)

    def minishock(self, intensity: float) -> None:
        """A shortcut for a 0.5 second shock at the specified intensity."""
        self.shock(intensity, 300)

    def vibrate(self, intensity: float, duration: int) -> None:
        """Vibrate the user with the specified intensity and duration.
        Intensity must be between 0 and 1, duration must be between 0 and 15."""
        # Sanity checks
        if not 0 <= intensity <= 1:
            raise ValueError("Intensity must be between 0 and 1")
        if not 0 <= duration <= 15:
            raise ValueError("Duration must be between 0 and 15")
        # Convert intensity to a percentage
        intensity = int(intensity * 100)
        data = {
            "Username": self.username,
            "Name": self.app_name,
            "Code": self.sharecode,
            "Intensity": intensity,
            "Duration": duration,
            "Apikey": self.api_key,
            "Op": "1"
        }
        self._send_request(data)

    def beep(self, duration: int) -> None:
        """Beep the user for the specified duration.
        Duration must be between 0 and 15."""
        if not 0 <= duration <= 15:
            raise ValueError("Duration must be between 0 and 15")
        data = {
            "Username": self.username,
            "Name": self.app_name,
            "Code": self.sharecode,
            "Duration": duration,
            "Apikey": self.api_key,
            "Op": "2"
        }
        self._send_request(data)