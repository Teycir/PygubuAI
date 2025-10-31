"""Progress indicators for long operations"""
import sys
import time
from typing import Optional


class ProgressBar:
    """Simple progress bar for CLI"""

    def __init__(self, total: int, prefix: str = "", width: int = 40):
        self.total = total
        self.current = 0
        self.prefix = prefix
        self.width = width
        self.start_time = time.time()

    def update(self, amount: int = 1):
        """Update progress"""
        self.current += amount
        self._render()

    def _render(self):
        """Render progress bar"""
        if self.total == 0:
            return

        percent = self.current / self.total
        filled = int(self.width * percent)
        bar = "=" * filled + ">" + " " * (self.width - filled - 1)

        # elapsed = time.time() - self.start_time
        # rate = self.current / elapsed if elapsed > 0 else 0

        sys.stdout.write(f"\r{self.prefix} [{bar}] {percent*100:.0f}% ({self.current}/{self.total})")
        sys.stdout.flush()

        if self.current >= self.total:
            sys.stdout.write("\n")
            sys.stdout.flush()


class Spinner:
    """Simple spinner for indeterminate operations"""

    def __init__(self, message: str = "Processing"):
        self.message = message
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current = 0
        self.running = False

    def start(self):
        """Start spinner"""
        self.running = True
        self._render()

    def stop(self, final_message: Optional[str] = None):
        """Stop spinner"""
        self.running = False
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        if final_message:
            sys.stdout.write(final_message + "\n")
        sys.stdout.flush()

    def _render(self):
        """Render spinner frame"""
        if not self.running:
            return
        frame = self.frames[self.current % len(self.frames)]
        sys.stdout.write(f"\r{frame} {self.message}...")
        sys.stdout.flush()
        self.current += 1
