# view.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import Calendar
from PIL import Image, ImageTk

class DecisionApp(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Decision Logger")
        self.geometry("1200x600")
        self.create_widgets()

    def create_widgets(self):
        self.controller.load_status_images()

        # Filter frame setup with calendar selection for start_date_entry and end_date_entry
        filter_frame = tk.Frame(self)
        filter_frame.pack()

        tk.Label(filter_frame, text="Status Filter:").pack(side=tk.LEFT)
        status_choices = ["All", "Approved", "Not Approved", "Waiting"]
        self.status_var = tk.StringVar(self)
        self.status_var.set(status_choices[0])
        status_menu = tk.OptionMenu(filter_frame, self.status_var, *status_choices)
        status_menu.pack(side=tk.LEFT)

        # Start Date Filter
        tk.Label(filter_frame, text="Start Date:").pack(side=tk.LEFT)
        self.start_date_entry = tk.Entry(filter_frame, state='readonly')
        self.start_date_entry.pack(side=tk.LEFT)
        start_date_button = tk.Button(filter_frame, text="Select", command=lambda: self.controller.select_date(self.start_date_entry))
        start_date_button.pack(side=tk.LEFT)

        # End Date Filter
        tk.Label(filter_frame, text="End Date:").pack(side=tk.LEFT)
        self.end_date_entry = tk.Entry(filter_frame, state='readonly')
        self.end_date_entry.pack(side=tk.LEFT)
        end_date_button = tk.Button(filter_frame, text="Select", command=lambda: self.controller.select_date(self.end_date_entry))
        end_date_button.pack(side=tk.LEFT)

        apply_button = tk.Button(filter_frame, text="Apply Filters", command=self.controller.apply_filters)
        apply_button.pack(side=tk.LEFT)
        clear_button = tk.Button(filter_frame, text="Clear Filters", command=self.controller.clear_filters)
        clear_button.pack(side=tk.LEFT)

        # Decision tree view with scrollbars
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill="both", expand=True)
        self.tree_scroll_y = ttk.Scrollbar(self.tree_frame, orient="vertical")
        self.tree_scroll_x = ttk.Scrollbar(self.tree_frame, orient="horizontal")
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        columns = ("ID", "Timestamp", "Area", "Decision Maker", "Decision", "Reasoning", "Status", "Due Date")
        self.decision_tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)

        for col in columns:
            self.decision_tree.heading(col, text=col, command=lambda _col=col: self.controller.treeview_sort_column(self.decision_tree, _col, False))
            self.decision_tree.column(col, anchor=tk.CENTER)

        self.tree_scroll_y.config(command=self.decision_tree.yview)
        self.tree_scroll_x.config(command=self.decision_tree.xview)
        self.decision_tree.pack(fill="both", expand=True)
        self.decision_tree.bind("<Double-1>", self.controller.on_decision_select)

        # Buttons
        log_button = tk.Button(self, text="Log New Decision", command=lambda: self.controller.create_decision_form())
        log_button.pack(side=tk.LEFT)
        delete_button = tk.Button(self, text="Delete Selected Decision", command=self.controller.delete_selected_decision)
        delete_button.pack(side=tk.LEFT)
        refresh_button = tk.Button(self, text="Refresh", command=self.controller.refresh_decision_view)
        refresh_button.pack(side=tk.RIGHT)
