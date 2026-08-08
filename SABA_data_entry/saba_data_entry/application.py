import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

from . import models as m
from . import views as v


class Application(tk.Tk):
    """Application root window."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Saba Data Entry Application")
        self.resizable(False, False)

        self.filename = tk.StringVar(
            value=self._get_default_filename()
        )

        self.settings_model = m.SettingsModel()
        self.load_settings()

        self.callbacks = {
            "file->select": self.on_file_select,
            "file->quit": self.quit
        }

        menu = v.MainMenu(
            self,
            self.settings,
            self.callbacks
        )
        self.config(menu=menu)

        self.recordform = v.DataRecordForm(
            self,
            m.CSVModel.fields,
            self.settings
        )
        self.recordform.grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        self.savebutton = ttk.Button(
            self,
            text="Save",
            command=self.on_save
        )
        self.savebutton.grid(
            row=2,
            column=0,
            padx=10,
            pady=(0, 5),
            sticky="e"
        )

        self.status = tk.StringVar()

        self.statusbar = ttk.Label(
            self,
            textvariable=self.status
        )
        self.statusbar.grid(
            row=3,
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew"
        )

        self.columnconfigure(0, weight=1)

        self.records_saved = 0

        self.withdraw()

        if not self._show_login():
            self.destroy()
            return

        self.update_idletasks()
        self.center_window()
        self.deiconify()

    @staticmethod
    def _get_default_filename():
        date_string = datetime.today().strftime("%Y-%m-%d")
        return f"saba_data_record_{date_string}.csv"

    def center_window(self):
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    def on_save(self):
        errors = self.recordform.get_errors()

        if errors:
            fields = ", ".join(errors.keys())

            detail = (
                "The following fields have errors:\n\n"
                + "\n".join(
                    f"• {field}: {error}"
                    for field, error in errors.items()
                )
            )

            self.status.set(
                f"Cannot save. Errors in: {fields}"
            )

            messagebox.showerror(
                title="Validation Error",
                message="Cannot save record",
                detail=detail,
                parent=self
            )

            return False

        filename = self.filename.get().strip()

        if not filename:
            messagebox.showerror(
                title="File Error",
                message="Please select a CSV file.",
                parent=self
            )
            return False

        try:
            model = m.CSVModel(filename)
            data = self.recordform.get()
            model.save_record(data)

        except OSError as error:
            messagebox.showerror(
                title="File Error",
                message="The record could not be saved.",
                detail=str(error),
                parent=self
            )
            return False

        self.records_saved += 1

        self.status.set(
            f"{self.records_saved} records saved this session"
        )

        self.recordform.reset()
        return True

    def on_file_select(self):
        filename = filedialog.asksaveasfilename(
            parent=self,
            title="Select the target file for saving records",
            defaultextension=".csv",
            filetypes=[
                ("Comma-Separated Values", "*.csv *.CSV"),
                ("All Files", "*.*")
            ]
        )

        if filename:
            self.filename.set(filename)
            self.status.set(
                f"Target file: {filename}"
            )

    def save_settings(self, *args):
        for key, variable in self.settings.items():
            self.settings_model.set(
                key,
                variable.get()
            )

        self.settings_model.save()

    def load_settings(self):
        variable_types = {
            "bool": tk.BooleanVar,
            "str": tk.StringVar,
            "int": tk.IntVar,
            "float": tk.DoubleVar
        }

        self.settings = {}

        for key, data in self.settings_model.variables.items():
            variable_type = variable_types.get(
                data.get("type"),
                tk.StringVar
            )

            self.settings[key] = variable_type(
                value=data.get("value")
            )

        for variable in self.settings.values():
            variable.trace_add(
                "write",
                self.save_settings
            )

    @staticmethod
    def _simple_login(username, password):
        return (
            username == "saba"
            and password == "Flowers"
        )

    def _show_login(self):
        title = "Login to Saba Data Entry Application"
        error = ""

        while True:
            login = v.LoginDialog(
                self,
                title,
                error
            )

            if not login.result:
                return False

            username, password = login.result

            if self._simple_login(username, password):
                return True

            error = "Login failed"

