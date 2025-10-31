#!/usr/bin/env python3
import tkinter as tk
import pygubu

class SettingsDialog:
    def __init__(self, master):
        self.builder = pygubu.Builder()
        self.builder.add_from_file('settings_dialog.ui')
        self.mainwindow = self.builder.get_object('mainwindow', master)
        
        self.notebook = self.builder.get_object('notebook')
        self.general_tab = self.builder.get_object('general_tab')
        self.advanced_tab = self.builder.get_object('advanced_tab')
        
        self.auto_save_var = tk.BooleanVar(value=True)
        self.notifications_var = tk.BooleanVar(value=True)
        self.debug_var = tk.BooleanVar(value=False)
        
        self.builder.get_object('auto_save_check').config(variable=self.auto_save_var)
        self.builder.get_object('notifications_check').config(variable=self.notifications_var)
        self.builder.get_object('debug_check').config(variable=self.debug_var)
        
        self.theme_combo = self.builder.get_object('theme_combo')
        self.theme_combo.current(0)
        
        self.cache_scale = self.builder.get_object('cache_scale')
        self.cache_value_label = self.builder.get_object('cache_value_label')
        self.cache_scale.config(command=self.update_cache_label)
        self.cache_scale.set(100)
        
        self.notebook.add(self.general_tab, text="General")
        self.notebook.add(self.advanced_tab, text="Advanced")
    
    def update_cache_label(self, value):
        self.cache_value_label.config(text=f"{int(float(value))}")
    
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = SettingsDialog(root)
    app.run()
