import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pyautogui
import time
import threading

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Typer")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        self.text = ""
        self.typing = False
        self.delay = 0.5

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Auto Typer", font=("Helvetica", 20, "bold"), bg="#f0f4f8").pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, width=70)
        self.text_area.pack(pady=10)

        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.pack()

        self.start_btn = tk.Button(frame, text="Start", width=10, bg="#28a745", fg="white", command=self.start_typing)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = tk.Button(frame, text="Stop", width=10, bg="#dc3545", fg="white", command=self.stop_typing)
        self.stop_btn.grid(row=0, column=1, padx=10)

        self.browse_btn = tk.Button(frame, text="Browse File", width=12, command=self.browse_file)
        self.browse_btn.grid(row=0, column=2, padx=10)

        self.speed_label = tk.Label(self.root, text="Typing Speed (seconds/char):", bg="#f0f4f8")
        self.speed_label.pack(pady=(15, 0))

        self.speed_slider = tk.Scale(self.root, from_=0.01, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, length=300, command=self.update_speed)
        self.speed_slider.set(self.delay)
        self.speed_slider.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.text = f.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, self.text)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}")

    def update_speed(self, val):
        self.delay = float(val)

    def type_text(self):
        time.sleep(5)  # Give user time to focus the desired window
        for char in self.text:
            if not self.typing:
                break
            pyautogui.write(char)
            time.sleep(self.delay)

        self.typing = False

    def start_typing(self):
        self.text = self.text_area.get("1.0", tk.END).strip()
        if not self.text:
            messagebox.showwarning("Warning", "No text to type!")
            return
        self.typing = True
        threading.Thread(target=self.type_text, daemon=True).start()

    def stop_typing(self):
        self.typing = False
        messagebox.showinfo("Stopped", "Typing stopped.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()
