# pip install pyautogui

import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import time
import threading
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AutoTyperApp:
    def __init__(self, master):
        self.master = master
        master.title("Created by Anatolie Jentimir")
        master.geometry("1000x900")
        master.configure(bg='#2c3e50')  # Dark blue-gray background
        
        # Set window icon - try different icon files
        try:
            # Try the 32x32 icon first (best for window title bar)
            icon_path = resource_path("assets/app_icon_32×32.ico")
            master.iconbitmap(icon_path)
        except:
            try:
                # Fallback to the 256x256 icon
                icon_path = resource_path("assets/app_icon_256×256.ico")
                master.iconbitmap(icon_path)
            except:
                try:
                    # Final fallback to the main icon
                    icon_path = resource_path("assets/app_icon.ico")
                    master.iconbitmap(icon_path)
                except:
                    # If all fail, continue without custom icon
                    pass
        
        self.typing = False
        self.delay = 0.5
        
        # --- Top button frame ---
        
        self.button_frame = tk.Frame(master, bg='#34495e')  # Slightly lighter blue-gray
        self.button_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.browse_button = tk.Button(self.button_frame, text="Browse Text File", command=self.browse_file,
                                     bg='#7f8c8d', fg='white', font=('Arial', 10, 'bold'),
                                     activebackground='#6c7b7f', activeforeground='white',
                                     relief=tk.RAISED, bd=3, padx=10, pady=5)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.start_button = tk.Button(self.button_frame, text="Start Typing", command=self.start_typing,
                                    bg='#7f8c8d', fg='white', font=('Arial', 10, 'bold'),
                                    activebackground='#6c7b7f', activeforeground='white',
                                    relief=tk.RAISED, bd=3, padx=10, pady=5)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_button = tk.Button(self.button_frame, text="Stop Typing", command=self.stop_typing,
                                   bg='#7f8c8d', fg='white', font=('Arial', 10, 'bold'),
                                   activebackground='#6c7b7f', activeforeground='white',
                                   relief=tk.RAISED, bd=3, padx=10, pady=5)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit_app,
                                   bg='#7f8c8d', fg='white', font=('Arial', 10, 'bold'),
                                   activebackground='#6c7b7f', activeforeground='white',
                                   relief=tk.RAISED, bd=3, padx=10, pady=5)
        self.exit_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.speed_label = tk.Label(self.button_frame, text="Delay (s/char):",
                                  bg='#34495e', fg='white', font=('Arial', 10))
        self.speed_label.pack(side=tk.LEFT, padx=(20, 5), pady=5)
        
        self.speed_scale = tk.Scale(self.button_frame, from_=0.01, to=1.0, resolution=0.01,
                                   orient=tk.HORIZONTAL, length=200, command=self.update_speed,
                                   bg='#34495e', fg='white', activebackground='#3498db',
                                   highlightbackground='#34495e', troughcolor='#2c3e50')
        self.speed_scale.set(self.delay)
        self.speed_scale.pack(side=tk.LEFT, pady=5)
        
        # --- Text editing label ---
        self.edit_label = tk.Label(master, text="Edit your text directly below or load from a file:",
                                 bg='#2c3e50', fg='white', font=('Arial', 12))
        self.edit_label.pack(pady=(10, 5))
        
        # --- Text display with scrollbar ---
        self.text_frame = tk.Frame(master, bg='#2c3e50')
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.text_display = tk.Text(self.text_frame, wrap=tk.WORD,
                                  bg='#ecf0f1', fg='#2c3e50', font=('Consolas', 11),
                                  insertbackground='#2c3e50', selectbackground='#3498db',
                                  selectforeground='white')
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_display.yview,
                                    bg='#34495e', activebackground='#3498db',
                                    troughcolor='#2c3e50')
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_display.config(yscrollcommand=self.scrollbar.set)
        
        # --- Status bar ---
        self.status_bar = tk.Label(master, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                 bg='#34495e', fg='white', font=('Arial', 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                loaded_text = f.read()
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, loaded_text)
            self.update_status("File loaded. You can edit the text before typing.")

    def update_speed(self, value):
        self.delay = float(value)

    def type_text(self):
        time.sleep(5)  # Give user time to switch to target application
        # Get the current text from the text display widget
        text_to_type = self.text_display.get(1.0, tk.END)
        for char in text_to_type:
            if not self.typing:
                break
            pyautogui.write(char)
            time.sleep(self.delay)
        self.typing = False
        if self.typing == False:
            self.update_status("Typing completed or stopped.")

    def start_typing(self):
        # Check if there's any text in the text display
        if not self.text_display.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No text to type! Please enter text or load a file.")
            return
        
        self.update_status("Starting typing in 5 seconds... Switch to your target application!")
        self.typing = True
        threading.Thread(target=self.type_text, daemon=True).start()

    def stop_typing(self):
        self.typing = False
        self.update_status("Typing stopped.")

    def update_status(self, message):
        self.status_bar.config(text=message)

    def exit_app(self):
        self.typing = False
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()