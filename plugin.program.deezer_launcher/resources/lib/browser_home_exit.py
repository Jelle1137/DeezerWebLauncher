import evdev
import sys
import subprocess
import logging
import os

# Set up logging
log_file_path = os.path.join(os.path.expanduser('~'), 'browser_home_exit.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

TARGET_DEVICE_NAME = "FiiO RM3 Consumer Control"
TARGET_KEYS = {"KEY_HOMEPAGE"}

def find_device_by_name(name):
    try:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.name == name:
                logging.info(f"Found device: {device.name} at {device.path}")
                return device
        logging.error(f"No input device named '{name}' found.")
    except Exception as e:
        logging.error(f"Error finding device: {e}")
    return None

def main():
    device = find_device_by_name(TARGET_DEVICE_NAME)
    if device is None:
        sys.exit(1)

    logging.info(f"Listening to device: {device.name} at {device.path}")
    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                key_event = evdev.categorize(event)
                if key_event.keycode in TARGET_KEYS and key_event.keystate == evdev.KeyEvent.key_down:
                    logging.info("Home button pressed! Exiting Browser...")
                    subprocess.call(['pkill', 'firefox'])  # Kill Firefox process
                    break
    except KeyboardInterrupt:
        logging.info("Watcher interrupted by user.")
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
