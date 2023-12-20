import logging
import datetime
import os
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

def setup_logger():
    logger = logging.getLogger('decision_logger')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_path = os.path.expanduser("~/Documents/_decision/decision.log")
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def decision_logger(logger, name, message):
    if message.strip() == "":
        return
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{current_time} - {name} - {message}"
    if log_message not in logged_messages:

        with open(os.path.expanduser("~/Documents/_decision/decision.log"), "a") as f:
            f.write(log_message + "\n")
        logged_messages.add(log_message)
    else:
        return

def validate_entry(entry):
    if entry.get().strip() == "":
        return False
    return True

def log_decision():
    if log_button['state'] == 'disabled':
        return
    log_button['state'] = 'disabled'  # Disable the button to prevent multiple clicks
    if not validate_entry(name_entry) or not validate_entry(message_entry):
        log_button['state'] = 'normal'  # Enable the button
        return
    name = name_entry.get()
    message = message_entry.get()
    decision_logger(logger, name, message)
    name_entry.delete(0, tk.END)
    message_entry.delete(0, tk.END)
    update_log_text()
    log_button['state'] = 'normal'  # Enable the button

def clear_log():
    result = messagebox.askyesno("Clear Log", "Are you sure you want to clear the log?")
    if result == tk.YES:
        with open(os.path.expanduser("~/Documents/_decision/decision.log"), "w") as f:
            f.write("")
        logged_messages.clear()
        update_log_text()

def search_log():
    search_query = search_entry.get().strip()
    if search_query == "":
        return
    search_results = []
    with open(os.path.expanduser("~/Documents/_decision/decision.log"), "r") as f:
        for line in f:
            if search_query in line:
                search_results.append(line)
    display_search_results(search_results)

def display_search_results(search_results):
    search_window = tk.Toplevel(root)
    search_window.title("Search Results")
    search_window.geometry("600x400")

    search_text = ScrolledText(search_window, height=20, width=80, font=("Arial", 12))
    search_text.pack(padx=10, pady=10)

    if len(search_results) == 0:
        search_text.insert(tk.END, "No results found.")
    else:
        for result in search_results:
            search_text.insert(tk.END, result)

def update_log_text():
    log_text.delete("1.0", tk.END)
    with open(os.path.expanduser("~/Documents/_decision/decision.log"), "r") as f:
        log_text.insert(tk.END, f.read())

logger = setup_logger()
logged_messages = set()

root = tk.Tk()
root.title("Decision Logger")

# Get window width and height
window_width = root.winfo_screenwidth() // 2
window_height = root.winfo_screenheight() // 2

# Set GUI elements
name_label = tk.Label(root, text="Name:", font=("Arial", 12))
name_label.place(x=10, y=10)

name_entry = tk.Entry(root, width=int(window_width * 0.9), font=("Arial", 12))
name_entry.place(x=10, y=30)
name_entry.config(validate="all", validatecommand=(root.register(validate_entry), "%P"))

message_label = tk.Label(root, text="Decision:", font=("Arial", 12))
message_label.place(x=10, y=70)

message_entry = tk.Entry(root, width=int(window_width * 0.9), font=("Arial", 12))
message_entry.place(x=10, y=90)
message_entry.config(validate="all", validatecommand=(root.register(validate_entry), "%P"))

log_button = tk.Button(root, text="Log Decision", command=log_decision, width=30, font=("Arial", 12))
log_button.place(x=window_width // 2 - 75, y=130)

clear_button = tk.Button(root, text="Clear Log", command=clear_log, width=30, font=("Arial", 12))
clear_button.place(x=window_width // 2 - 75, y=170)

search_label = tk.Label(root, text="Search (yyyy-mm-dd) | name:", font=("Arial", 12))
search_label.place(x=10, y=210)

search_entry = tk.Entry(root, width=int(window_width * 0.9), font=("Arial", 12))
search_entry.place(x=10, y=240)

search_button = tk.Button(root, text="Search", command=search_log, width=30, font=("Arial", 12))
search_button.place(x=window_width // 2 - 75, y=280)

log_label = tk.Label(root, text="Log:", font=("Arial", 12))
log_label.place(x=10, y=320)

log_text = ScrolledText(root, height=10, width=150, font=("Arial", 12))
log_text.place(x=10, y=350)
log_text.configure(state="normal")
log_text.configure(wrap="word")

update_log_text()

# Increase the text area to view and edit the log entries another 50% of its original size to fit the window
text_field_height = window_height - 300
log_text.place(x=10, y=350, width=window_width , height=text_field_height)

root.geometry(f"{window_width}x{window_height}")
root.mainloop()