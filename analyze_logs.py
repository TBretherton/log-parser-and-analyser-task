import csv
from datetime import datetime, timedelta
import logging

import sys
import unittest

def create_logger(name="log_monitor", stream=None, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.hasHandlers():
        logger.handlers.clear()
    handler = logging.StreamHandler(stream or sys.stdout)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def parse_timestamp(time_str, logger):
    try:
        return datetime.strptime(time_str.strip(), "%H:%M:%S")
    except ValueError:
        logger.warning(f"Invalid time format: {time_str}")
        return None

def handle_start(pid, timestamp, description, job_starts):
    job_starts[pid] = (timestamp, description)

def handle_end(pid, timestamp, job_starts, logger, warning_threshold, error_threshold):
    if pid not in job_starts:
        logger.warning(f"END without START for PID: {pid}")
        return

    start_time, desc = job_starts.pop(pid)
    duration = timestamp - start_time
    message = f"Job '{desc}' (PID: {pid}) took {duration}"

    if duration > error_threshold:
        logger.error(message)
    elif duration > warning_threshold:
        logger.warning(message)
    else:
        logger.info(message)

def check_unfinished_jobs(job_starts, logger):
    if job_starts:
        logger.warning("Unfinished jobs detected:")
        for pid, (start_time, desc) in job_starts.items():
            logger.warning(f"Job '{desc}' (PID: {pid}) started at {start_time.strftime('%H:%M:%S')} but has no END.")

def process_log_lines(log_lines, warning_threshold, error_threshold, logger=None):
    logger = logger or create_logger()
    job_starts = {}
    reader = csv.reader(log_lines)

    for line in reader:
        if len(line) != 4:
            logger.warning(f"Skipping malformed line: {line}")
            continue

        time_str, description, status, pid = [item.strip() for item in line]
        timestamp = parse_timestamp(time_str, logger)
        if not timestamp:
            continue

        if status == "START":
            handle_start(pid, timestamp, description, job_starts)
        elif status == "END":
            handle_end(pid, timestamp, job_starts, logger, warning_threshold, error_threshold)
        else:
            logger.warning(f"Unknown status: {status} in line: {line}")

    check_unfinished_jobs(job_starts, logger)


def main():
    warning_threshold = timedelta(minutes=5)
    error_threshold = timedelta(minutes=10)
    logger = create_logger()

    with open('logs[7].log', 'r') as file:
        process_log_lines(file, warning_threshold, error_threshold, logger)

if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.discover('.', '*_test.py')
    test_runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    print("running tests")
    result = test_runner.run(test_suite)
    if not result.wasSuccessful():
        sys.exit(1)
    print("running log analysis")
    main()