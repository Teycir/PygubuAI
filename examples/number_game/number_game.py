#!/usr/bin/env python3
"""
number guessing game with entry, submit button, and result label

AI Workflow:
- Edit UI: ~/pygubu-designer number_game.ui
- Watch changes: ~/pygubu-ai-workflow watch number_game
- Ask AI to sync code after UI changes
"""
import pathlib
import tkinter as tk
import pygubu
import random

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "number_game.ui"

class NumberGameApp:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_from_file(PROJECT_UI)
        self.mainwindow = self.builder.get_object('mainwindow', master)
        self.builder.connect_callbacks(self)
        
        # Get widgets
        self.guess_entry = self.builder.get_object('guess_entry')
        self.result_label = self.builder.get_object('result_label')
        self.attempts_label = self.builder.get_object('attempts_label')
        self.hint_label = self.builder.get_object('hint_label')
        self.guess_button = self.builder.get_object('guess_button')
        self.reset_button = self.builder.get_object('reset_button')
        
        # Connect buttons
        self.guess_button.config(command=self.on_guess)
        self.reset_button.config(command=self.on_reset)
        
        # Game state
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        
        # Bind Enter key
        self.guess_entry.bind('<Return>', lambda e: self.on_guess())
    
    def on_guess(self):
        """Handle guess submission"""
        # Guard against guesses after win
        if self.guess_entry.cget('state') == 'disabled':
            return
        
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1
            self.attempts_label.config(text=f"Attempts: {self.attempts}")
            
            if guess < 1 or guess > 100:
                self.result_label.config(text="Please enter 1-100!", foreground="orange")
            elif guess < self.secret_number:
                self.result_label.config(text="📈 Too low! Try higher", foreground="#ff6b6b")
                self.hint_label.config(text=f"Hint: Number is between {guess} and 100")
            elif guess > self.secret_number:
                self.result_label.config(text="📉 Too high! Try lower", foreground="#ff6b6b")
                self.hint_label.config(text=f"Hint: Number is between 1 and {guess}")
            else:
                self.result_label.config(text=f"🎉 YOU WIN! It was {self.secret_number}!", foreground="#51cf66")
                self.hint_label.config(text=f"You got it in {self.attempts} attempts!")
                self.guess_entry.config(state='disabled')
                self.guess_button.config(state='disabled')
            
            self.guess_entry.delete(0, tk.END)
        except ValueError:
            self.result_label.config(text="Please enter a valid number!", foreground="orange")
    
    def on_reset(self):
        """Start new game"""
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.attempts_label.config(text="Attempts: 0")
        self.result_label.config(text="Make your guess!", foreground="#0066cc")
        self.hint_label.config(text="I'm thinking of a number...")
        self.guess_entry.config(state='normal')
        self.guess_button.config(state='normal')
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
    
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = NumberGameApp()
    app.run()
