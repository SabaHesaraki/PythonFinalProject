from datetime import date
import tkinter as tk
from tkinter import filedialog, font, messagebox, ttk
import login
import mainmenu
import models

import views


class Application(tk.Tk):
    """Main window of SABA Data Entry Application."""

    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title("SABA Data Entry Application")
        self.geometry("1000x620")
        self.minsize(800, 500)

        self.settings_model = models.SettingsModel()
        self.settings = {}
        self._load_settings()

        self.data_model = None
        self.filename = tk.StringVar()
        self.status = tk.StringVar(value="Select a CSV file to start.")

        self.create_style()
        self._bind_setting_traces()

        self.callbacks = {
            "on_file_select": self.select_file,
            "on_new_record": self.open_new_record,
            "on_quit": self.destroy,
            "on_about": self.show_about,
        }

        self.create_widgets()
        self.login_window = login.LoginWindow(
            parent=self, on_success=self.show_main_window
        )

    def _load_settings(self):
        """Load settings variables before installing any traces."""
        for key, info in models.SettingsModel.fields.items():
            val = self.settings_model.get(key)
            if info["type"] == "int":
                var = tk.IntVar(value=val)
            elif info["type"] == "bool":
                var = tk.BooleanVar(value=val)
            else:
                var = tk.StringVar(value=val)
            self.settings[key] = var

    def _bind_setting_traces(self):
        """Persist settings and apply live font/theme changes."""
        for key, var in self.settings.items():
            var.trace_add(
                "write",
                lambda *_, k=key, v=var: self.settings_model.set(k, v.get()),
            )

        self._set_font()
        self.settings["font size"].trace_add("write", self._set_font)
        self.settings["font family"].trace_add("write", self._set_font)
        self.settings["theme"].trace_add("write", self._set_theme)

    def _set_font(self, *_):
        """Set the application font dynamically across Tk standard named fonts."""
        font_size = self.settings["font size"].get()
        font_family = self.settings["font family"].get()

        font_names = (
            "TkDefaultFont",
            "TkMenuFont",
            "TkTextFont",
            "TkFixedFont",
        )

        for font_name in font_names:
            tk_font = font.nametofont(font_name)
            if font_family:
                tk_font.config(size=font_size, family=font_family)
            else:
                tk_font.config(size=font_size)

    def show_main_window(self):
        self.deiconify()
        self.lift()
        self.show_status("Login successful. Welcome, Saba!", "success")

    def _set_theme(self, *_):
        """Apply the selected ttk theme, falling back to a safe available theme."""
        requested = self.settings["theme"].get()
        try:
            self.style.theme_use(requested)
            return
        except tk.TclError:
            themes = self.style.theme_names()
            fallback = "clam" if "clam" in themes else (themes[0] if themes else None)
            if fallback is None:
                return
            self.style.theme_use(fallback)
            if requested != fallback:
                # Keep the model/JSON valid without recursively applying the theme.
                self.settings["theme"].set(fallback)

    def create_style(self):
        """Create the ttk style and apply the configured theme."""
        self.style = ttk.Style(self)
        self._set_theme()
        style = self.style

        self.configure(background="#FFF7FB")

        style.configure("TFrame", background="#FFF7FB")

        style.configure("TLabel", background="#FFF7FB", foreground="#5C4B57")

        style.configure(
            "Title.TLabel",
            background="#FDEBF2",
            foreground="#805C7A",
            font=("Arial", 18, "bold"),
        )

        style.configure(
            "TLabelframe",
            background="#FFF7FB",
            foreground="#805C7A",
            bordercolor="#E8B4C8",
        )

        style.configure(
            "TLabelframe.Label",
            background="#FFF7FB",
            foreground="#805C7A",
            font=("Arial", 10, "bold"),
        )

        style.configure(
            "TButton",
            background="#D9C2E9",
            foreground="#4E3B4A",
            padding=(10, 6),
        )

        style.map("TButton", background=[("active", "#F5C6D6")])

        style.configure(
            "Treeview",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#4E3B4A",
            rowheight=30,
        )

        style.configure(
            "Treeview.Heading",
            background="#E9D5F5",
            foreground="#5D4663",
            font=("Arial", 10, "bold"),
        )

        style.map(
            "Treeview",
            background=[("selected", "#BFD7EA")],
            foreground=[("selected", "#3E4C59")],
        )
        style.configure(
            "Status.TLabel",
            background="#FDEBF2",
            foreground="#76506F",
            font=("Arial", 10),
            padding=8,
        )

        style.configure(
            "SuccessStatus.TLabel",
            background="#DDF4E4",
            foreground="#287A45",
            font=("Arial", 10, "bold"),
            padding=8,
        )

        style.configure(
            "ErrorStatus.TLabel",
            background="#FCE2E2",
            foreground="#B23A3A",
            font=("Arial", 10, "bold"),
            padding=8,
        )

    def create_widgets(self):
        """Build main page."""
        menu_bar = mainmenu.MainMenu(self, self.settings, self.callbacks)
        self.config(menu=menu_bar)

        main_frame = ttk.Frame(self, padding=14)
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Header
        header = tk.Frame(main_frame, background="#FDEBF2", height=85)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        header.grid_propagate(False)

        title = ttk.Label(
            header, text="SABA Data Entry Application", style="Title.TLabel"
        )
        title.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # CSV selection
        file_frame = ttk.LabelFrame(main_frame, text="CSV File", padding=10)
        file_frame.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        file_frame.columnconfigure(0, weight=1)

        self.filename_entry = ttk.Entry(
            file_frame, textvariable=self.filename, state="readonly"
        )
        self.filename_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        select_button = ttk.Button(
            file_frame, text="Select CSV File", command=self.select_file
        )
        select_button.grid(row=0, column=1)

        # Records table
        self.record_list = views.RecordList(
            main_frame, on_select=self.open_existing_record
        )
        self.record_list.grid(row=2, column=0, sticky="nsew")

        # Status bar
        self.status_label = ttk.Label(
            main_frame,
            textvariable=self.status,
            style="Status.TLabel",
            anchor=tk.W,
            relief=tk.SUNKEN,
        )
        self.status_label.grid(row=3, column=0, sticky="ew", pady=(14, 0))

    def show_status(self, message, status_type="normal"):
        """Show a colored message at the bottom of the main window."""
        style_name = "Status.TLabel"
        if status_type == "success":
            style_name = "SuccessStatus.TLabel"
        elif status_type == "error":
            style_name = "ErrorStatus.TLabel"

        self.status.set(message)
        self.status_label.configure(style=style_name)

    def get_empty_record(self):
        """Create a new empty record with today's Gregorian date."""
        record = {field: "" for field in models.CSVModel.fieldnames}
        record["Date"] = date.today().isoformat()
        record["Humidity"] = "0.0"
        record["Light"] = "0.0"
        record["Temperature"] = "0.0"
        record["Plants"] = "0"
        record["Blossoms"] = "0"
        record["Fruit"] = "0"
        record["Min Height"] = "0.0"
        record["Max Height"] = "0.0"
        record["Median Height"] = "0.0"
        record["Equipment Fault"] = "No"
        return record

    def select_file(self):
        """Choose a CSV file."""
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

        if not filename:
            return

        try:
            self.data_model = models.CSVModel(filename)
            self.filename.set(filename)
            self.record_list.clear_row_colors()
            records = self.refresh_table()
            print(f"Loaded CSV: {filename} ({len(records)} records)")
            if records:
                self.show_status("CSV file loaded. Click a row to edit it.", "success")
            else:
                self.show_status("CSV file loaded, but no records were found.")
        except Exception as error:
            messagebox.showerror(
                "File Error", f"Could not open the file.\n\n{error}"
            )

    def open_new_record(self):
        """Open the complete form for creating a new record."""
        if self.data_model is None:
            messagebox.showwarning("No File", "Please select a CSV file first.")
            self.show_status(
                "Select a CSV file before creating a record.", "error"
            )
            return

        empty_record = self.get_empty_record()
        views.RecordEditor(
            parent=self,
            record=empty_record,
            row_number=None,
            on_save=self.save_record,
        )

    def open_existing_record(self, row_number):
        """Open the selected record in the complete editor."""
        if self.data_model is None:
            return

        try:
            record = self.data_model.get_record(row_number)
            views.RecordEditor(
                parent=self,
                record=record,
                row_number=row_number,
                on_save=self.save_record,
            )
        except Exception as error:
            messagebox.showerror(
                "Record Error", f"Could not open the record.\n\n{error}"
            )

    def save_record(self, record, row_number):
        """Save a new record or update an existing record."""
        try:
            if row_number is None:
                self.data_model.add_record(record)
                new_row_number = len(self.data_model.get_all_records()) - 1
                self.record_list.mark_inserted(new_row_number)
                self.show_status(
                    "✓ New record saved successfully.", "success"
                )
            else:
                self.data_model.update_record(row_number, record)
                self.record_list.mark_updated(row_number)
                self.show_status(
                    f"✓ Record {row_number} updated successfully.", "success"
                )
            self.refresh_table()
        except Exception as error:
            messagebox.showerror(
                "Save Error", f"Could not save the record.\n\n{error}"
            )
            self.show_status("Could not save the record.", "error")

    def refresh_table(self):
        """Refresh the table with all records currently loaded."""
        records = []
        if self.data_model is not None:
            records = self.data_model.get_all_records()
        self.record_list.populate(records)
        return records

    def show_about(self):
        """Show About message."""
        messagebox.showinfo(
            "About",
            "SABA Data Entry Application\n\n"
            "Click a row to open its complete form.",
        )


if __name__ == "__main__":
    app = Application()
    app.mainloop()
