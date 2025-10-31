#!/usr/bin/env python3
import tkinter as tk
import pygubu

class Calculator:
    def __init__(self, master):
        self.builder = pygubu.Builder()
        self.builder.add_from_file('calculator.ui')
        self.mainwindow = self.builder.get_object('mainwindow', master)
        
        self.display = self.builder.get_object('display')
        self.current = ""
        self.operation = None
        self.previous = None
        
        for i in range(10):
            btn = self.builder.get_object(f'btn_{i}')
            btn.config(command=lambda n=i: self.append_number(n))
        
        self.builder.get_object('btn_add').config(command=lambda: self.set_operation('+'))
        self.builder.get_object('btn_sub').config(command=lambda: self.set_operation('-'))
        self.builder.get_object('btn_mul').config(command=lambda: self.set_operation('*'))
        self.builder.get_object('btn_div').config(command=lambda: self.set_operation('/'))
        self.builder.get_object('btn_equals').config(command=self.calculate)
        self.builder.get_object('btn_dot').config(command=self.append_dot)
        self.builder.get_object('btn_clear').config(command=self.clear)
        self.builder.get_object('btn_back').config(command=self.backspace)
        
        self.display.config(state='readonly')
    
    def append_number(self, num):
        self.current += str(num)
        self.update_display()
    
    def append_dot(self):
        if '.' not in self.current:
            self.current += '.'
            self.update_display()
    
    def set_operation(self, op):
        if self.current:
            if self.previous is not None and self.operation:
                self.calculate()
            self.previous = float(self.current)
            self.current = ""
            self.operation = op
    
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
    
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Calculator(root)
    app.run()
