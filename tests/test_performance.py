"""Performance tests and benchmarks"""

import gc
import time
import tracemalloc

import pytest

from pygubuai.create import create_project
from pygubuai.registry import Registry
from pygubuai.workflow import WorkflowTracker
from pygubuai.status import check_project_status


class TestPerformanceBenchmarks:
    """Benchmark critical operations"""

    def test_project_creation_speed(self, tmp_path, benchmark):
        """Benchmark: Project creation should be < 1 second"""

        def create():
            name = f"perf_test_{time.time()}"
            return create_project(name, "test app", str(tmp_path))

        result = benchmark(create)
        assert result is True
        assert benchmark.stats.stats.mean < 1.0, "Project creation too slow"

    def test_registry_operations_speed(self, tmp_path, benchmark):
        """Benchmark: Registry operations should be < 100ms"""
        registry = Registry()
        project_name = "bench_project"
        project_path = tmp_path / project_name
        create_project(project_name, "test", str(tmp_path))

        def registry_ops():
            registry.add_project(project_name, str(project_path))
            registry.get_project(project_name)
            registry.list_projects()
            registry.remove_project(project_name)

        benchmark(registry_ops)
        assert benchmark.stats.stats.mean < 0.1, "Registry operations too slow"

    def test_status_check_speed(self, tmp_path, benchmark):
        """Benchmark: Status check should be < 500ms"""
        project_name = "status_bench"
        create_project(project_name, "test", str(tmp_path))

        registry = Registry()
        registry.add_project(project_name, str(tmp_path / project_name))

        def check_status():
            return check_project_status(project_name)

        benchmark(check_status)
        assert benchmark.stats.stats.mean < 0.5, "Status check too slow"


class TestLargeRegistries:
    """Test with large registries (100+ projects)"""

    @pytest.fixture
    def large_registry(self, tmp_path):
        """Create registry with 100 projects"""
        registry = Registry()

        for i in range(100):
            proj_name = f"project_{i:03d}"
            proj_path = tmp_path / proj_name
            proj_path.mkdir(parents=True)

            # Create minimal project structure
            (proj_path / f"{proj_name}.ui").write_text("<interface></interface>")
            (proj_path / f"{proj_name}.py").write_text("# test")

            registry.add_project(proj_name, str(proj_path))

        return registry

    def test_list_100_projects(self, large_registry):
        """Test listing 100 projects"""
        start = time.time()
        projects = large_registry.list_projects()
        elapsed = time.time() - start

        assert len(projects) == 100
        assert elapsed < 1.0, f"Listing 100 projects took {elapsed:.2f}s"

    def test_search_in_large_registry(self, large_registry):
        """Test searching in large registry"""
        start = time.time()
        project = large_registry.get_project("project_050")
        elapsed = time.time() - start

        assert project is not None
        assert elapsed < 0.1, f"Search took {elapsed:.2f}s"

    def test_add_to_large_registry(self, large_registry, tmp_path):
        """Test adding to large registry"""
        start = time.time()

        new_proj = tmp_path / "new_project"
        new_proj.mkdir(parents=True)
        large_registry.add_project("new_project", str(new_proj))

        elapsed = time.time() - start

        assert "new_project" in large_registry.list_projects()
        assert elapsed < 0.5, f"Adding to large registry took {elapsed:.2f}s"

    def test_remove_from_large_registry(self, large_registry):
        """Test removing from large registry"""
        start = time.time()
        large_registry.remove_project("project_050")
        elapsed = time.time() - start

        assert "project_050" not in large_registry.list_projects()
        assert elapsed < 0.5, f"Removing from large registry took {elapsed:.2f}s"


class TestMemoryLeaks:
    """Test for memory leaks"""

    def test_repeated_project_creation_memory(self, tmp_path):
        """Test memory doesn't grow with repeated operations"""
        tracemalloc.start()

        # Baseline
        gc.collect()
        baseline = tracemalloc.get_traced_memory()[0]

        # Create and destroy 50 projects
        for i in range(50):
            proj_name = f"mem_test_{i}"
            create_project(proj_name, "test", str(tmp_path))

            # Clean up
            proj_path = tmp_path / proj_name
            if proj_path.exists():
                for file in proj_path.iterdir():
                    file.unlink()
                proj_path.rmdir()

        gc.collect()
        final = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()

        # Memory growth should be minimal (< 10MB)
        growth = (final - baseline) / 1024 / 1024
        assert growth < 10, f"Memory leak detected: {growth:.2f}MB growth"

    def test_registry_memory_stability(self, tmp_path):
        """Test registry doesn't leak memory"""
        tracemalloc.start()

        registry = Registry()
        gc.collect()
        baseline = tracemalloc.get_traced_memory()[0]

        # Add and remove 100 projects
        for i in range(100):
            proj_name = f"reg_mem_{i}"
            proj_path = tmp_path / proj_name
            proj_path.mkdir(parents=True)

            registry.add_project(proj_name, str(proj_path))
            registry.remove_project(proj_name)

        gc.collect()
        final = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()

        growth = (final - baseline) / 1024 / 1024
        assert growth < 5, f"Registry memory leak: {growth:.2f}MB growth"

    def test_workflow_tracker_memory(self, tmp_path):
        """Test workflow tracker doesn't leak memory"""
        project_name = "workflow_mem"
        project_path = tmp_path / project_name
        create_project(project_name, "test", str(tmp_path))

        tracemalloc.start()
        gc.collect()
        baseline = tracemalloc.get_traced_memory()[0]

        # Add 1000 events
        tracker = WorkflowTracker(str(project_path))
        for i in range(1000):
            tracker.add_event("test", f"Event {i}")

        gc.collect()
        final = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()

        growth = (final - baseline) / 1024 / 1024
        assert growth < 5, f"Workflow tracker memory leak: {growth:.2f}MB growth"


class TestScalability:
    """Test scalability with increasing load"""

    def test_project_creation_scales_linearly(self, tmp_path):
        """Test creation time scales linearly"""
        times = []

        for count in [1, 5, 10, 20]:
            start = time.time()

            for i in range(count):
                proj_name = f"scale_{count}_{i}"
                create_project(proj_name, "test", str(tmp_path))

            elapsed = time.time() - start
            times.append(elapsed / count)

        # Average time per project should be consistent
        avg_time = sum(times) / len(times)
        for t in times:
            assert abs(t - avg_time) < avg_time * 0.5, "Non-linear scaling detected"

    def test_registry_scales_with_size(self, tmp_path):
        """Test registry performance with increasing size"""
        registry = Registry()
        times = []

        for size in [10, 50, 100, 200]:
            # Add projects to reach size
            current_size = len(registry.list_projects())
            for i in range(current_size, size):
                proj_name = f"scale_reg_{i}"
                proj_path = tmp_path / proj_name
                proj_path.mkdir(parents=True, exist_ok=True)
                registry.add_project(proj_name, str(proj_path))

            # Measure list operation
            start = time.time()
            registry.list_projects()
            elapsed = time.time() - start
            times.append(elapsed)

        # Should scale sub-linearly (O(n) or better)
        assert times[-1] < times[0] * 20, "Registry doesn't scale well"


class TestConcurrency:
    """Test concurrent operations"""

    def test_concurrent_registry_access(self, tmp_path):
        """Test multiple registry instances"""
        registries = [Registry() for _ in range(5)]

        project_name = "concurrent_test"
        project_path = tmp_path / project_name
        create_project(project_name, "test", str(tmp_path))

        # All registries should work
        for reg in registries:
            reg.add_project(project_name, str(project_path))
            assert project_name in reg.list_projects()

    def test_rapid_operations(self, tmp_path):
        """Test rapid successive operations"""
        registry = Registry()

        # Rapid add/remove cycles
        for i in range(50):
            proj_name = f"rapid_{i}"
            proj_path = tmp_path / proj_name
            proj_path.mkdir(parents=True, exist_ok=True)

            registry.add_project(proj_name, str(proj_path))
            assert proj_name in registry.list_projects()
            registry.remove_project(proj_name)
            assert proj_name not in registry.list_projects()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
