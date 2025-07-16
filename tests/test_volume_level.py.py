import subprocess

def run():
    result = subprocess.run(['adb', 'shell', 'media volume --get'], capture_output=True, text=True)
    return "volume is 0" not in result.stdout.lower()
