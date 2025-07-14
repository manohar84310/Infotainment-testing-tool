# infotainment_test_tool/gui/main_window.py

from core.result_manager import ResultManager
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from core.test_runner import TestRunner
import os
import shutil
import ast

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Infotainment Test Automation Tool")
        self.root.geometry("900x750")

        self.result_manager = ResultManager()
        self.last_run_results = []

        title_label = ttk.Label(self.root, text="Infotainment Test Runner", font=("Arial", 16))
        title_label.pack(pady=10)

        self.test_frame = ttk.LabelFrame(self.root, text="Available Test Cases")
        self.test_frame.pack(fill="x", padx=10, pady=10)

        self.test_vars = {}
        self.load_test_cases()

        upload_button = ttk.Button(self.root, text="📤 Upload Test Script", command=self.upload_test_script)
        upload_button.pack(pady=5)

        run_button = ttk.Button(self.root, text="Run Selected Tests", command=self.run_selected_tests)
        run_button.pack(pady=5)

        export_button = ttk.Button(self.root, text="Export CSV Report", command=self.export_results)
        export_button.pack(pady=5)

        clear_button = ttk.Button(self.root, text="Clear Output", command=self.clear_output)
        clear_button.pack(pady=5)

        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=5)
        ttk.Button(filter_frame, text="Show All", command=self.show_all_results).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Show Only PASS", command=lambda: self.filter_results("PASS")).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Show Only FAIL", command=lambda: self.filter_results("FAIL")).pack(side="left", padx=5)

        log_frame = ttk.Frame(self.root)
        log_frame.pack(pady=5)
        ttk.Label(log_frame, text="View Saved Logs:").pack(side="left")
        self.log_var = tk.StringVar()
        self.log_dropdown = ttk.Combobox(log_frame, textvariable=self.log_var, width=60, state="readonly")
        self.log_dropdown.pack(side="left", padx=5)
        self.log_dropdown.bind("<<ComboboxSelected>>", self.load_selected_log)
        self.refresh_log_dropdown()

        self.output_box = tk.Text(self.root, height=10, width=110, wrap="word")
        self.output_box.pack(padx=10, pady=10)

        self.table = ttk.Treeview(self.root, columns=("Test", "Status", "Log"), show="headings")
        self.table.heading("Test", text="Test Case")
        self.table.heading("Status", text="Status")
        self.table.heading("Log", text="Log File")
        self.table.pack(padx=10, pady=10, fill="x")

    def load_test_cases(self):
        self.test_vars = {}
        for widget in self.test_frame.winfo_children():
            widget.destroy()

        test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
        test_files = [f[:-3] for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")]

        for test_name in sorted(test_files):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(self.test_frame, text=test_name, variable=var)
            cb.pack(anchor="w", padx=10, pady=2)
            self.test_vars[test_name] = var

    def upload_test_script(self):
        file_path = filedialog.askopenfilename(title="Select Test Script", filetypes=[("Python files", "*.py")])
        if file_path:
            try:
                file_name = os.path.basename(file_path)
                if not file_name.startswith("test_") or not file_name.endswith(".py"):
                    messagebox.showwarning("Invalid File", "Test script must start with 'test_' and end with '.py'")
                    return

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                try:
                    parsed = ast.parse(content)
                except SyntaxError as e:
                    messagebox.showerror("Syntax Error", f"Syntax error in script on line {e.lineno}: {e.msg}")
                    return

                has_run = any(isinstance(node, ast.FunctionDef) and node.name == "run" for node in parsed.body)
                if not has_run:
                    messagebox.showerror("Missing Function", "The script must contain a 'run()' function.")
                    return

                dest_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
                dest_path = os.path.join(dest_dir, file_name)
                shutil.copy(file_path, dest_path)
                self.load_test_cases()

            except Exception as e:
                messagebox.showerror("Upload Failed", f"Failed to upload script:\n{str(e)}")
