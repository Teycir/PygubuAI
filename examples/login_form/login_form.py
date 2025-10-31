#!/usr/bin/env python3
import tkinter as tk
import pygubu

class LoginForm:
    def __init__(self, master):
        self.builder = pygubu.Builder()
        self.builder.add_from_file('login_form.ui')
        self.mainwindow = self.builder.get_object('mainwindow', master)
        
        self.username_entry = self.builder.get_object('username_entry')
        self.password_entry = self.builder.get_object('password_entry')
        self.remember_check = self.builder.get_object('remember_check')
        self.login_button = self.builder.get_object('login_button')
        self.status_label = self.builder.get_object('status_label')
        
        self.remember_var = tk.BooleanVar()
        self.remember_check.config(variable=self.remember_var)
        
        self.login_button.config(command=self.login)
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        self.username_entry.focus()
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username:
            self.status_label.config(text="Username required")
            return
        
        if not password:
            self.status_label.config(text="Password required")
            return
        
        if username == "admin" and password == "password":
            self.status_label.config(text="Login successful!", foreground="green")
        else:
            self.status_label.config(text="Invalid credentials", foreground="red")
    
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = LoginForm(root)
    app.run()
