#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import pygubu

class DataViewer:
    def __init__(self, master):
        self.builder = pygubu.Builder()
        self.builder.add_from_file('data_viewer.ui')
        self.mainwindow = self.builder.get_object('mainwindow', master)
        
        self.data_tree = self.builder.get_object('data_tree')
        self.tree_scrollbar = self.builder.get_object('tree_scrollbar')
        self.search_entry = self.builder.get_object('search_entry')
        self.status_label = self.builder.get_object('status_label')
        self.count_label = self.builder.get_object('count_label')
        
        self.data_tree.config(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.config(command=self.data_tree.yview)
        
        self.data_tree.heading('#0', text='ID')
        self.data_tree.heading('name', text='Name')
        self.data_tree.heading('age', text='Age')
        self.data_tree.heading('city', text='City')
        
        self.data_tree.column('#0', width=50)
        self.data_tree.column('name', width=150)
        self.data_tree.column('age', width=80)
        self.data_tree.column('city', width=150)
        
        self.builder.get_object('load_button').config(command=self.load_data)
        self.builder.get_object('refresh_button').config(command=self.refresh_data)
        self.builder.get_object('search_button').config(command=self.search_data)
        
        self.sample_data = [
            (1, 'Alice Johnson', 28, 'New York'),
            (2, 'Bob Smith', 35, 'Los Angeles'),
            (3, 'Carol White', 42, 'Chicago'),
            (4, 'David Brown', 31, 'Houston'),
            (5, 'Eve Davis', 26, 'Phoenix'),
        ]
        
        self.load_data()
    
    def load_data(self):
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        for row in self.sample_data:
            self.data_tree.insert('', 'end', text=str(row[0]), 
                                values=(row[1], row[2], row[3]))
        
        self.update_count()
        self.status_label.config(text='Data loaded')
    
    def refresh_data(self):
        self.load_data()
        self.status_label.config(text='Data refreshed')
    
    def search_data(self):
        query = self.search_entry.get().lower()
        if not query:
            self.load_data()
            return
        
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        for row in self.sample_data:
            if query in str(row).lower():
                self.data_tree.insert('', 'end', text=str(row[0]), 
                                    values=(row[1], row[2], row[3]))
        
        self.update_count()
        self.status_label.config(text=f'Search: {query}')
    
    def update_count(self):
        count = len(self.data_tree.get_children())
        self.count_label.config(text=f'{count} records')
    
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = DataViewer(root)
    app.run()
