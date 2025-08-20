# ui.py

import tkinter as tk
from tkinter import messagebox

class CookingAssistantUI:
    def __init__(self, steps, speak_function=None):
        self.steps = steps
        self.current_step = 0
        self.speak_function = speak_function

        self.window = tk.Tk()
        self.window.title("Smart Cooking Assistant")
        self.window.geometry("600x400")
        self.window.config(bg="#fff")

        self.text_area = tk.Text(self.window, wrap=tk.WORD, font=("Arial", 14), bg="#f9f9f9", fg="#333")
        self.text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        button_frame = tk.Frame(self.window, bg="#fff")
        button_frame.pack(pady=10)

        self.next_button = tk.Button(button_frame, text="Next Step ➡️", command=self.next_step, width=15)
        self.next_button.grid(row=0, column=0, padx=10)

        self.repeat_button = tk.Button(button_frame, text="🔁 Repeat Step", command=self.repeat_step, width=15)
        self.repeat_button.grid(row=0, column=1, padx=10)

        self.show_current_step()

    def show_current_step(self):
        if self.current_step < len(self.steps):
            step_text = self.steps[self.current_step]
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, step_text)

            if self.speak_function:
                self.speak_function(step_text)
        else:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "🎉 You have completed the recipe!")
            messagebox.showinfo("Completed", "You have finished cooking!")

    def next_step(self):
        self.current_step += 1
        self.show_current_step()

    def repeat_step(self):
        self.show_current_step()

    def run(self):
        self.window.mainloop()
