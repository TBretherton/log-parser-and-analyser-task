import unittest
from io import StringIO
from datetime import timedelta
from analyze_logs import process_log_lines, create_logger

class TestLogAnalyzer(unittest.TestCase):

    def run_log_test(self, log_content, expected_outputs, warning_threshold=5, error_threshold=10):
        log_stream = StringIO()
        logger = create_logger(stream=log_stream)
        logs = StringIO(log_content)
        process_log_lines(logs,
                          timedelta(minutes=warning_threshold),
                          timedelta(minutes=error_threshold),
                          logger)
        output = log_stream.getvalue()
        for expected in expected_outputs:
            self.assertIn(expected, output)

    def test_info_log_for_short_job(self):
        self.run_log_test(
            "12:00:00, Task A, START, 100\n12:03:00, Task A, END, 100",
            ["INFO: Job 'Task A' (PID: 100) took 0:03:00"]
        )

    def test_warning_for_medium_job(self):
        self.run_log_test(
            "12:00:00, Task B, START, 101\n12:06:00, Task B, END, 101",
            ["WARNING: Job 'Task B' (PID: 101) took 0:06:00"]
        )

    def test_error_for_long_job(self):
        self.run_log_test(
            "12:00:00, Task C, START, 102\n12:11:00, Task C, END, 102",
            ["ERROR: Job 'Task C' (PID: 102) took 0:11:00"]
        )

    def test_end_without_start(self):
        self.run_log_test(
            "12:05:00, Task D, END, 103",
            ["WARNING: END without START for PID: 103"]
        )

    def test_start_without_end(self):
        self.run_log_test(
            "12:05:00, Task E, START, 104",
            [
                "WARNING: Unfinished jobs detected:",
                "WARNING: Job 'Task E' (PID: 104) started at 12:05:00 but has no END."
            ]
        )

    def test_invalid_timestamp(self):
        self.run_log_test(
            "invalid_time, Task F, START, 105",
            ["WARNING: Invalid time format: invalid_time"]
        )

    def test_malformed_line(self):
        self.run_log_test(
            "12:00:00, Task G, START",  # missing PID
            ["WARNING: Skipping malformed line"]
        )

    def test_unknown_status(self):
        self.run_log_test(
            "12:00:00, Task H, LAUNCH, 106",
            ["WARNING: Unknown status: LAUNCH"]
        )
