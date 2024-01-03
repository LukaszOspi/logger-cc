# controller.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import Calendar
import sqlite3
import datetime
from PIL import Image, ImageTk

class DecisionController:
  def __init__(self):
        self.root = tk.Tk()
        self.setup_database()
        self.load_status_images()
        self.create_widgets()


def setup_database(self):
        conn = sqlite3.connect('decision_log.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                area TEXT,
                decision_maker TEXT,
                decision TEXT,
                reasoning TEXT,
                status TEXT,
                due_date TEXT
            )
        ''')
        conn.commit()
        conn.close()

def load_status_images(self):
        global global_approved_img, global_waiting_img, global_not_approved_img
        try:
            green_img = Image.open("green_circle.png")
            yellow_img = Image.open("yellow_circle.png")
            red_img = Image.open("red_circle.png")

            global_approved_img = ImageTk.PhotoImage(green_img)
            global_waiting_img = ImageTk.PhotoImage(yellow_img)
            global_not_approved_img = ImageTk.PhotoImage(red_img)
        except Exception as e:
            print(f"Error loading images: {e}")

# Inside DecisionController class
def create_widgets(self):
    # Filter frame setup with calendar selection for start_date_entry and end_date_entry
    filter_frame = tk.Frame(self.root)
    filter_frame.pack()

    tk.Label(filter_frame, text="Status Filter:").pack(side=tk.LEFT)
    status_choices = ["All", "Approved", "Not Approved", "Waiting"]
    self.status_var = tk.StringVar(self.root)
    self.status_var.set(status_choices[0])
    status_menu = tk.OptionMenu(filter_frame, self.status_var, *status_choices)
    status_menu.pack(side=tk.LEFT)

    # Start Date Filter
    tk.Label(filter_frame, text="Start Date:").pack(side=tk.LEFT)
    self.start_date_entry = tk.Entry(filter_frame, state='readonly')
    self.start_date_entry.pack(side=tk.LEFT)
    start_date_button = tk.Button(filter_frame, text="Select", command=lambda: self.select_date(self.start_date_entry))
    start_date_button.pack(side=tk.LEFT)

    # End Date Filter
    tk.Label(filter_frame, text="End Date:").pack(side=tk.LEFT)
    self.end_date_entry = tk.Entry(filter_frame, state='readonly')
    self.end_date_entry.pack(side=tk.LEFT)
    end_date_button = tk.Button(filter_frame, text="Select", command=lambda: self.select_date(self.end_date_entry))
    end_date_button.pack(side=tk.LEFT)

    apply_button = tk.Button(filter_frame, text="Apply Filters", command=self.apply_filters)
    apply_button.pack(side=tk.LEFT)
    clear_button = tk.Button(filter_frame, text="Clear Filters", command=self.clear_filters)
    clear_button.pack(side=tk.LEFT)

    # Decision tree view with scrollbars
    tree_frame = ttk.Frame(self.root)
    tree_frame.pack(fill="both", expand=True)
    tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
    tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
    tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    # Modify columns for Treeview
    columns = ("ID", "Timestamp", "Area", "Decision Maker", "Decision", "Reasoning", "Status", "Due Date")
    self.decision_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

    # Configure the column widths
    self.decision_tree.column("#0", width=20, anchor='center')
    for col in columns:
        self.decision_tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.decision_tree, _col, False))
        self.decision_tree.column(col, anchor=tk.CENTER, width=100)

    tree_scroll_y.config(command=self.decision_tree.yview)
    tree_scroll_x.config(command=self.decision_tree.xview)
    self.decision_tree.pack(fill="both", expand=True)
    self.decision_tree.bind("<Double-1>", self.on_decision_select)

    # Buttons
    log_button = tk.Button(self.root, text="Log New Decision", command=lambda: self.create_decision_form())
    log_button.pack(side=tk.LEFT)
    delete_button = tk.Button(self.root, text="Delete Selected Decision", command=self.delete_selected_decision)
    delete_button.pack(side=tk.LEFT)
    refresh_button = tk.Button(self.root, text="Refresh", command=lambda: self.refresh_decision_view())
    refresh_button.pack(side=tk.RIGHT)

    self.refresh_decision_view()

def create_decision_form(self, is_update=False, decision_data=None):
        form = tk.Toplevel(self.root)
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
        decision_entry = scrolledtext.ScrolledText(form, height=3, width=38)
        decision_entry.grid(row=row, column=1, sticky='w', pady=(0, 10))
        if decision_data:
            decision_entry.insert(tk.END, decision_data[4])
        row += 1

        tk.Label(form, text="Reasoning:").grid(row=row, column=0, sticky='nw')
        reasoning_entry = scrolledtext.ScrolledText(form, height=3, width=38)
        reasoning_entry.grid(row=row, column=1, sticky='w')
        if decision_data:
            reasoning_entry.insert(tk.END, decision_data[5])
        row += 1

        tk.Label(form, text="Status:").grid(row=row, column=0)
        status_var = tk.StringVar(form)
        status_choices = ["Approved", "Not Approved", "Waiting"]
        status_var.set(decision_data[6] if decision_data else status_choices[0])
        status_menu = tk.OptionMenu(form, status_var, *status_choices)
        status_menu.grid(row=row, column=1)
        row += 1

        # Due Date Selection with Calendar
        tk.Label(form, text="Due Date:").grid(row=row, column=0)
        due_date_entry = tk.Entry(form, state='readonly')  # Set to readonly
        due_date_entry.grid(row=row, column=2)
        due_date_button = tk.Button(form, text="Select Date", command=lambda: select_date(due_date_entry))
        due_date_button.grid(row=row, column=1)
        if decision_data:
            due_date_entry.configure(state='normal')
            due_date_entry.insert(0, decision_data[7])
            due_date_entry.configure(state='readonly')
        row += 1

        submit_button_text = "Update Decision" if is_update else "Log Decision"
        submit_button = tk.Button(form, text=submit_button_text, command=lambda: submit_decision(form, area_entry.get(), decision_maker_entry.get(), decision_entry.get("1.0", tk.END), reasoning_entry.get("1.0", tk.END), status_var.get(), due_date_entry.get(), is_update, decision_data[0] if decision_data else None))
        submit_button.grid(row=row, column=0, columnspan=3)

def log_decision(area, decision_maker, decision, reasoning, status, due_date):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('decision_log.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO decisions (timestamp, area, decision_maker, decision, reasoning, status, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, area, decision_maker, decision, reasoning, status, due_date))
    conn.commit()
    conn.close()

def update_decision(id, area, decision_maker, decision, reasoning, status, due_date):
    conn = sqlite3.connect('decision_log.db')
    c = conn.cursor()
    c.execute('''
        UPDATE decisions
        SET area = ?, decision_maker = ?, decision = ?, reasoning = ?, status = ?, due_date = ?
        WHERE id = ?
    ''', (area, decision_maker, decision, reasoning, status, due_date, id))
    conn.commit()
    conn.close()

# Delete decision
def delete_decision(id):
    conn = sqlite3.connect('decision_log.db')
    c = conn.cursor()
    c.execute('DELETE FROM decisions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
# Retrieve decisions with optional filters
def retrieve_decisions(status_filter=None, start_date=None, end_date=None):
    conn = sqlite3.connect('decision_log.db')
    c = conn.cursor()
    query = 'SELECT * FROM decisions'
    filters = []
    if status_filter or start_date or end_date:
        query += ' WHERE'
        if status_filter:
            query += ' status = ?'
            filters.append(status_filter)
        if start_date:
            if filters:
                query += ' AND'
            query += ' timestamp >= ?'
            filters.append(start_date)
        if end_date:
            if filters:
                query += ' AND'
            query += ' timestamp <= ?'
            filters.append(end_date)
    c.execute(query, tuple(filters))
    decisions = c.fetchall()
    conn.close()
    return decisions
def refresh_decision_view(status_filter=None, start_date=None, end_date=None):
    # Use the global image variables in a local dictionary for easy access
    status_images = {
        "Approved": global_approved_img,
        "Waiting": global_waiting_img,
        "Not Approved": global_not_approved_img
    }

def on_decision_select(self, event):
    selected_item = self.decision_tree.focus()
    decision_data = self.decision_tree.item(selected_item)['values']
    if decision_data:
        self.create_decision_form(True, decision_data)

def delete_selected_decision(self):
    selected_item = self.decision_tree.focus()
    decision_data = self.decision_tree.item(selected_item)['values']
    if decision_data and messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this decision?"):
        self.delete_decision(decision_data[0])
        self.refresh_decision_view()

def apply_filters(self):
    status_filter = self.status_var.get() if self.status_var.get() != "All" else None
    start_date = self.start_date_entry.get() if self.start_date_entry.get() else None
    end_date = self.end_date_entry.get() if self.end_date_entry.get() else None
    self.refresh_decision_view(status_filter, start_date, end_date)

def clear_filters(self):
    self.status_var.set("All")
    self.start_date_entry.delete(0, tk.END)
    self.end_date_entry.delete(0, tk.END)
    self.refresh_decision_view()

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

def select_date(self, entry):
    def on_cal_select():
        # Retrieve the selected date and format it to European format (day-month-year)
        selected_date = cal.selection_get()
        formatted_date = selected_date.strftime("%d-%m-%Y")

        entry.configure(state='normal')  # Enable writing to the entry
        entry.delete(0, tk.END)  # Clear existing content
        entry.insert(0, formatted_date)  # Insert the formatted date
        entry.configure(state='readonly')  # Set back to readonly
        top.destroy()  # Close the calendar window

    top = tk.Toplevel(self.root)
    cal = Calendar(top, selectmode='day')
    cal.pack(padx=10, pady=10)
    tk.Button(top, text="Select", command=on_cal_select).pack()


def submit_decision(form, area, decision_maker, decision, reasoning, status, due_date, is_update, decision_id):
    if is_update:
        update_decision(decision_id, area, decision_maker, decision, reasoning, status, due_date)
    else:
        log_decision(area, decision_maker, decision, reasoning, status, due_date)
    form.destroy()
    refresh_decision_view()

def refresh_decision_view(self, status_filter=None, start_date=None, end_date=None):
    # Use the class attributes for image variables
    status_images = {
        "Approved": self.global_approved_img,
        "Waiting": self.global_waiting_img,
        "Not Approved": self.global_not_approved_img
    }

    # Clearing existing rows in the tree view
    for row in self.decision_tree.get_children():
        self.decision_tree.delete(row)

    # Retrieving decisions and inserting them into the tree view
    for decision in self.retrieve_decisions(status_filter, start_date, end_date):
        status_icon = status_images.get(decision[6], None)
        self.decision_tree.insert('', 'end', image=status_icon, values=(decision[0], decision[1], decision[2], decision[3], decision[4], decision[5], decision[6], decision[7]))

def run(self):
        self.root.title("Decision Logger")
        self.root.geometry("1200x600")
        self.refresh_decision_view()
        self.root.mainloop()

if __name__ == "__main__":
    controller = DecisionController()
    controller.run()
