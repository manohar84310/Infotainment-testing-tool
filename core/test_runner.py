import importlib
import time
import traceback

class TestRunner:
    def run_test(self, test_name):
        try:
            module = importlib.import_module(f"tests.{test_name}")
            start_time = time.time()
            result = module.run()  # True/False or string
            end_time = time.time()
            duration = end_time - start_time

            status = "PASS" if result else "FAIL"
            summary_output = f"Test: {test_name}\nStatus: {status}\nDuration: {duration:.2f}s"
            raw_output = f"=== FULL RAW EXECUTION ===\n{test_name} finished in {duration:.2f}s\nResult: {result}"

            return summary_output, result, raw_output

        except Exception as e:
            tb = traceback.format_exc()
            summary_output = f"Test: {test_name}\nStatus: FAIL\nError: {str(e)}"
            raw_output = f"=== EXCEPTION ===\n{tb}"
            return summary_output, False, raw_output
