import subprocess

def run():
    result = subprocess.run(['adb', 'shell', 'settings get global airplane_mode_on'], capture_output=True, text=True)
    return result.stdout.strip() == "0"
