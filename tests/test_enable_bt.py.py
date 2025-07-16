import subprocess
import time

def run():
    try:
        subprocess.run(
            ['adb', 'shell', 'service call bluetooth_manager 6'],
            check=True
        )
        time.sleep(2)

        result = subprocess.run(
            ['adb', 'shell', 'dumpsys', 'bluetooth_manager'],
            capture_output=True, text=True
        )

        return "enabled: true" in result.stdout.lower()

    except Exception as e:
        print(f"Bluetooth test failed: {e}")
        return False
