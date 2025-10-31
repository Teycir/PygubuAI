#!/usr/bin/env python3
"""Quick preview tool for UI files"""
import tkinter as tk
from .registry import Registry


def preview_ui(ui_file_path: str, watch: bool = False):
    """Preview UI file in Tkinter window"""
    from .errors import DependencyError, UIParseError, FileOperationError
    from .utils import validate_safe_path

    try:
        import pygubu
    except ImportError as e:
        raise DependencyError("pygubu", "pip install pygubu>=0.39") from e

    try:
        ui_path = validate_safe_path(ui_file_path, must_exist=True)
    except ValueError as e:
        raise FileOperationError("read", ui_file_path, e) from e

    last_mtime = ui_path.stat().st_mtime

    def create_window():
        root = tk.Tk()
        root.title(f"Preview: {ui_path.name}")

        builder = pygubu.Builder()
        try:
            builder.add_from_file(str(ui_path))
            builder.get_object('mainwindow', root)
        except (KeyError, AttributeError) as e:
            # If mainwindow not found, try first object
            try:
                builder.add_from_file(str(ui_path))
                first_obj = list(builder.objects.keys())[0] if builder.objects else None
                if first_obj:
                    builder.get_object(first_obj, root)
                else:
                    raise UIParseError(str(ui_path), "No objects found in UI file") from e
            except (KeyError, AttributeError, IndexError) as e2:
                tk.Label(root, text=f"Error loading UI:\n{str(e2)}", fg="red", padx=20, pady=20).pack()
        except Exception as e:
            raise UIParseError(str(ui_path), f"Failed to load UI: {e}") from e

        if watch:
            def check_changes():
                nonlocal last_mtime
                try:
                    current_mtime = ui_path.stat().st_mtime
                    if current_mtime != last_mtime:
                        last_mtime = current_mtime
                        root.destroy()
                        create_window()
                except (OSError, PermissionError) as e:
                    # File may be temporarily unavailable during write
                    import logging
                    logging.debug(f"Temporary error checking file: {e}")
                except tk.TclError:
                    # Window already destroyed
                    return
                root.after(1000, check_changes)

            root.after(1000, check_changes)

        return root

    root = create_window()
    root.mainloop()


def preview_project(project_name: str, watch: bool = False):
    """Preview project by name"""
    from .errors import ProjectNotFoundError
    from .utils import validate_safe_path

    registry = Registry()
    project_path = registry.get_project(project_name)

    if not project_path:
        raise ProjectNotFoundError(project_name)

    safe_path = validate_safe_path(project_path, must_exist=True, must_be_dir=True)
    ui_file = safe_path / f"{project_name}.ui"

    if not ui_file.exists():
        raise FileNotFoundError(f"UI file not found: {ui_file}")

    preview_ui(str(ui_file), watch)


def main():
    """CLI entry point"""
    import sys
    import logging
    from .errors import PygubuAIError

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger(__name__)

    if len(sys.argv) < 2:
        print("Usage: pygubu-preview <project_name|file.ui> [--watch]")
        print("\nOptions:")
        print("  --watch    Auto-reload on file changes")
        sys.exit(1)

    target = sys.argv[1]
    watch = "--watch" in sys.argv

    try:
        if target.endswith('.ui'):
            preview_ui(target, watch)
        else:
            preview_project(target, watch)
    except PygubuAIError as e:
        logger.error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\nPreview stopped")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
