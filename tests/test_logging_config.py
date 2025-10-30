#!/usr/bin/env python3
"""Tests for logging configuration."""
import unittest
import logging
import os
import sys
import pathlib
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))

from pygubuai.logging_config import get_log_level, setup_logging, get_logger

class TestLoggingConfig(unittest.TestCase):
    """Test logging configuration functionality."""
    
    def test_get_log_level_default(self):
        """Test default log level is INFO."""
        with patch.dict(os.environ, {}, clear=True):
            level = get_log_level()
            self.assertEqual(level, logging.INFO)
    
    def test_get_log_level_from_env(self):
        """Test log level from environment variable."""
        with patch.dict(os.environ, {'PYGUBUAI_LOG_LEVEL': 'DEBUG'}):
            level = get_log_level()
            self.assertEqual(level, logging.DEBUG)
        
        with patch.dict(os.environ, {'PYGUBUAI_LOG_LEVEL': 'ERROR'}):
            level = get_log_level()
            self.assertEqual(level, logging.ERROR)
    
    def test_get_log_level_invalid(self):
        """Test invalid log level defaults to INFO."""
        with patch.dict(os.environ, {'PYGUBUAI_LOG_LEVEL': 'INVALID'}):
            level = get_log_level()
            self.assertEqual(level, logging.INFO)
    
    def test_setup_logging(self):
        """Test logger setup."""
        logger = setup_logging('test_logger')
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, 'test_logger')
    
    def test_setup_logging_with_level(self):
        """Test logger setup with custom level."""
        logger = setup_logging('test_logger_debug', level=logging.DEBUG)
        self.assertEqual(logger.level, logging.DEBUG)
    
    def test_get_logger(self):
        """Test get_logger convenience function."""
        logger = get_logger('test_module')
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, 'test_module')
    
    def test_logger_no_duplicate_handlers(self):
        """Test that multiple calls don't add duplicate handlers."""
        logger1 = get_logger('test_dup')
        handler_count1 = len(logger1.handlers)
        
        logger2 = get_logger('test_dup')
        handler_count2 = len(logger2.handlers)
        
        self.assertEqual(handler_count1, handler_count2)

if __name__ == '__main__':
    unittest.main()
