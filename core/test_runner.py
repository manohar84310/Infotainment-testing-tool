# infotainment_test_tool/core/test_runner.py

import importlib
import traceback
import io
import contextlib
from core.logger import save_log

class TestRunner:
    def run_test(self, test_module_name):
        try:
            # Dynamically import the test module
            module = importlib.import_module(f"tests.{test_module_name}")

            # Capture any print output from the test
            output_buffer = io.StringIO()
            with contextlib.redirect_stdout(output_buffer):
                passed = module.run()

            output = output_buffer.getvalue()

            # Save log and return its path
            log_path = save_log(test_module_name, output)

            # Return output text, pass/fail status, and log path
            return output, passed, log_path

        except Exception:
            error_msg = f"Exception in {test_module_name}:\n{traceback.format_exc()}"
            log_path = save_log(test_module_name, error_msg)
            return error_msg, False, log_path
