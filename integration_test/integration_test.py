#!/usr/bin/env python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "integration_test.ui"

class IntegrationTestApp:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_from_file(PROJECT_UI)
        self.mainwindow = self.builder.get_object('mainwindow', master)
        self.builder.connect_callbacks(self)

    def on_add(self):
        """Handle on_add event."""
        pass

    def on_update(self):
        """Handle on_update event."""
        pass

    def on_delete(self):
        """Handle on_delete event."""
        pass


    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = IntegrationTestApp()
    app.run()
