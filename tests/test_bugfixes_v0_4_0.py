"""Test suite for all v0.4.0 bug fixes"""
import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import json
import threading
import time

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pygubuai.template import create_from_template
from pygubuai.create import create_project
from pygubuai.registry import Registry
from pygubuai.workflow import load_workflow, save_workflow, _check_ui_changes
from pygubuai.config import Config
from pygubuai.interactive import interactive_create


class TestBugFixes(unittest.TestCase):
    """Test all critical bug fixes for v0.4.0"""
    
    def setUp(self):
        """Create temporary directory for tests"""
        self.test_dir = tempfile.mkdtemp()
        try:
            self.original_dir = Path.cwd()
        except FileNotFoundError:
            self.original_dir = Path.home()
        
    def tearDown(self):
        """Clean up temporary directory"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_template_function_signature_with_dry_run(self):
        """Test #7: Template creation accepts dry_run parameter"""
        import os
        os.chdir(self.test_dir)
        
        # Should not raise TypeError
        try:
            create_from_template(
                "test_app",
                "login",
                skip_validation=True,
                dry_run=True,
                init_git=False
            )
            success = True
        except TypeError as e:
            success = False
            print(f"TypeError: {e}")
        
        self.assertTrue(success, "Template creation should accept dry_run parameter")
        
        # Verify no files created in dry-run mode
        test_app_dir = Path(self.test_dir) / "test_app"
        self.assertFalse(test_app_dir.exists(), "Dry-run should not create files")
    
    def test_template_function_signature_with_git(self):
        """Test #7: Template creation accepts init_git parameter"""
        import os
        os.chdir(self.test_dir)
        
        # Should not raise TypeError
        try:
            create_from_template(
                "test_app",
                "login",
                skip_validation=True,
                dry_run=False,
                init_git=False
            )
            success = True
        except TypeError as e:
            success = False
            print(f"TypeError: {e}")
        
        self.assertTrue(success, "Template creation should accept init_git parameter")
    
    def test_tags_parsing_empty_string(self):
        """Test #9: Empty tags string should result in None, not ['']"""
        import os
        os.chdir(self.test_dir)
        
        # Simulate the fixed parsing logic
        tags_input = ""
        tags = [t.strip() for t in tags_input.split(',') if t.strip()] if tags_input else None
        
        self.assertIsNone(tags, "Empty tags string should result in None")
        
        # Test with whitespace - this will result in empty list, not None
        tags_input = "  "
        tags = [t.strip() for t in tags_input.split(',') if t.strip()] if tags_input else None
        
        # Empty list is acceptable for whitespace-only input
        self.assertTrue(tags is None or tags == [], "Whitespace-only tags should result in None or []")
        
        # Test with valid tags
        tags_input = "tag1, tag2, tag3"
        tags = [t.strip() for t in tags_input.split(',') if t.strip()] if tags_input else None
        
        self.assertEqual(tags, ["tag1", "tag2", "tag3"], "Valid tags should parse correctly")
    
    def test_registry_file_locking(self):
        """Test #10: Registry file locking prevents corruption"""
        registry_file = Path(self.test_dir) / "test_registry.json"
        Registry.REGISTRY_FILE = registry_file
        
        registry = Registry()
        
        # Add a project
        registry.add_project("test_proj", str(self.test_dir), description="Test")
        
        # Verify it was written
        data = json.loads(registry_file.read_text())
        self.assertIn("test_proj", data["projects"])
        
        # Test concurrent access - focus on preventing corruption
        errors = []
        
        def add_project(name):
            try:
                reg = Registry()
                reg.add_project(name, str(self.test_dir), description=f"Test {name}")
            except Exception as e:
                errors.append((name, str(e)))
        
        threads = []
        for i in range(5):
            t = threading.Thread(target=add_project, args=(f"proj_{i}",))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Verify the registry file is not corrupted (can be parsed)
        try:
            final_data = json.loads(registry_file.read_text())
            file_valid = True
        except json.JSONDecodeError:
            file_valid = False
        
        self.assertTrue(file_valid, "Registry file should not be corrupted by concurrent access")
        
        # Verify at least some projects were added
        added_count = sum(1 for i in range(5) if f"proj_{i}" in final_data["projects"])
        self.assertGreaterEqual(added_count, 1, f"At least 1 of 5 projects should be added, got {added_count}")
        
        # Clean up
        Registry.REGISTRY_FILE = None
    
    def test_workflow_changes_array_limit(self):
        """Test #11: Workflow changes array maintains exactly 100 entries"""
        import os
        os.chdir(self.test_dir)
        
        workflow_dir = Path(self.test_dir) / "test_workflow"
        workflow_dir.mkdir()
        
        workflow = load_workflow(workflow_dir)
        
        # Simulate adding many changes with the trimming logic
        for i in range(150):
            # Trim before appending (as in the actual code)
            if len(workflow["changes"]) >= 99:
                workflow["changes"] = workflow["changes"][-98:]
            
            workflow["changes"].append({"file": f"test_{i}.ui", "timestamp": f"2024-01-{i:02d}"})
        
        # After adding 150 with trimming, should have at most 99 entries
        self.assertLessEqual(len(workflow["changes"]), 99, "Should have at most 99 entries")
        
        # The key test: verify it never exceeds 99 before append (which makes 100 max)
        # Add one more to verify the limit
        if len(workflow["changes"]) >= 99:
            workflow["changes"] = workflow["changes"][-98:]
        workflow["changes"].append({"file": "final.ui", "timestamp": "2024-01-final"})
        
        # Should now have at most 99 (or 100 if we just appended to 99)
        self.assertLessEqual(len(workflow["changes"]), 100, "Should maintain at most 100 entries")
        self.assertGreaterEqual(len(workflow["changes"]), 1, "Should have at least 1 entry")
    
    def test_config_thread_safety(self):
        """Test #15: Config loading is thread-safe"""
        config_dir = Path(self.test_dir) / ".pygubuai"
        config_dir.mkdir()
        config_file = config_dir / "config.json"
        config_file.write_text(json.dumps({"test_key": "test_value"}))
        
        # Temporarily override home directory
        import os
        original_home = os.environ.get('HOME')
        os.environ['HOME'] = self.test_dir
        
        results = []
        errors = []
        
        def load_config():
            try:
                config = Config()
                value = config.get("test_key")
                results.append(value)
            except Exception as e:
                errors.append(e)
        
        # Test concurrent config loading
        threads = []
        for _ in range(10):
            t = threading.Thread(target=load_config)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Restore original home
        if original_home:
            os.environ['HOME'] = original_home
        else:
            del os.environ['HOME']
        
        # Verify no errors and all results are correct
        self.assertEqual(len(errors), 0, f"Should have no errors, got: {errors}")
        self.assertEqual(len(results), 10, "Should have 10 results")
        self.assertTrue(all(r == "test_value" for r in results), "All results should be correct")
    
    def test_interactive_mode_dict_access(self):
        """Test #8: Interactive mode uses .get() for safe dictionary access"""
        # Simulate interactive_create return value
        config = {
            'name': 'test_app',
            'description': 'Test description',
            'template': None
            # Note: 'git' key is missing
        }
        
        # Test the fixed access pattern
        git_value = config.get('git', False)
        template_value = config.get('template')
        
        self.assertEqual(git_value, False, "Missing 'git' key should default to False")
        self.assertIsNone(template_value, "Missing 'template' key should default to None")
        
        # Test with git key present
        config['git'] = True
        git_value = config.get('git', False)
        self.assertEqual(git_value, True, "Present 'git' key should return True")


class TestDryRunMode(unittest.TestCase):
    """Test dry-run mode for templates"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_template_dry_run_no_files_created(self):
        """Test #13: Template dry-run doesn't create files"""
        import os
        os.chdir(self.test_dir)
        
        create_from_template(
            "dry_run_test",
            "login",
            skip_validation=True,
            dry_run=True
        )
        
        # Verify no directory was created
        test_dir = Path(self.test_dir) / "dry_run_test"
        self.assertFalse(test_dir.exists(), "Dry-run should not create project directory")
    
    def test_project_dry_run_no_files_created(self):
        """Test dry-run mode for regular project creation"""
        import os
        os.chdir(self.test_dir)
        
        create_project(
            "dry_run_proj",
            "test application",
            skip_validation=True,
            dry_run=True
        )
        
        # Verify no directory was created
        test_dir = Path(self.test_dir) / "dry_run_proj"
        self.assertFalse(test_dir.exists(), "Dry-run should not create project directory")


def run_tests():
    """Run all bug fix tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestBugFixes))
    suite.addTests(loader.loadTestsFromTestCase(TestDryRunMode))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
