import tkinter as tk
from tkinter import ttk, messagebox


class RecordList(ttk.Frame):
    """Table for showing CSV records."""

    columns = (
        "Date",
        "Time",
        "Technician",
        "Lab",
        "Plot"
    )

    def __init__(self, parent, on_select):
        super().__init__(parent, padding=10)

        self.on_select = on_select
        self.inserted_rows = set()
        self.updated_rows = set()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            selectmode="browse"
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.tree.heading("#0", text="Row")
        self.tree.column(
            "#0",
            width=55,
            anchor=tk.CENTER,
            stretch=False
        )

        for column_name in self.columns:
            self.tree.heading(
                column_name,
                text=column_name,
                anchor=tk.CENTER
            )

            self.tree.column(
                column_name,
                width=120,
                anchor=tk.CENTER
            )

        self.tree.column(
            "Technician",
            width=150
        )


        self.tree.tag_configure(
            "inserted",
            background="#CDEAC0",
            foreground="#355834"
        )

        self.tree.tag_configure(
            "updated",
            background="#CDE7F0",
            foreground="#365563"
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.open_selected_record
        )

    def populate(self, records):
        """Refresh records in table."""

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row_number, record in enumerate(records):
            values = (
                record.get("Date", ""),
                record.get("Time", ""),
                record.get("Technician", ""),
                record.get("Lab", ""),
                record.get("Plot", "")
            )

            tags = ()

            if row_number in self.inserted_rows:
                tags = ("inserted",)

            elif row_number in self.updated_rows:
                tags = ("updated",)

            self.tree.insert(
                "",
                tk.END,
                iid=str(row_number),
                text=str(row_number),
                values=values,
                tags=tags
            )

    def open_selected_record(self, event=None):
        """Open clicked row."""

        selected = self.tree.selection()

        if not selected:
            return

        self.on_select(int(selected[0]))

    def mark_inserted(self, row_number):
        self.inserted_rows.add(int(row_number))

    def mark_updated(self, row_number):
        row_number = int(row_number)

        self.inserted_rows.discard(row_number)
        self.updated_rows.add(row_number)

    def clear_row_colors(self):
        self.inserted_rows.clear()
        self.updated_rows.clear()


class RecordEditor(tk.Toplevel):
    """Complete data-entry form for one record."""

    required_fields = {
        "Date": "A value is required",
        "Time": "A value is required",
        "Lab": "A value is required",
        "Plot": "A value is required",
        "Humidity": "A value is required",
        "Temperature": "A value is required",
        "Plants": "A value is required",
        "Fruit": "A value is required",
        "Min Height": "A value is required",
        "Max Height": "A value is required"
    }

    numeric_fields = (
        "Humidity",
        "Light",
        "Temperature",
        "Plants",
        "Blossoms",
        "Fruit",
        "Min Height",
        "Max Height",
        "Median Height"
    )

    def __init__(self, parent, record, row_number, on_save):
        super().__init__(parent)

        self.row_number = row_number
        self.on_save_callback = on_save

        self.title("SABA Data Entry Application")
        self.geometry("920x780")
        self.minsize(780, 650)

        self.configure(background="#FFF7FB")

        self.variables = {}
        self.error_labels = {}

        self.create_variables(record)
        self.create_widgets()

        self.transient(parent)
        self.grab_set()

    def create_variables(self, record):
        """Load record values into Tkinter variables."""

        all_fields = [
            "Date",
            "Time",
            "Technician",
            "Lab",
            "Plot",
            "Seed sample",
            "Humidity",
            "Light",
            "Temperature",
            "Equipment Fault",
            "Plants",
            "Blossoms",
            "Fruit",
            "Min Height",
            "Max Height",
            "Median Height"
        ]

        for field in all_fields:
            value = record.get(field, "")

            if value is None:
                value = ""

            self.variables[field] = tk.StringVar(
                value=str(value)
            )

        self.notes_value = str(record.get("Notes", ""))

    def create_widgets(self):
        """Create all sections of the form."""

        self.main_frame = ttk.Frame(
            self,
            padding=14
        )

        self.main_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)

        title = ttk.Label(
            self.main_frame,
            text="Saba Data Entry Application",
            font=("Arial", 16, "bold")
        )

        title.grid(
            row=0,
            column=0,
            pady=(0, 14)
        )

        self.create_record_info()
        self.create_environment_data()
        self.create_plant_data()
        self.create_notes()
        self.create_buttons()

    def add_label(self, parent, text, row, column):
        """Create a label above a field."""

        label = ttk.Label(parent, text=text)

        label.grid(
            row=row,
            column=column,
            padx=6,
            pady=(7, 2),
            sticky="w"
        )

    def add_error_label(self, parent, field, row, column):
        """Create an initially-empty validation message."""

        error_label = tk.Label(
            parent,
            text="",
            background="#FFF7FB",
            foreground="#E74C3C",
            font=("Arial", 9)
        )

        error_label.grid(
            row=row,
            column=column,
            padx=6,
            pady=(1, 4),
            sticky="w"
        )

        self.error_labels[field] = error_label

    def add_entry(self, parent, field, row, column):
        """Create a regular Entry."""

        entry = ttk.Entry(
            parent,
            textvariable=self.variables[field]
        )

        entry.grid(
            row=row,
            column=column,
            padx=6,
            sticky="ew"
        )

        return entry

    def add_spinbox(
        self,
        parent,
        field,
        row,
        column,
        minimum,
        maximum,
        increment
    ):
        """Create numeric Spinbox."""

        spinbox = ttk.Spinbox(
            parent,
            from_=minimum,
            to=maximum,
            increment=increment,
            textvariable=self.variables[field]
        )

        spinbox.grid(
            row=row,
            column=column,
            padx=6,
            sticky="ew"
        )

        return spinbox

    def create_record_info(self):
        """Create Record Information section."""

        frame = ttk.LabelFrame(
            self.main_frame,
            text="Record Info",
            padding=10
        )

        frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        for column in range(3):
            frame.columnconfigure(column, weight=1)

        # Row 1
        self.add_label(frame, "Date", 0, 0)
        self.add_label(frame, "Time", 0, 1)
        self.add_label(frame, "Technician", 0, 2)

        self.add_entry(frame, "Date", 1, 0)

        # Time = Combobox
        self.time_box = ttk.Combobox(
            frame,
            textvariable=self.variables["Time"],
            values=[
                "08:00",
                "10:00",
                "12:00",
                "14:00",
                "16:00",
                "18:00",
                "20:00"
            ],
            state="readonly"
        )

        self.time_box.grid(
            row=1,
            column=1,
            padx=6,
            sticky="ew"
        )

        self.add_entry(frame, "Technician", 1, 2)

        self.add_error_label(frame, "Date", 2, 0)
        self.add_error_label(frame, "Time", 2, 1)

        # Row 2
        self.add_label(frame, "Lab", 3, 0)
        self.add_label(frame, "Plot", 3, 1)
        self.add_label(frame, "Seed Sample", 3, 2)

        # Lab = Combobox
        self.lab_box = ttk.Combobox(
            frame,
            textvariable=self.variables["Lab"],
            values=["A", "B", "C", "D", "E"],
            state="readonly"
        )

        self.lab_box.grid(
            row=4,
            column=0,
            padx=6,
            sticky="ew"
        )

        # Plot = Combobox
        self.plot_box = ttk.Combobox(
            frame,
            textvariable=self.variables["Plot"],
            values=[
                "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "10"
            ],
            state="readonly"
        )

        self.plot_box.grid(
            row=4,
            column=1,
            padx=6,
            sticky="ew"
        )

        self.add_entry(frame, "Seed sample", 4, 2)

        self.add_error_label(frame, "Lab", 5, 0)
        self.add_error_label(frame, "Plot", 5, 1)

    def create_environment_data(self):
        """Create Environment Data section."""

        frame = ttk.LabelFrame(
            self.main_frame,
            text="Environment Data",
            padding=10
        )

        frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        for column in range(3):
            frame.columnconfigure(column, weight=1)

        self.add_label(frame, "Humidity", 0, 0)
        self.add_label(frame, "Light", 0, 1)
        self.add_label(frame, "Temperature", 0, 2)

        # Numeric fields = Spinbox
        self.add_spinbox(
            frame,
            "Humidity",
            1,
            0,
            minimum=0,
            maximum=100,
            increment=0.1
        )

        self.add_spinbox(
            frame,
            "Light",
            1,
            1,
            minimum=0,
            maximum=100000,
            increment=0.1
        )

        self.add_spinbox(
            frame,
            "Temperature",
            1,
            2,
            minimum=0,
            maximum=100,
            increment=0.1
        )

        self.add_error_label(frame, "Humidity", 2, 0)
        self.add_error_label(frame, "Light", 2, 1)
        self.add_error_label(frame, "Temperature", 2, 2)

        self.fault_check = ttk.Checkbutton(
            frame,
            text="Equipment Fault",
            variable=self.variables["Equipment Fault"],
            onvalue="Yes",
            offvalue="No"
        )

        self.fault_check.grid(
            row=3,
            column=0,
            padx=6,
            pady=(7, 2),
            sticky="w"
        )

    def create_plant_data(self):
        """Create Plant Data section."""

        frame = ttk.LabelFrame(
            self.main_frame,
            text="Plant Data",
            padding=10
        )

        frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        for column in range(3):
            frame.columnconfigure(column, weight=1)

        self.add_label(frame, "Plants", 0, 0)
        self.add_label(frame, "Blossoms", 0, 1)
        self.add_label(frame, "Fruit", 0, 2)

        self.add_spinbox(
            frame,
            "Plants",
            1,
            0,
            minimum=0,
            maximum=100000,
            increment=1
        )

        self.add_spinbox(
            frame,
            "Blossoms",
            1,
            1,
            minimum=0,
            maximum=100000,
            increment=1
        )

        self.add_spinbox(
            frame,
            "Fruit",
            1,
            2,
            minimum=0,
            maximum=100000,
            increment=1
        )

        self.add_error_label(frame, "Plants", 2, 0)
        self.add_error_label(frame, "Blossoms", 2, 1)
        self.add_error_label(frame, "Fruit", 2, 2)

        self.add_label(frame, "Min Height", 3, 0)
        self.add_label(frame, "Max Height", 3, 1)
        self.add_label(frame, "Median Height", 3, 2)

        self.add_spinbox(
            frame,
            "Min Height",
            4,
            0,
            minimum=0,
            maximum=1000,
            increment=0.1
        )

        self.add_spinbox(
            frame,
            "Max Height",
            4,
            1,
            minimum=0,
            maximum=1000,
            increment=0.1
        )

        self.add_spinbox(
            frame,
            "Median Height",
            4,
            2,
            minimum=0,
            maximum=1000,
            increment=0.1
        )

        self.add_error_label(frame, "Min Height", 5, 0)
        self.add_error_label(frame, "Max Height", 5, 1)
        self.add_error_label(frame, "Median Height", 5, 2)

    def create_notes(self):
        """Create Notes section."""

        frame = ttk.LabelFrame(
            self.main_frame,
            text="Notes",
            padding=8
        )

        frame.grid(
            row=4,
            column=0,
            sticky="nsew",
            pady=(0, 12)
        )

        self.main_frame.rowconfigure(4, weight=1)

        self.notes_text = tk.Text(
            frame,
            height=7,
            wrap=tk.WORD,
            background="#FFFFFF",
            foreground="#4E3B4A",
            relief=tk.SOLID,
            borderwidth=1
        )

        self.notes_text.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.notes_text.insert(
            "1.0",
            self.notes_value
        )

    def create_buttons(self):
        """Create Save and Cancel buttons."""

        button_frame = ttk.Frame(self.main_frame)

        button_frame.grid(
            row=5,
            column=0,
            sticky="e"
        )

        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy
        )

        cancel_button.pack(
            side=tk.RIGHT
        )

        save_button = ttk.Button(
            button_frame,
            text="Save",
            command=self.save_record
        )

        save_button.pack(
            side=tk.RIGHT,
            padx=(0, 8)
        )

    def get_record(self):
        """Convert form values into a dictionary."""

        record = {}

        for field, variable in self.variables.items():
            record[field] = variable.get().strip()

        record["Notes"] = self.notes_text.get(
            "1.0",
            tk.END
        ).strip()

        return record

    def clear_errors(self):
        """Clear all red validation messages."""

        for error_label in self.error_labels.values():
            error_label.config(text="")

    def show_error(self, field, message):
        """Show red message under one field."""

        error_label = self.error_labels.get(field)

        if error_label:
            error_label.config(text=message)

    def validate_record(self, record):
        """Validate required and numeric fields."""

        self.clear_errors()
        is_valid = True

        # Required fields
        for field, error_message in self.required_fields.items():
            if not record[field]:
                self.show_error(field, error_message)
                is_valid = False

        # Check numeric values
        for field in self.numeric_fields:
            value = record[field].replace(",", ".")

            if not value:
                continue

            try:
                float(value)
            except ValueError:
                self.show_error(
                    field,
                    "Enter a valid number"
                )
                is_valid = False

        # Min Height must be <= Max Height
        min_height = record["Min Height"].replace(",", ".")
        max_height = record["Max Height"].replace(",", ".")

        if min_height and max_height:
            try:
                if float(min_height) > float(max_height):
                    self.show_error(
                        "Min Height",
                        "Min cannot be greater than Max"
                    )

                    self.show_error(
                        "Max Height",
                        "Max must be greater than Min"
                    )

                    is_valid = False

            except ValueError:
                pass

        return is_valid

    def save_record(self):
        """Validate form, then return data to Application."""

        record = self.get_record()

        if not self.validate_record(record):
            messagebox.showwarning(
                "Validation Error",
                "Please correct the highlighted fields."
            )
            return

        self.on_save_callback(
            record,
            self.row_number
        )

        self.destroy()
