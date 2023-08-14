import tkinter as tk
from tkinter import ttk
import sys, os

def load_settings():
    try:
        if getattr(sys, 'frozen', False): 
            config_path = os.path.join(sys._MEIPASS, 'settings.config')
        else:
            config_path = 'settings.config'  
        with open(config_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                if key == "AUTO_SWITCH_LANGUAGE":
                    chk_language_var.set(value == 'True')
                elif key == "AUTO_SWITCH_CAPSLOCK":
                    chk_capslock_var.set(value == 'True')
    except FileNotFoundError:
        pass

def save_settings():
    with open(config_path, 'w') as f:  # ใช้ mode 'w' เพื่อเขียนทับ
        f.write(f"AUTO_SWITCH_LANGUAGE={chk_language_var.get()}\n")
        f.write(f"AUTO_SWITCH_CAPSLOCK={chk_capslock_var.get()}")

app = tk.Tk()
app.title("Settings")

chk_language_var = tk.BooleanVar()
chk_language = ttk.Checkbutton(app, text="สลับภาษาอัตโนมัติเมื่อแก้ไข", variable=chk_language_var)
chk_language.pack(pady=10)

chk_capslock_var = tk.BooleanVar()
chk_capslock = ttk.Checkbutton(app, text="กด CAPS LOCK อัตโนมัติเมื่อแก้ไข", variable=chk_capslock_var)
chk_capslock.pack(pady=10)

btn_save = ttk.Button(app, text="Save", command=save_settings)
btn_save.pack(pady=20)

def run_gui():
    load_settings()
    app.mainloop()

if __name__ == "__main__":
    run_gui()
