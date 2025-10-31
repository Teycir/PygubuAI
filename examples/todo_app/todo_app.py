#!/usr/bin/env python3
import tkinter as tk
import pygubu

class TodoApp:
    def __init__(self, master):
        self.builder = pygubu.Builder()
        self.builder.add_from_file('todo_app.ui')
        self.mainwindow = self.builder.get_object('mainwindow', master)
        
        self.task_entry = self.builder.get_object('task_entry')
        self.task_listbox = self.builder.get_object('task_listbox')
        self.scrollbar = self.builder.get_object('scrollbar')
        self.counter_label = self.builder.get_object('counter_label')
        self.add_button = self.builder.get_object('add_button')
        self.delete_button = self.builder.get_object('delete_button')
        self.clear_button = self.builder.get_object('clear_button')
        
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)
        
        self.add_button.config(command=self.add_task)
        self.delete_button.config(command=self.delete_task)
        self.clear_button.config(command=self.clear_all)
        
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        self.update_counter()
    
    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.update_counter()
    
    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            self.task_listbox.delete(selection[0])
            self.update_counter()
    
    def clear_all(self):
        self.task_listbox.delete(0, tk.END)
        self.update_counter()
    
    def update_counter(self):
        count = self.task_listbox.size()
        text = f"{count} task{'s' if count != 1 else ''}"
        self.counter_label.config(text=text)
    
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = TodoApp(root)
    app.run()
