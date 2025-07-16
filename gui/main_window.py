# infotainment_test_tool/gui/main_window.py

from core.result_manager import ResultManager
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from core.test_runner import TestRunner
import importlib
import inspect
import io
import contextlib
import traceback
import os
import shutil
import ast
import time
import smtplib
from email.message import EmailMessage

# class MainWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Infotainment Test Automation Tool")
#         self.root.geometry("900x800")

#         self.result_manager = ResultManager()
#         self.last_run_results = []

#         title_label = ttk.Label(self.root, text="Infotainment Test Runner", font=("Arial", 16))
#         title_label.pack(pady=10)

#         self.test_frame = ttk.LabelFrame(self.root, text="Available Test Cases")
#         self.test_frame.pack(fill="x", padx=10, pady=10)

#         self.test_vars = {}
#         self.load_test_cases()

#         button_frame = ttk.Frame(self.root)
#         button_frame.pack(pady=10)

#         remove_button = ttk.Button(button_frame, text="🗑️ Remove Selected", command=self.remove_selected_tests)
#         remove_button.pack(side="left", padx=5)


#         clear_selection_button = ttk.Button(button_frame, text="❎ Clear Selection", command=self.clear_test_selection)
#         clear_selection_button.pack(side="left", padx=5)


#         upload_button = ttk.Button(button_frame, text="📤 Upload Test Script", command=self.upload_test_script)
#         upload_button.pack(side="left", padx=5)

#         run_button = ttk.Button(button_frame, text="▶️ Run Selected Tests", command=self.run_selected_tests)
#         run_button.pack(side="left", padx=5)


#         export_button = ttk.Button(button_frame, text="💾 Export CSV Report", command=self.export_results)
#         export_button.pack(side="left", padx=5)

#         clear_button = ttk.Button(button_frame, text="🧹 Clear Output", command=self.clear_output)
#         clear_button.pack(side="left", padx=5)

#         save_logs_button = ttk.Button(button_frame, text="💾 Save Logs", command=self.save_logs)
#         save_logs_button.pack(side="left", padx=5)

#         pie_button = ttk.Button(button_frame, text="📊 Show Pass/Fail Pie",
#                         command=self.show_pass_fail_pie)
#         pie_button.pack(side="left", padx=5)



#         email_frame = ttk.LabelFrame(self.root, text="📧 Email Report")
#         email_frame.pack(pady=10, fill="x")

#         ttk.Label(email_frame, text="Recipient Email:").pack(side="left", padx=5)
#         self.email_entry = ttk.Entry(email_frame, width=40)
#         self.email_entry.pack(side="left", padx=5)
#         send_button = ttk.Button(email_frame, text="Send CSV Report", command=self.send_email_report)
#         send_button.pack(side="left", padx=5)

#         filter_frame = ttk.Frame(self.root)
#         filter_frame.pack(pady=5)
#         ttk.Button(filter_frame, text="Show All", command=self.show_all_results).pack(side="left", padx=5)
#         ttk.Button(filter_frame, text="Show Only PASS", command=lambda: self.filter_results("PASS")).pack(side="left", padx=5)
#         ttk.Button(filter_frame, text="Show Only FAIL", command=lambda: self.filter_results("FAIL")).pack(side="left", padx=5)

#         log_frame = ttk.Frame(self.root)
#         log_frame.pack(pady=5)
#         ttk.Label(log_frame, text="View Saved Logs:").pack(side="left")
#         self.log_var = tk.StringVar()
#         self.log_dropdown = ttk.Combobox(log_frame, textvariable=self.log_var, width=60, state="readonly")
#         self.log_dropdown.pack(side="left", padx=5)
#         self.log_dropdown.bind("<<ComboboxSelected>>", self.load_selected_log)
#         self.refresh_log_dropdown()

#         self.output_box = tk.Text(self.root, height=10, width=110, wrap="word")
#         self.output_box.pack(padx=10, pady=10)

#         self.table = ttk.Treeview(self.root, columns=("Test", "Status", "Log"), show="headings")
#         self.table.heading("Test", text="Test Case")
#         self.table.heading("Status", text="Status")
#         self.table.heading("Log", text="Log File")
#         self.table.pack(padx=10, pady=10, fill="x")


#     def load_test_cases(self):
#         self.test_vars = {}
#         for widget in self.test_frame.winfo_children():
#             widget.destroy()

#         test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
#         if not os.path.exists(test_dir):
#             os.makedirs(test_dir)
#         test_files = [f[:-3] for f in os.listdir(test_dir)
#                       if f.startswith("test_") and f.endswith(".py")]

#         for test_name in sorted(test_files):
#             var = tk.BooleanVar()
#             cb = ttk.Checkbutton(self.test_frame, text=test_name, variable=var)
#             cb.pack(anchor="w", padx=10, pady=2)
#             self.test_vars[test_name] = var




    # infotainment_test_tool/gui/main_window.py

# from core.result_manager import ResultManager
# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from core.test_runner import TestRunner
# import os
# import ast
# import time

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Infotainment Test Automation Tool")
        self.root.geometry("1000x850")

        self.result_manager = ResultManager()
        self.last_run_results = []

        # Title
        title_label = ttk.Label(self.root, text="Infotainment Test Runner", font=("Arial", 16))
        title_label.pack(pady=10)

        # Test case area
        self.test_frame = ttk.LabelFrame(self.root, text="Available Test Cases")
        self.test_frame.pack(fill="x", padx=10, pady=10)

        self.test_vars = {}

        # Row of action buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="📤 Upload Test Script", command=self.upload_test_script).pack(side="left", padx=5)
        ttk.Button(button_frame, text="▶️ Run Selected Tests", command=self.run_selected_tests).pack(side="left", padx=5)
        ttk.Button(button_frame, text="💾 Export CSV Report", command=self.export_results).pack(side="left", padx=5)
        ttk.Button(button_frame, text="🧹 Clear Output", command=self.clear_output).pack(side="left", padx=5)
        ttk.Button(button_frame, text="📁 Save Logs", command=self.save_logs).pack(side="left", padx=5)
        ttk.Button(button_frame, text="📊 Dashboard", command=self.show_dashboard).pack(side="left", padx=5)

        # Email section
        email_frame = ttk.LabelFrame(self.root, text="📧 Email Report")
        email_frame.pack(pady=10, fill="x")

        ttk.Label(email_frame, text="Recipient Email:").pack(side="left", padx=5)
        self.email_entry = ttk.Entry(email_frame, width=40)
        self.email_entry.pack(side="left", padx=5)
        ttk.Button(email_frame, text="Send CSV Report", command=self.send_email_report).pack(side="left", padx=5)

        # Filter section
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=5)

        ttk.Button(filter_frame, text="📋 Show All", command=self.show_all_results).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="✅ Show Only PASS", command=lambda: self.filter_results("PASS")).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="❌ Show Only FAIL", command=lambda: self.filter_results("FAIL")).pack(side="left", padx=5)
        
        # 📁 View Saved Logs Dropdown
        log_frame = ttk.Frame(self.root)
        log_frame.pack(pady=5)

        ttk.Label(log_frame, text="View Saved Logs:").pack(side="left")
        self.log_var = tk.StringVar()
        self.log_dropdown = ttk.Combobox(log_frame, textvariable=self.log_var, width=60, state="readonly")
        self.log_dropdown.pack(side="left", padx=5)
        self.log_dropdown.bind("<<ComboboxSelected>>", self.load_selected_log)

        self.refresh_log_dropdown()


        # Output area
        self.output_box = tk.Text(self.root, height=12, width=115, wrap="word")
        self.output_box.pack(padx=10, pady=10)

        # Table
        self.table = ttk.Treeview(self.root, columns=("Test", "Status", "Log"), show="headings")
        self.table.heading("Test", text="Test Case")
        self.table.heading("Status", text="Status")
        self.table.heading("Log", text="Log File")
        self.table.pack(padx=10, pady=10, fill="x")

    def upload_test_script(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Test Scripts",
            filetypes=[("Python files", "*.py")]
        )
        if not file_paths:
            return

        uploaded = skipped = 0

        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            try:
                if not (file_name.startswith("test_") and file_name.endswith(".py")):
                    skipped += 1
                    continue

                with open(file_path, "r", encoding="utf-8") as f:
                    source = f.read()

                try:
                    parsed = ast.parse(source)
                except SyntaxError as e:
                    skipped += 1
                    messagebox.showerror(
                        "Syntax Error",
                        f"'{file_name}' skipped – line {e.lineno}: {e.msg}"
                    )
                    continue

                has_run = any(
                    isinstance(node, ast.FunctionDef) and node.name.startswith("run")
                    for node in ast.walk(parsed)
                )
                if not has_run:
                    skipped += 1
                    messagebox.showwarning(
                        "No run() found",
                        f"'{file_name}' skipped – it has no function starting with 'run'."
                    )
                    continue

                display_name = file_name[:-3]
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(self.test_frame, text=display_name, variable=var)
                cb.pack(anchor="w", padx=10, pady=2)

                self.test_vars[display_name] = {
                    "selected": var,
                    "path": file_path
                }

                uploaded += 1

            except Exception as e:
                skipped += 1
                messagebox.showerror("Upload Failed", f"Failed to upload '{file_name}':\n{e}")

        messagebox.showinfo("Upload Summary", f"✅ Uploaded: {uploaded}\n⛔ Skipped: {skipped}")

    def run_selected_tests(self):
        selected = [name for name, meta in self.test_vars.items() if meta["selected"].get()]
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one test case.")
            return

        self.output_box.delete(1.0, tk.END)
        self.table.delete(*self.table.get_children())
        self.last_run_results.clear()

        for test_name in selected:
            file_path = self.test_vars[test_name]["path"]
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()

                namespace = {}
                exec(code, namespace)

                run_functions = [fn for fn in namespace if fn.startswith("run") and callable(namespace[fn])]
                if not run_functions:
                    raise Exception("No run_*() functions found.")

                combined_output = []
                passed = True

                for fn in run_functions:
                    try:
                        result = namespace[fn]()
                        msg = f"{fn}() => {'PASS' if result else 'FAIL'}"
                        combined_output.append(msg)
                        if not result:
                            passed = False
                    except Exception as inner_e:
                        combined_output.append(f"{fn}() => ERROR: {inner_e}")
                        passed = False

                status = "PASS" if passed else "FAIL"
                output_text = "\n".join(combined_output)
                log_entry = f"[{status}] {test_name}:\n{output_text}\n\n"

                self.output_box.insert(tk.END, log_entry)
                self.output_box.see(tk.END)

                self.table.insert("", "end", values=(test_name, status, ""))

                self.last_run_results.append({
                    "test": test_name,
                    "status": status,
                    "output": output_text,
                    "log_path": ""
                })

            except Exception as e:
                error_text = f"❌ Error running {test_name}: {e}\n"
                self.output_box.insert(tk.END, error_text)
                self.output_box.see(tk.END)


    def save_logs(self):
        if not self.last_run_results:
            messagebox.showinfo("No Logs", "No test results available to save.")
            return

        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
        os.makedirs(log_dir, exist_ok=True)

        saved = 0
        for result in self.last_run_results:
            test_name = result["test"]
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"{test_name}_{timestamp}.log"
            log_path = os.path.join(log_dir, filename)

        try:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(result["output"])
            result["log_path"] = log_path
            saved += 1
        except Exception as e:
            messagebox.showerror("Save Failed", f"Could not save log for {test_name}:\n{e}")

        if saved > 0:
            messagebox.showinfo("Logs Saved", f"✅ Saved {saved} logs to the logs folder.")
            self.refresh_log_dropdown()
            self.update_table_with_logs()

        else:
            messagebox.showwarning("No Logs Saved", "❌ No logs were saved.")



    def send_email_report(self):
        recipient = self.email_entry.get().strip()
        if not recipient:
            messagebox.showerror("Missing Email", "Please enter a recipient email address.")
            return

        csv_path = self.result_manager.export_to_csv()

        try:
            msg = EmailMessage()
            msg['Subject'] = "Infotainment Test Report"
            msg['From'] = "your_email@gmail.com"  # Replace with your sender email
            msg['To'] = recipient
            msg.set_content("Please find the attached test report.")

            with open(csv_path, "rb") as f:
                msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=os.path.basename(csv_path))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("manohargc2650@gmail.com", "llcsmmpjggxebgej")  # Replace with app password
                smtp.send_message(msg)

            messagebox.showinfo("Email Sent", f"✅ Report sent to {recipient}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email:\n{str(e)}")

    def export_results(self):
        filepath = self.result_manager.export_to_csv()
        messagebox.showinfo("Report Exported", f"✅ Test results saved to:\n{filepath}")

    def clear_output(self):
        self.output_box.delete(1.0, tk.END)
        self.table.delete(*self.table.get_children())

    def show_all_results(self):
        self.output_box.delete(1.0, tk.END)
        self.table.delete(*self.table.get_children())
        for result in self.last_run_results:
            self.display_result(result)

    def filter_results(self, status_filter):
        self.output_box.delete(1.0, tk.END)
        self.table.delete(*self.table.get_children())
        for result in self.last_run_results:
            if result['status'] == status_filter:
                self.display_result(result)

    def display_result(self, result):
        log_display = result["log_path"] if result.get("log_saved") else "Not saved"
        log_line = (
            f"[{result['status']}] {result['test']}:\n"
            f"{result['output']}\n"
            f"📁 Log saved to: {'log_display'}\n\n"
        )
        self.output_box.insert(tk.END, log_line)
        self.table.insert("", "end", values=(result['test'], result['status'], log_display))

    def refresh_log_dropdown(self):
        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_files = sorted(os.listdir(log_dir), reverse=True)
        self.log_dropdown['values'] = log_files[:20]
        self.log_var.set("")

    def load_selected_log(self, event):
        selected_log = self.log_var.get()
        if not selected_log:
            return
        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
        log_path = os.path.join(log_dir, selected_log)
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.output_box.delete(1.0, tk.END)
                self.output_box.insert(tk.END, f"📂 Viewing log: {selected_log}\n\n{content}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load log:\n{str(e)}")


    def clear_test_selection(self):
        for var in self.test_vars.values():
            var.set(False)



    def remove_selected_tests(self):
        selected_to_remove = [name for name, var in self.test_vars.items() if var.get()]
        if not selected_to_remove:
            messagebox.showinfo("No Selection", "Please select test cases to remove.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected_to_remove)} test file(s)?")
        if not confirm:
            return

        removed = 0
        failed = []

        test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))

        for test_name in selected_to_remove:
            try:
                file_path = os.path.join(test_dir, f"{test_name}.py")
               

                if os.path.exists(file_path):
                    os.remove(file_path)
                    removed += 1
                    print(f"✅ Deleted: {file_path}")
                else:
                    print(f"❌ File not found: {file_path}")
                    failed.append(test_name)

            

            # Remove .pyc from __pycache__ (optional)
                pycache_dir = os.path.join(test_dir, "__pycache__")
                if os.path.exists(pycache_dir):
                    for fname in os.listdir(pycache_dir):
                        if fname.startswith(test_name)and fname.endswith(".pyc"):
                            os.remove(os.path.join(pycache_dir, fname))

            except Exception as e:
                print(f"⚠️ Error deleting {test_name}: {e}")
                failed.append(test_name)

    # ✅ Reload available test cases UI
        self.load_test_cases()

        messagebox.showinfo("Remove Complete", f"🗑️ Removed: {removed}\n❌ Failed: {len(failed)}")


    def show_all_results(self):
        self.output_box.delete(1.0, tk.END)
        self.table.delete(*self.table.get_children())
        for result in self.last_run_results:
            self.display_result(result)
   
       # ---------------------------------------------------------------------
    #  Pie‑chart of pass / fail results
    # ---------------------------------------------------------------------
    def show_dashboard(self):
        """
        Open a small window with a pie chart of PASS vs FAIL based on
        self.last_run_results.  Call this after running tests.
        """
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        if not self.last_run_results:
            messagebox.showinfo("No Data", "Run some tests first.")
            return

        # ----- count results ---------------------------------------------
        pass_count = sum(1 for r in self.last_run_results if r["status"] == "PASS")
        fail_count = sum(1 for r in self.last_run_results if r["status"] == "FAIL")

        # avoid zero‑division
        if pass_count + fail_count == 0:
            messagebox.showinfo("No Results", "No PASS/FAIL data to plot.")
            return

        # ----- create figure ---------------------------------------------
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(
            [pass_count, fail_count],
            labels=[f"PASS ({pass_count})", f"FAIL ({fail_count})"],
            autopct="%1.0f%%",
            startangle=90,
        )
        ax.set_title("Test‑case Result Distribution")

        # ----- embed in a new Tk window ----------------------------------
        pie_win = tk.Toplevel(self.root)
        pie_win.title("PASS vs FAIL")
        canvas = FigureCanvasTkAgg(fig, master=pie_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # optional: close matplotlib figure when the Tk window closes
        pie_win.protocol("WM_DELETE_WINDOW", lambda: (plt.close(fig), pie_win.destroy()))



    def refresh_log_dropdown(self):
        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_files = sorted(os.listdir(log_dir), reverse=True)
        self.log_dropdown['values'] = log_files[:20]  # Show latest 20
        self.log_var.set("")  # Clear selection

    def load_selected_log(self, event):
        selected_log = self.log_var.get()
        if not selected_log:
            return
        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
        log_path = os.path.join(log_dir, selected_log)
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, f"📂 Viewing log: {selected_log}\n\n{content}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load log:\n{str(e)}")


    def update_table_with_logs(self):
    # Clear the table and repopulate with updated log paths
        self.table.delete(*self.table.get_children())
        for result in self.last_run_results:
            self.table.insert("", "end", values=(result["test"], result["status"], result["log_path"]))


    # def run_selected_tests(self):
    #     selected = [name for name, var in self.test_vars.items() if var.get()]
    #     if not selected:
    #         messagebox.showwarning("No Selection", "Please select at least one test case.")
    #         return

    #     self.output_box.delete(1.0, tk.END)
    #     self.table.delete(*self.table.get_children())
    #     self.last_run_results.clear()

    #     for test_name in selected:
    #         file_path = self.test_vars[test_name]["path"]
    #         try:
    #             with open(file_path, "r", encoding="utf-8") as f:
    #                 code = f.read()

    #             namespace = {}
    #             exec(code, namespace)

    #             run_functions = [fn for fn in namespace if fn.startswith("run") and callable(namespace[fn])]
    #             if not run_functions:
    #                 raise Exception("No run_*() functions found.")

    #             combined_output = []
    #             passed = True

    #             for fn in run_functions:
    #                 try:
    #                     result = namespace[fn]()
    #                     if result:
    #                         msg = f"✅ {fn}() PASSED"
    #                     else:
    #                         msg = f"❌ {fn}() FAILED — returned False"
    #                         passed = False
    #                     combined_output.append(msg)
    #                 except AssertionError as ae:
    #                     msg = f"❌ {fn}() ASSERTION FAILED: {ae}"
    #                     combined_output.append(msg)
    #                     passed = False
    #                 except Exception as e:
    #                     msg = f"❌ {fn}() CRASHED:\n{traceback.format_exc()}"
    #                     combined_output.append(msg)
    #                     passed = False

    #             status = "PASS" if passed else "FAIL"
    #             output_text = "\n".join(combined_output)
    #             log_line = f"[{status}] {test_name}\n{'='*40}\n{output_text}\n\n"

    #             self.output_box.insert(tk.END, log_line)
    #             self.output_box.see(tk.END)

    #             self.last_run_results.append({
    #                 "test": test_name,
    #                 "status": status,
    #                 "output": log_line,
    #                 "log_path": ""
    #             })

    #             self.table.insert("", "end", values=(test_name, status, ""))

    #         except Exception as e:
    #             error_log = f"❌ Error running {test_name}:\n{traceback.format_exc()}"
    #             self.output_box.insert(tk.END, error_log)
    #             self.output_box.see(tk.END)
