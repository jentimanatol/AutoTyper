import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import time
import threading

class AutoTyperApp:
    def __init__(self, master):
        self.master = master
        master.title("Auto Typer")
        master.geometry("500x300")

        self.text = ""
        self.typing = False
        self.delay = 0.5

        self.label = tk.Label(master, text="Auto Typer with Delay")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(master, text="Browse Text File", command=self.browse_file)
        self.browse_button.pack()

        self.start_button = tk.Button(master, text="Start Typing", command=self.start_typing)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop Typing", command=self.stop_typing)
        self.stop_button.pack()

        self.speed_label = tk.Label(master, text="Delay (seconds per character):")
        self.speed_label.pack(pady=(20, 0))

        self.speed_scale = tk.Scale(master, from_=0.01, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, length=200, command=self.update_speed)
        self.speed_scale.set(self.delay)
        self.speed_scale.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.text = f.read()
            messagebox.showinfo("Success", "File loaded. Ready to type!")

    def update_speed(self, value):
        self.delay = float(value)

    def type_text(self):
        time.sleep(5)
        for char in self.text:
            if not self.typing:
                break
            pyautogui.write(char)
            time.sleep(self.delay)
        self.typing = False

    def start_typing(self):
        if not self.text:
            messagebox.showwarning("Warning", "No text loaded!")
            return
        self.typing = True
        threading.Thread(target=self.type_text, daemon=True).start()

    def stop_typing(self):
        self.typing = False
        messagebox.showinfo("Stopped", "Typing stopped.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()
