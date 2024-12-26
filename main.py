from PIL import ImageGrab
from apscheduler.schedulers.blocking import BlockingScheduler
import os
from datetime import datetime
import configparser

# Read settings from the configuration file
config = configparser.ConfigParser()
config.read("settings.ini")

save_directory = config["Settings"]["save_directory"]
filename = config["Settings"]["filename"]
interval_seconds = int(config["Settings"]["interval_seconds"])


def capture_and_save_screenshot():
    # Ensure the server drive path exists
    if not os.path.exists(save_directory):
        raise Exception(
            f"The path {save_directory} does not exist or cannot be accessed."
        )

    # Capture the screenshot using ImageGrab
    screenshot = ImageGrab.grab()

    # Construct the full path to save the screenshot
    file_path = os.path.join(save_directory, filename)

    # Save the screenshot to the server drive
    screenshot.save(file_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"Screenshot saved to {file_path} at {timestamp}")


# Create an instance of the scheduler
scheduler = BlockingScheduler()

# Schedule the job
# Schedule the job to run every xx seconds
scheduler.add_job(capture_and_save_screenshot, "interval", seconds=interval_seconds)

try:
    print("Starting scheduler...")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped.")
