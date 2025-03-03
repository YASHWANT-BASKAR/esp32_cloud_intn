import subprocess
import re
import time
import csv
from datetime import datetime

# File name for CSV
csv_filename = "wifi_signal_log.csv"

# Create and open CSV file for writing (add header if new)
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Wi-Fi Signal Strength (%)"])  # CSV Header

def log_wifi_signal():
    print(f"Logging Wi-Fi Signal Strength to {csv_filename}... Press Ctrl+C to stop.\n")

    while True:
        try:
            # Run the netsh command to get Wi-Fi signal strength
            result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
            
            # Extract the Signal Strength
            match = re.search(r"Signal\s*:\s*(\d+)%", result.stdout)
            if match:
                signal_strength = int(match.group(1))
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Save to CSV
                with open(csv_filename, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, signal_strength])
                
                # Print real-time output
                print(f"{timestamp} - Wi-Fi Signal Strength: {signal_strength}%   ", end="\r", flush=True)
            else:
                print("Wi-Fi signal strength not found.         ", end="\r", flush=True)

            time.sleep(1)  # Update every 1 second

        except KeyboardInterrupt:
            print(f"\nLogging stopped. Data saved in {csv_filename}.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

# Start logging
log_wifi_signal()

