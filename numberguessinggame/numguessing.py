import random
import tkinter as tk
from tkinter import messagebox

# Initialize game variable
number = random.randint(1,100)
attempts = 0

def check_guess():
    global attempts
    try:
        guess = int(entry.get())
        attempts += 1

        if guess < 1 or guess > 100:
            result_label.config(text="⚠️ Enter a number between 1 and 100")
        elif guess < number:
            result_label.config(text="📉 Too low! Try again.")
        elif guess > number:
            result_label.config(text="📈 Too high! Try again.")
        else:
            messagebox.showinfo("🎉 Success!", f"You guessed it in {attempts} attempts!")
            reset_game()

    except ValueError:
        result_label.config(text="❌ Please enter a valid number")

def reset_game():
    global number, attempts
    number = random.randint(1, 100)
    attempts = 0
    entry.delete(0, tk.END)
    result_label.config(text="Game reset! Start guessing...")




# Create window
root = tk.Tk()
root.title("Guess the Number Game")
root.geometry("350x250")

# Title
title_label = tk.Label(root, text="🎯 Guess the Number!", font=("Arial", 16))
title_label.pack(pady=10)

# Instructions
instruction_label = tk.Label(root, text="Guess a number between 1 and 100")
instruction_label.pack()

# Input field
entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=10)

# Guess button
guess_button = tk.Button(root, text="Submit Guess", command=check_guess)
guess_button.pack()

# Result label
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Reset button
reset_button = tk.Button(root, text="Reset Game", command=reset_game)
reset_button.pack()

# Run app
root.mainloop()