"""Pytest configuration and fixtures"""
import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def tmp_path():
    """Create temporary directory for tests"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def clean_registry(tmp_path):
    """Create clean registry for testing"""
    from pygubuai.registry import Registry
    registry_path = tmp_path / "test_registry.json"
    return Registry(str(registry_path))


@pytest.fixture
def sample_project(tmp_path):
    """Create sample project for testing"""
    from pygubuai.create import create_project
    project_name = "test_project"
    create_project(project_name, "test application", str(tmp_path))
    return tmp_path / project_name


@pytest.fixture
def benchmark(request):
    """Simple benchmark fixture"""
    import time
    
    class BenchmarkResult:
        def __init__(self):
            self.stats = type('obj', (object,), {
                'stats': type('obj', (object,), {'mean': 0})()
            })()
        
        def __call__(self, func):
            start = time.time()
            result = func()
            elapsed = time.time() - start
            self.stats.stats.mean = elapsed
            return result
    
    return BenchmarkResult()


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
