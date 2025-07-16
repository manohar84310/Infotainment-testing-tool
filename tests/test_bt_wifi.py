"""
Example infotainment‑head‑unit test suite.

Each function’s name starts with “run”, so your modified
runner will discover and execute them all automatically.
Return True  ➜ PASS
Return False ➜ FAIL
Raise Exception ➜ FAIL (with traceback in log)
"""

import time
import random


def _simulated_step(desc, seconds=1):
    """Tiny helper to mimic test steps with log output."""
    print(f"[STEP] {desc} ({seconds}s)")
    time.sleep(seconds)


# 1. --------------------------------------------------------------------------
def run_boot():
    """Verify that the unit boots within 10 s."""
    _simulated_step("Power ON", 2)
    boot_time = random.uniform(5, 12)  # pretend we measured it
    print(f"Measured boot time: {boot_time:.1f}s")
    return boot_time <= 10


# 2. --------------------------------------------------------------------------
def run_bluetooth_pairing():
    """Pair a phone over Bluetooth and check connection status."""
    _simulated_step("Enable Bluetooth")
    _simulated_step("Search for device", 2)
    paired = random.choice([True, True, False])  # 66 % pass rate
    print(f"Pairing result: {'success' if paired else 'failure'}")
    return paired


# 3. --------------------------------------------------------------------------
def run_media_playback():
    """Start media playback and verify audio is routed."""
    _simulated_step("Start playback")
    audio_ok = random.choice([True, True, True, False])  # 75 % pass rate
    print(f"Audio routed: {audio_ok}")
    return audio_ok


# 4. --------------------------------------------------------------------------
def run_navigation_route():
    """Calculate a navigation route and ensure guidance starts."""
    _simulated_step("Enter destination", 1)
    _simulated_step("Calculate route", 2)
    guidance_started = True  # always passes in this demo
    print("Guidance started:", guidance_started)
    return guidance_started


# 5. --------------------------------------------------------------------------
def run_shutdown():
    """Verify that the unit powers off gracefully."""
    _simulated_step("Power OFF", 2)
    shutdown_clean = True
    print("Shutdown clean:", shutdown_clean)
    return shutdown_clean
