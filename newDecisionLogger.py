import sqlite3
import datetime
import tkinter as tk
import tkmacosx as tkm
import threading
import cProfile
from tkinter import ttk, messagebox
from tkcalendar import Calendar

# Database setup and connection
conn = sqlite3.connect('decision_log.db', check_same_thread=False)  # Allow multi-threaded access

def setup_database():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS decisions (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    area TEXT,
                    decision_maker TEXT,
                    decision TEXT,
                    reasoning TEXT,
                    status TEXT,
                    due_date DATE
                )''')
    conn.commit()

def execute_db_query(query, parameters=()):
    c = conn.cursor()
    c.execute(query, parameters)
    if query.lstrip().upper().startswith("SELECT"):
        return c.fetchall()
    conn.commit()


# Logging decisions
def log_decision(area, decision_maker, decision, reasoning, status, due_date):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = conn.cursor()
    c.execute('''
        INSERT INTO decisions (timestamp, area, decision_maker, decision, reasoning, status, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, area, decision_maker, decision, reasoning, status, due_date))
    conn.commit()


# Update decision
def update_decision(id, area, decision_maker, decision, reasoning, status, due_date):
    c = conn.cursor()
    c.execute('''
        UPDATE decisions
        SET area = ?, decision_maker = ?, decision = ?, reasoning = ?, status = ?, due_date = ?
        WHERE id = ?
    ''', (area, decision_maker, decision, reasoning, status, due_date, id))
    conn.commit()
   

# Delete decision
def delete_decision(id):
    c = conn.cursor()
    c.execute('DELETE FROM decisions WHERE id = ?', (id,))
    conn.commit()
   

# Retrieve decisions with optional filters
import datetime

def convert_date_format(date_str):
    """Converts DD-MM-YYYY to MM-DD-YYYY format."""
    return datetime.datetime.strptime(date_str, "%d-%m-%Y").strftime("%m/%d/%Y")

def retrieve_decisions(status_filter=None, start_date=None, end_date=None):
    query = 'SELECT * FROM decisions'
    filters = []

    # Simplified conditional logic
    if status_filter:
        query += ' WHERE status = ?'
        filters.append(status_filter)
    if start_date:
        query += ' AND' if filters else ' WHERE'
        query += ' due_date >= ?'
        filters.append(start_date)
    if end_date:
        query += ' AND' if filters else ' WHERE'
        query += ' due_date <= ?'
        filters.append(end_date)

    return execute_db_query(query, tuple(filters))



# Threaded GUI functions
def update_treeview(decisions):
    # Clear existing rows
    decision_tree.delete(*decision_tree.get_children())
    # Populate the treeview with new data
    for decision in decisions:
        decision_tree.insert('', 'end', values=decision)

def retrieve_decisions_threaded(status_filter=None, start_date=None, end_date=None):
    # This function will run in a separate thread
    decisions = retrieve_decisions(status_filter, start_date, end_date)
    # After retrieving decisions, update the GUI from the main thread
    root.after(0, lambda: update_treeview(decisions))

def refresh_decision_view(status_filter=None, start_date=None, end_date=None):

       # Start the retrieve_decisions operation in a separate thread
    thread = threading.Thread(target=retrieve_decisions_threaded, args=(status_filter, start_date, end_date))
    thread.daemon = True  # Set the thread as a daemon
    thread.start()


# GUI Functions
def create_decision_form(is_update=False, decision_data=None):
    form = tk.Toplevel(root)
    form.title("Decision Form" if not is_update else "Edit Decision")
    form.geometry("600x600")  # Increased window size for better layout

    # Grid layout configuration for alignment
    row = 0
    tk.Label(form, text="Area Affected:").grid(row=row, column=0, sticky='w')
    area_entry = tk.Entry(form, width=50)
    area_entry.grid(row=row, column=1, sticky='w')
    if decision_data:
        area_entry.insert(0, decision_data[2])
    row += 1

    tk.Label(form, text="Decision Maker:").grid(row=row, column=0, sticky='w')
    decision_maker_entry = tk.Entry(form, width=50)
    decision_maker_entry.grid(row=row, column=1, sticky='w')
    if decision_data:
        decision_maker_entry.insert(0, decision_data[3])
    row += 1

    tk.Label(form, text="Decision:").grid(row=row, column=0, sticky='nw')
    decision_entry = tk.Text(form, height=4, width=65)
    decision_entry.grid(row=row, column=1,  sticky='w')
    if decision_data:
        decision_entry.insert(tk.END, decision_data[4])
    row += 1
    

    tk.Label(form, text="Reasoning:").grid(row=row, column=0, sticky='nw')
    reasoning_entry = tk.Text(form, height=4, width=65)
    reasoning_entry.grid(row=row, column=1, sticky='w')
    if decision_data:
        reasoning_entry.insert(tk.END, decision_data[5])
    row += 2

    tk.Label(form, text="Status:").grid(row=row, column=0, sticky='w')
    status_var = tk.StringVar(form)
    status_choices = ["Approved", "Not Approved", "Waiting"]
    status_var.set(decision_data[6] if decision_data else status_choices[0])
    status_menu = tk.OptionMenu(form, status_var, *status_choices)
    status_menu.grid(row=row, column=1, sticky='w')
    row += 1

 
 # Due Date Selection with Calendar
    tk.Label(form, text="Due Date:").grid(row=row, column=0, sticky='w')
    due_date_entry = tk.Entry(form, state='readonly')  # Set to readonly
    due_date_entry.grid(row=row, column=1, sticky='w')
    row += 1
    due_date_button = tkm.Button(form, text="Select Date", command=lambda: select_date(due_date_entry))
    due_date_button.grid(row=row, column=1, sticky='w')

    row += 1

    if decision_data:
        due_date_entry.configure(state='normal')
        due_date_entry.insert(0, decision_data[7])
        due_date_entry.configure(state='readonly')

    row += 1

    submit_button_text = "Update Decision" if is_update else "Log Decision"
    submit_button = tkm.Button(form, text=submit_button_text, command=lambda: submit_decision(form, area_entry.get(), decision_maker_entry.get(), decision_entry.get("1.0", tk.END), reasoning_entry.get("1.0", tk.END), status_var.get(), due_date_entry.get(), is_update, decision_data[0] if decision_data else None))
    submit_button.grid(row=row, column=0, columnspan=3,  sticky='w')

def select_date(entry):
    def on_cal_select():
        # Retrieve the selected date and format it to European format (day-month-year)
        selected_date = cal.selection_get()
        formatted_date = selected_date.strftime("%Y-%m-%d")

        entry.configure(state='normal')  # Enable writing to the entry
        entry.delete(0, tk.END)  # Clear existing content
        entry.insert(0, formatted_date)  # Insert the formatted date
        entry.configure(state='readonly')  # Set back to readonly
        top.destroy()  # Close the calendar window

    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='day')
    cal.pack(padx=10, pady=10)
    tkm.Button(top, text="Select", command=on_cal_select).pack()


# Search function
def search_entries():
    print("Search function called")  # Debugging print statement
    search_term = search_var.get().lower()

    for row in decision_tree.get_children():
        values_str = " ".join(map(str, decision_tree.item(row)['values'])).lower()
        # Check if the search term is in the concatenated string of values
        if search_term in values_str:
            decision_tree.item(row, tags=('visible',))
        else:
            decision_tree.item(row, tags=('hidden',))

    # Configure tags to show or hide rows
    decision_tree.tag_configure('visible', foreground='black')  # Change to default text color
    decision_tree.tag_configure('hidden', foreground='white')  # Change to background color

    print(f"Searched for: {search_term}")  # Print the search term for debugging


def submit_decision(form, area, decision_maker, decision, reasoning, status, due_date, is_update, decision_id):
    print("Submit button clicked")
    if is_update:
        update_decision(decision_id, area, decision_maker, decision, reasoning, status, due_date)
    else:
        log_decision(area, decision_maker, decision, reasoning, status, due_date)
    form.destroy()
    refresh_decision_view()

def refresh_decision_view(status_filter=None, start_date=None, end_date=None):
    decision_tree.delete(*decision_tree.get_children())  # Clear existing rows
    for decision in retrieve_decisions(status_filter, start_date, end_date):
        decision_tree.insert('', 'end', values=decision)

def on_decision_select(event):
    selected_item = decision_tree.focus()
    decision_data = decision_tree.item(selected_item)['values']
    if decision_data:
        create_decision_form(True, decision_data)

def delete_selected_decision():
    selected_item = decision_tree.focus()
    decision_data = decision_tree.item(selected_item)['values']
    if decision_data and messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this decision?"):
        delete_decision(decision_data[0])
        refresh_decision_view()

def apply_filters():
    start_date = start_date_entry.get() if start_date_entry.get() else None
    end_date = end_date_entry.get() if end_date_entry.get() else None
    global status_var  # Ensure that status_var is accessible

    status_filter = status_var.get() if status_var.get() != "All" else None
    print(f"Status filter applied: {status_filter}")  # Debugging print

    print(f"Applying filters with start_date: {start_date}, end_date: {end_date}")
    refresh_decision_view(status_filter, start_date, end_date)

    try:
            if start_date:
                start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            if end_date:
                end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            if start_date and end_date and start_date_obj > end_date_obj:
                messagebox.showerror("Date Error", "Start date cannot be after end date.")
                return
    except ValueError as e:
            messagebox.showerror("Date Format Error", str(e))
            return

    refresh_decision_view(status_filter, start_date, end_date)

def clear_filters():
    print("Clearing filters...")  # Debugging print

    # Reset status filter
    status_var.set("All")

    # Clear the date entries
    print(f"Before clear: Start Date - {start_date_entry.get()}, End Date - {end_date_entry.get()}")
    # Temporarily enable, clear, and disable the date entries
    start_date_entry.config(state=tk.NORMAL)
    start_date_entry.delete(0, tk.END)
    start_date_entry.config(state='readonly')

    end_date_entry.config(state=tk.NORMAL)
    end_date_entry.delete(0, tk.END)
    end_date_entry.config(state='readonly')

    print(f"After clear: Start Date - {start_date_entry.get()}, End Date - {end_date_entry.get()}")

    # Clear the search entry
    search_var.set("")
    search_entry.delete(0, tk.END)

    # Reset the treeview to show all entries
    for row in decision_tree.get_children():
        decision_tree.item(row, tags=('visible',))
    decision_tree.tag_configure('visible', foreground='black')  # Or your default text color

    # Refresh the treeview with all entries
    refresh_decision_view()

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

def on_decision_select(event):
    selected_item = decision_tree.focus()
    decision_data = decision_tree.item(selected_item)['values']
    if decision_data:
        create_decision_form(True, decision_data)

# Tkinter window setup with increased width and scrollbar
root = tk.Tk()
root.title("Decision Logger")
root.geometry("1450x800")

# Filter frame setup with calendar selection for start_date_entry and end_date_entry
filter_frame = tk.Frame(root)
filter_frame.pack()

tk.Label(filter_frame, text="Status Filter:").pack(side=tk.LEFT)
status_choices = ["All", "Approved", "Not Approved", "Waiting"]
status_var = tk.StringVar(root)
status_var.set(status_choices[0])
status_menu = tk.OptionMenu(filter_frame, status_var, *status_choices)
status_menu

status_menu.pack(side=tk.LEFT)

# Start Date Filter
tk.Label(filter_frame, text="Start Date:").pack(side=tk.LEFT)
start_date_entry = tk.Entry(filter_frame, state='readonly')
start_date_entry.pack(side=tk.LEFT)
start_date_button = tkm.Button(filter_frame, text="Select", command=lambda: select_date(start_date_entry))
start_date_button.pack(side=tk.LEFT)

# End Date Filter
tk.Label(filter_frame, text="End Date:").pack(side=tk.LEFT)
end_date_entry = tk.Entry(filter_frame, state='readonly')
end_date_entry.pack(side=tk.LEFT)
end_date_button = tkm.Button(filter_frame, text="Select", command=lambda: select_date(end_date_entry))
end_date_button.pack(side=tk.LEFT)

apply_button = tkm.Button(filter_frame, text="Apply Filters", command=apply_filters)
apply_button.pack(side=tk.LEFT)
clear_button = tkm.Button(filter_frame, text="Clear Filters", command=clear_filters)
clear_button.pack(side=tk.LEFT)

# Decision tree view with scrollbars
tree_frame = ttk.Frame(root)
tree_frame.pack(fill="both", expand=True)

tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

# Modify columns for Treeview
columns = ("ID", "Timestamp", "Area", "Decision Maker", "Decision", "Reasoning", "Status", "Due Date")
decision_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

# Configure the column widths
for col in columns:
    decision_tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(decision_tree, _col, False))
    decision_tree.column(col, anchor=tk.CENTER, width=100)

tree_scroll_y.config(command=decision_tree.yview)
tree_scroll_x.config(command=decision_tree.xview)
decision_tree.pack(fill="both", expand=True)

# Buttons
log_button = tkm.Button(root, text="Log New Decision", command=lambda: create_decision_form())
log_button.pack(side=tk.LEFT)
delete_button = tkm.Button(root, text="Delete Selected Decision", command=delete_selected_decision)
delete_button.pack(side=tk.RIGHT)
refresh_button = tkm.Button(root, text="Refresh", command=lambda: refresh_decision_view())
refresh_button.pack(side=tk.RIGHT)

# Bind double-click event to Treeview for updating entries
decision_tree.bind("<Double-1>", on_decision_select)

# Add search entry and button in filter_frame
tk.Label(filter_frame, text="Search:").pack(side=tk.LEFT)
search_var = tk.StringVar(root)
search_entry = tk.Entry(filter_frame, textvariable=search_var)
search_entry.pack(side=tk.LEFT)
search_button = tkm.Button(filter_frame, text="Search", command=search_entries)
search_button.pack(side=tk.LEFT)

# Bind the Enter key with the search function
search_entry.bind('<Return>', lambda event: search_entries())

# First refresh of the treeview
refresh_decision_view()


def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


# Function to start the main loop and profile it
def start_main_loop():
    root.mainloop()

if __name__ == "__main__":

    setup_database()  # Ensure database is setup
    start_main_loop()  # Start the main loop

    # Run the main loop under the profiler
    cProfile.run('start_main_loop()', 'profile_stats')

    # Optionally, you can add code here to automatically analyze and print the stats after the GUI is closed
    import pstats
    p = pstats.Stats('profile_stats')
    p.sort_stats('cumulative').print_stats(10)  # Adjust the number as needed