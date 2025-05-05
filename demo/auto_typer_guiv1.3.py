import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import time
import threading

class AutoTyperApp:
    def __init__(self, master):
        self.master = master
        master.title("Created by Anatolie Jentimir")
        master.geometry("1800x1200")

        self.text = ""
        self.typing = False
        self.delay = 0.5

        # --- Top button frame ---
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        self.browse_button = tk.Button(self.button_frame, text="Browse Text File", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(self.button_frame, text="Start Typing", command=self.start_typing)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Stop Typing", command=self.stop_typing)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit_app)
        self.exit_button.pack(side=tk.LEFT, padx=5)

        self.speed_label = tk.Label(self.button_frame, text="Delay (s/char):")
        self.speed_label.pack(side=tk.LEFT, padx=(20, 5))

        self.speed_scale = tk.Scale(self.button_frame, from_=0.01, to=1.0, resolution=0.01,
                                    orient=tk.HORIZONTAL, length=200, command=self.update_speed)
        self.speed_scale.set(self.delay)
        self.speed_scale.pack(side=tk.LEFT)

        # --- Text display with scrollbar ---
        self.text_frame = tk.Frame(master)
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text_display = tk.Text(self.text_frame, wrap=tk.WORD)
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_display.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_display.config(yscrollcommand=self.scrollbar.set)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.text = f.read()
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, self.text)
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

    def exit_app(self):
        self.typing = False
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()
