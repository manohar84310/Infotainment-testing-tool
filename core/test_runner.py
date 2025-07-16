# core/test_runner.py

import traceback

class TestRunner:
    def run_test(self, file_path):
        try:
            namespace = {}

            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
                exec(code, namespace)

            run_functions = [f for f in namespace if f.startswith("run") and callable(namespace[f])]

            output_lines = []
            all_passed = True

            for func_name in run_functions:
                try:
                    result = namespace[func_name]()
                    output_lines.append(f"{func_name}() => {'PASS' if result else 'FAIL'}")
                    if not result:
                        all_passed = False
                except Exception as e:
                    output_lines.append(f"{func_name}() => ERROR: {e}")
                    all_passed = False

            return "\n".join(output_lines), all_passed

        except Exception as e:
            tb = traceback.format_exc()
            return f"❌ Failed to run script:\n{e}\n\n{tb}", False
