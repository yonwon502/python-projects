import customtkinter as ctk
import json
import os

# Set appearance and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern Python TODO")
        self.geometry("500x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.tasks = []
        self.task_file = "tasks.json"
        self.load_tasks()

        # --- UI Elements ---
        
        # Header
        self.header_label = ctk.CTkLabel(self, text="My Tasks", font=ctk.CTkFont(size=30, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Input Frame
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter a new task...", height=40)
        self.task_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.add_button = ctk.CTkButton(self.input_frame, text="Add Task", width=100, height=40, font=ctk.CTkFont(weight="bold"), command=self.add_task)
        self.add_button.grid(row=0, column=1)

        # Scrollable Task List
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Your TODO List")
        self.scrollable_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.render_tasks()

    def load_tasks(self):
        if os.path.exists(self.task_file):
            try:
                with open(self.task_file, "r") as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                self.tasks = []

    def save_tasks(self):
        with open(self.task_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False})
            self.task_entry.delete(0, "end")
            self.save_tasks()
            self.render_tasks()

    def toggle_task(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_tasks()
        self.render_tasks()

    def delete_task(self, index):
        self.tasks.pop(index)
        self.save_tasks()
        self.render_tasks()

    def render_tasks(self):
        # Clear existing tasks in the frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for i, task in enumerate(self.tasks):
            task_row = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            task_row.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
            task_row.grid_columnconfigure(0, weight=1)

            # Checkbox
            checkbox = ctk.CTkCheckBox(task_row, text=task["text"], 
                                         command=lambda idx=i: self.toggle_task(idx))
            if task["completed"]:
                checkbox.select()
                checkbox.configure(font=ctk.CTkFont(slant="italic"), text_color="gray")
            else:
                checkbox.deselect()
            
            checkbox.grid(row=0, column=0, sticky="w", padx=10)

            # Delete Button
            delete_btn = ctk.CTkButton(task_row, text="Delete", width=60, height=25, 
                                        fg_color="#e74c3c", hover_color="#c0392b",
                                        command=lambda idx=i: self.delete_task(idx))
            delete_btn.grid(row=0, column=1, padx=5)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
