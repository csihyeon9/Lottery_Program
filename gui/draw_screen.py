import tkinter as tk
import random
import time

class DrawScreen:
    def __init__(self, parent, candidates, final_winner):
        self.parent = parent
        self.candidates = candidates
        self.final_winner = final_winner

        self.window = tk.Toplevel(parent)
        self.window.attributes("-fullscreen", True)
        self.window.configure(bg="black")

        self.label = tk.Label(
            self.window,
            text="",
            font=("맑은 고딕", 60, "bold"),
            fg="white",
            bg="black"
        )
        self.label.pack(expand=True)

        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def start_animation(self):
        self.animate(20, 0.05)

    def animate(self, rounds, delay):
        if rounds <= 0:
            self.show_winner()
            return

        name = random.choice(self.candidates)
        self.label.config(text=name)
        self.window.update()

        self.window.after(
            int(delay * 1000),
            lambda: self.animate(rounds - 1, delay + 0.03)
        )

    def show_winner(self):
        self.label.config(
            text=f"🎉 {self.final_winner} 🎉",
            fg="yellow"
        )
