#!/usr/bin/env python3
"""Test runner for PygubuAI"""
import unittest
import sys
import pathlib

def run_tests():
    """Run all tests"""
    test_dir = pathlib.Path(__file__).parent / "tests"
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
