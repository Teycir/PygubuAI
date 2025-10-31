#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("300x400")
        
        self.current = ""
        self.operation = None
        self.previous = None
        
        main_frame = ttk.Frame(master, padding=10)
        main_frame.pack(expand=True, fill='both')
        
        self.display = ttk.Entry(main_frame, font=('Arial', 18), justify='right', state='readonly')
        self.display.pack(fill='x', pady=(0, 10))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(expand=True, fill='both')
        
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
        ]
        
        for (text, row, col) in buttons:
            cmd = lambda t=text: self.button_click(t)
            btn = ttk.Button(button_frame, text=text, command=cmd)
            btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        ttk.Button(button_frame, text='C', command=self.clear).grid(row=4, column=0, columnspan=2, sticky='nsew', padx=2, pady=2)
        ttk.Button(button_frame, text='Back', command=self.backspace).grid(row=4, column=2, columnspan=2, sticky='nsew', padx=2, pady=2)
        
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.rowconfigure(i, weight=1)
    
    def button_click(self, char):
        if char in '0123456789':
            self.current += char
            self.update_display()
        elif char == '.':
            if '.' not in self.current:
                self.current += '.'
                self.update_display()
        elif char in '+-*/':
            if self.current:
                if self.previous is not None and self.operation:
                    self.calculate()
                self.previous = float(self.current)
                self.current = ""
                self.operation = char
        elif char == '=':
            self.calculate()
    
    def calculate(self):
        if self.current and self.previous is not None and self.operation:
            try:
                current_num = float(self.current)
                if self.operation == '+':
                    result = self.previous + current_num
                elif self.operation == '-':
                    result = self.previous - current_num
                elif self.operation == '*':
                    result = self.previous * current_num
                elif self.operation == '/':
                    if current_num == 0:
                        self.current = "Error"
                        self.update_display()
                        self.previous = None
                        self.operation = None
                        return
                    result = self.previous / current_num
                
                self.current = str(result)
                self.previous = None
                self.operation = None
                self.update_display()
            except:
                self.current = "Error"
                self.update_display()
    
    def clear(self):
        self.current = ""
        self.previous = None
        self.operation = None
        self.update_display()
    
    def backspace(self):
        self.current = self.current[:-1]
        self.update_display()
    
    def update_display(self):
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current)
        self.display.config(state='readonly')

if __name__ == '__main__':
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
