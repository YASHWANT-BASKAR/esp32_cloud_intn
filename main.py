import subprocess
import re
import time
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

def get_wifi_signal():
    """
    Runs 'netsh wlan show interfaces' command and extracts Wi-Fi signal strength.
    Returns: dict {"timestamp": "..", "signal_strength": ..} or {"error": ".."}
    """
    try:
        # Run the netsh command to get Wi-Fi signal strength
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)

        # Extract the Signal Strength
        match = re.search(r"Signal\s*:\s*(\d+)%", result.stdout)
        if match:
            signal_strength = int(match.group(1))
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return {"timestamp": timestamp, "signal_strength": signal_strength}

        return {"error": "Wi-Fi signal strength not found"}

    except Exception as e:
        return {"error": str(e)}

@app.get("/wifi-signal")
def wifi_signal():
    """
    API endpoint to get the current Wi-Fi signal strength.
    Example usage: GET request to /wifi-signal
    """
    return get_wifi_signal()


