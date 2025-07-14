# infotainment_test_tool/core/result_manager.py

import os
import csv
from datetime import datetime

REPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports"))
os.makedirs(REPORT_DIR, exist_ok=True)

class ResultManager:
    def __init__(self):
        self.results = []

    def add_result(self, test_name, status, log_path):
        self.results.append({
            "Test Case": test_name,
            "Status": status,
            "Log File": log_path
        })

    def export_to_csv(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.csv"
        filepath = os.path.join(REPORT_DIR, filename)

        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Test Case", "Status", "Log File"])
            writer.writeheader()
            writer.writerows(self.results)

        return filepath
