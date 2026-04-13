import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import re
from langdetect import detect
import datetime
import time

# Text Processing Functions

def preprocess_text(text):
    return re.findall(r'\w+', text.lower())

def basic_stats(text):
    words = preprocess_text(text)
    return {
        'word_count': len(words),
        'unique_words': len(set(words)),
        'average_word_length': sum(len(word) for word in words) / len(words) if words else 0,
        'character_count': len(text),
        'whitespace_count': len(re.findall(r'\s', text)),
        'sentence_count': len(re.split(r'[.!?]+', text)),
        'paragraph_count': len(re.split(r'\n\s*\n', text)) if text.strip() else 0,
        'language': detect_language(text),
        'word_frequency': Counter(words).most_common(10),
    }

def word_frequency(words):
    return Counter(words)

# Language Detection   
def detect_language(text):
    if not text.strip():
        return "Unknown"
    try:
        return detect(text)
    except:
        return "Unknown"

start_time = time.time()

# Real-time Analysis 
def analyze_text(event=None):
    text = text_area.get("1.0", tk.END).strip()
    
    stats = basic_stats(text)
    
    # Update stats
    lines_count = text.count('\n') + 1 if text else 0
    lines_label.config(text=f"Lines: {lines_count}")
    words_label.config(text=f"Words: {stats['word_count']}")
    characters_label.config(text=f"Characters: {stats['character_count']}")

    # Language
    lang = detect_language(text)
    lang_label.config(text=f"Language: {lang}")

    # Typing speed
    update_typing_speed()

# Typing speed (WPM)
def update_typing_speed():
    global start_time
    text = text_area.get("1.0", tk.END).strip()
    words = len(text.split())

    elapsed_time = time.time() - start_time
    minutes = elapsed_time / 60 if elapsed_time > 0 else 1

    wpm = int(words / minutes)
    speed_label.config(text=f"Speed: {wpm} WPM")

# File loader
def load_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                text_area.delete("1.0", tk.END)
                text_area.insert("1.0", text)
                global start_time
                start_time = time.time() # Reset typing speed for loaded file
                analyze_text()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {e}")
        
# Save Report
def save_report():
    text = text_area.get("1.0", tk.END)
    stats = basic_stats(text)
    
    lines_count = text.count('\n') + 1 if text else 0
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prompt user for a save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        initialfile="analysis_report.txt"
    )

    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                # Original Text
                file.write("\n📝 ORIGINAL TEXT:\n")
                file.write("-" * 50 + "\n")
                file.write(text.strip() + "\n")
                
                file.write(f"\nTime: {current_time}\n")
                file.write("TEXT ANALYSIS REPORT\n")
                file.write("=" * 40 + "\n")
                file.write(f"Lines: {lines_count}\n")
                file.write(f"Words: {stats['word_count']}\n")
                file.write(f"Characters: {stats['character_count']}\n")
                file.write(f"Unique Words: {stats['unique_words']}\n")
                file.write(f"Average Word Length: {stats['average_word_length']:.2f}\n")
                file.write(f"Language: {stats['language']}\n")
                
                file.write("\n--- WORD FREQUENCY ---\n")
                for word, freq in stats['word_frequency']:
                    file.write(f"{word}: {freq}\n")

            messagebox.showinfo("Saved", f"Report successfully saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {e}")

# GUI Setup
root = tk.Tk()
root.title("Advanced Text Analyzer")
root.geometry("900x600")

# Info Frame

frame = tk.Frame(root)
frame.pack(pady=10)

# Labels
lines_label = tk.Label(frame, text="Lines: 0", font=("Arial", 12))
lines_label.pack()

words_label = tk.Label(frame, text="Words: 0", font=("Arial", 12))
words_label.pack()

characters_label = tk.Label(frame, text="Characters: 0", font=("Arial", 12))
characters_label.pack()

lang_label = tk.Label(frame, text="Language: Unknown", font=("Arial", 12))
lang_label.pack()

speed_label = tk.Label(frame, text="Speed: 0 WPM", font=("Arial", 12))
speed_label.pack()

# Text Area
text_area = tk.Text(root, height=10, width=60, font=("Arial", 12))
text_area.pack()
text_area.bind("<KeyRelease>", analyze_text)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

load_button = tk.Button(btn_frame, text="Load File", command=load_file)
load_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(btn_frame, text="Save Report", command=save_report)
save_button.pack(side=tk.LEFT, padx=5)

# Start
try:
    root.mainloop()
except KeyboardInterrupt:
    pass
        
    
