import copy
import os
import re
import sys
import unittest

def main():
    print(f"running main")

if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.discover('.', '*_test.py')
    test_runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    result = test_runner.run(test_suite)
    if not result.wasSuccessful():
        sys.exit(1)
    main()