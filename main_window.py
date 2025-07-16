# infotainment_test_tool/gui/main_window.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import ast

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Infotainment Test Tool")

        # 🧱 Frame to hold test cases
        self.test_frame = ttk.LabelFrame(self.root, text="Test Scripts")
        self.test_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # 📤 Upload button
        self.upload_button = ttk.Button(self.root, text="Upload Test Script", command=self.upload_test_script)
        self.upload_button.pack(padx=10, pady=5)

        # Load test cases at startup
        self.load_test_cases()

    def load_test_cases(self):
        self.test_vars = {}

        # Clear existing widgets
        for widget in self.test_frame.winfo_children():
            widget.destroy()

        test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
        os.makedirs(test_dir, exist_ok=True)  # Ensure directory exists

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
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, file_name)
                shutil.copy(file_path, dest_path)

                self.load_test_cases()  # 🔄 Refresh GUI

            except Exception as e:
                messagebox.showerror("Upload Failed", f"Failed to upload script:\n{str(e)}")
