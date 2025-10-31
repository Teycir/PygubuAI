#!/usr/bin/env python3
"""Tests for critical fixes in v0.4.1"""
import unittest
import tempfile
import pathlib
import json
import time
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))

class TestPathValidation(unittest.TestCase):
    """Test path validation security fixes"""
    
    def test_validate_path_prevents_traversal(self):
        """Test that directory traversal is blocked"""
        from pygubuai.utils import validate_path
        
        with self.assertRaises(ValueError) as ctx:
            validate_path("../../etc/passwd")
        self.assertIn("traversal", str(ctx.exception).lower())
    
    def test_validate_path_requires_existence(self):
        """Test must_exist parameter"""
        from pygubuai.utils import validate_path
        
        with self.assertRaises(ValueError) as ctx:
            validate_path("/nonexistent/path/12345", must_exist=True)
        self.assertIn("does not exist", str(ctx.exception))
    
    def test_validate_path_requires_directory(self):
        """Test must_be_dir parameter"""
        from pygubuai.utils import validate_path
        
        with tempfile.NamedTemporaryFile() as tmp:
            with self.assertRaises(ValueError) as ctx:
                validate_path(tmp.name, must_be_dir=True)
            self.assertIn("not a directory", str(ctx.exception))
    
    def test_validate_path_accepts_valid_paths(self):
        """Test that valid paths are accepted"""
        from pygubuai.utils import validate_path
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = validate_path(tmpdir, must_exist=True, must_be_dir=True)
            self.assertIsInstance(result, pathlib.Path)
            self.assertTrue(result.exists())


class TestAtomicWrites(unittest.TestCase):
    """Test atomic file write operations"""
    
    def test_workflow_save_is_atomic(self):
        """Test workflow saves don't corrupt on failure"""
        from pygubuai.workflow import save_workflow
        
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = pathlib.Path(tmpdir)
            workflow_file = project_path / ".pygubu-workflow.json"
            
            # Create initial workflow
            data = {"project": "test", "file_hashes": {}, "history": []}
            save_workflow(project_path, data)
            
            self.assertTrue(workflow_file.exists())
            
            # Verify no temp files left behind
            temp_files = list(project_path.glob(".pygubu-workflow-*.tmp"))
            self.assertEqual(len(temp_files), 0)
    
    def test_workflow_save_cleans_up_on_error(self):
        """Test temp files are cleaned up on error"""
        from pygubuai.workflow import save_workflow
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = pathlib.Path(tmpdir)
            
            # Make directory read-only to cause write error
            os.chmod(project_path, 0o444)
            
            data = {"project": "test", "file_hashes": {}, "history": []}
            
            try:
                with self.assertRaises(Exception):
                    save_workflow(project_path, data)
                
                # Verify no temp files left behind
                temp_files = list(project_path.glob(".pygubu-workflow-*.tmp"))
                self.assertEqual(len(temp_files), 0)
            finally:
                os.chmod(project_path, 0o755)


class TestCircuitBreaker(unittest.TestCase):
    """Test watch loop circuit breaker"""
    
    @patch('pygubuai.workflow.Registry')
    @patch('pygubuai.workflow._check_ui_changes')
    @patch('pygubuai.workflow.time.sleep')
    def test_watch_stops_after_max_errors(self, mock_sleep, mock_check, mock_registry):
        """Test watch exits after MAX_ERRORS consecutive failures"""
        from pygubuai.workflow import watch_project
        
        # Setup mocks
        mock_reg_instance = MagicMock()
        mock_reg_instance.list_projects.return_value = {"test": "/tmp/test"}
        mock_registry.return_value = mock_reg_instance
        
        # Make _check_ui_changes always fail
        mock_check.side_effect = RuntimeError("Simulated error")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a .ui file
            test_path = pathlib.Path(tmpdir)
            (test_path / "test.ui").write_text("<interface></interface>")
            
            mock_reg_instance.list_projects.return_value = {"test": str(test_path)}
            
            # Should exit after 5 errors
            with self.assertRaises(SystemExit):
                watch_project("test", interval=0.01)
            
            # Verify it tried multiple times (5 errors + initial success check)
            self.assertGreaterEqual(mock_check.call_count, 5)


class TestConfigErrorReporting(unittest.TestCase):
    """Test configuration error reporting"""
    
    def test_corrupted_config_logs_warning(self):
        """Test that corrupted config files log warnings"""
        from pygubuai.config import Config
        
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = pathlib.Path(tmpdir) / ".pygubuai"
            config_dir.mkdir()
            config_file = config_dir / "config.json"
            
            # Write invalid JSON
            config_file.write_text("{invalid json")
            
            # Patch config path
            with patch.object(Config, '__init__', lambda self: None):
                cfg = Config()
                cfg.config_path = config_file
                
                with self.assertLogs(level='WARNING') as log:
                    result = cfg._load()
                    
                    # Should use defaults
                    self.assertIn("registry_path", result)
                    
                    # Should log warning
                    self.assertTrue(any("corrupted" in msg.lower() for msg in log.output))
    
    def test_invalid_config_format_logs_warning(self):
        """Test that non-dict config logs warning"""
        from pygubuai.config import Config
        
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = pathlib.Path(tmpdir) / ".pygubuai"
            config_dir.mkdir()
            config_file = config_dir / "config.json"
            
            # Write valid JSON but wrong type
            config_file.write_text('["not", "a", "dict"]')
            
            with patch.object(Config, '__init__', lambda self: None):
                cfg = Config()
                cfg.config_path = config_file
                
                with self.assertLogs(level='WARNING') as log:
                    result = cfg._load()
                    
                    # Should use defaults
                    self.assertIn("registry_path", result)
                    
                    # Should log warning
                    self.assertTrue(any("invalid config format" in msg.lower() for msg in log.output))


class TestRegistryPathValidation(unittest.TestCase):
    """Test registry path validation"""
    
    def test_registry_path_blocks_traversal(self):
        """Test that registry path blocks directory traversal"""
        from pygubuai.config import Config
        
        with patch.object(Config, '__init__', lambda self: None):
            cfg = Config()
            cfg.config_path = pathlib.Path("/tmp/.pygubuai/config.json")
            cfg.config = {"registry_path": "../../etc/passwd"}
            
            with self.assertLogs(level='WARNING') as log:
                result = cfg.registry_path
                
                # Should use default instead
                self.assertIn(".pygubu-registry.json", str(result))
                
                # Should log warning
                self.assertTrue(any("suspicious" in msg.lower() for msg in log.output))


class TestRegisterPathValidation(unittest.TestCase):
    """Test register command path validation"""
    
    def test_register_validates_paths(self):
        """Test that register_project validates paths"""
        from pygubuai.register import register_project
        from pygubuai.errors import InvalidProjectError
        
        with self.assertRaises(InvalidProjectError):
            register_project("/nonexistent/path/12345")
    
    def test_scan_validates_paths(self):
        """Test that scan_directory validates paths"""
        from pygubuai.register import scan_directory
        from pygubuai.errors import InvalidProjectError
        
        with self.assertRaises(InvalidProjectError):
            scan_directory("/nonexistent/path/12345")


class TestResourceLimits(unittest.TestCase):
    """Test resource limit protections"""
    
    @patch('pygubuai.workflow.Registry')
    def test_watch_limits_file_count(self, mock_registry):
        """Test that watch limits number of files processed"""
        from pygubuai.workflow import watch_project
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = pathlib.Path(tmpdir)
            
            # Create many .ui files (more than MAX_FILES)
            for i in range(1100):
                (test_path / f"test{i}.ui").write_text("<interface></interface>")
            
            mock_reg_instance = MagicMock()
            mock_reg_instance.list_projects.return_value = {"test": str(test_path)}
            mock_registry.return_value = mock_reg_instance
            
            # Should log warning about too many files
            with self.assertLogs(level='WARNING') as log:
                # This will start watching, we need to interrupt it quickly
                import threading
                def stop_watch():
                    time.sleep(0.1)
                    import os
                    import signal
                    os.kill(os.getpid(), signal.SIGINT)
                
                thread = threading.Thread(target=stop_watch)
                thread.start()
                
                try:
                    watch_project("test", interval=0.01)
                except (KeyboardInterrupt, SystemExit):
                    pass
                
                thread.join()
                
                # Should have logged warning about file limit
                self.assertTrue(any("limiting to" in msg.lower() for msg in log.output))


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
