from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

try:
    from .models import SQLModel, SettingsModel
    from .views import DataRecordForm, LoginDialog, RecordList, setup_pastel_theme
except ImportError:
    from models import SQLModel, SettingsModel
    from views import DataRecordForm, LoginDialog, RecordList, setup_pastel_theme


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("SABA Data Entry Application 💕")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.settings = SettingsModel()
        self.model = SQLModel()

        setup_pastel_theme(self)
        self._build_ui()

        self.after(100, self._show_login)

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.record_list = RecordList(
            self,
            callbacks={
                "on_add": self._on_add_new,
                "on_edit": self._on_edit_record,
                "on_delete": self._on_delete_record,
            },
        )
        self.record_list.grid(row=0, column=0, sticky="nsew")

        self.status_var = tk.StringVar(value="Ready. Please connect to database...")
        self.status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor="w",
            padding=(8, 4),
        )
        self.status_bar.grid(row=1, column=0, sticky="ew")

    def _show_login(self) -> None:
        LoginDialog(self, on_success=self._connect_db)

    def _connect_db(self, db_params: dict[str, Any]) -> None:
        try:
            self.model.connect(**db_params)
            self._load_records()
            self.status_var.set(f"Connected to database: {db_params.get('database')}")
            messagebox.showinfo("Success", "Connected to database successfully! 🌸")
        except Exception as e:
            self.status_var.set("Database connection failed.")
            messagebox.showerror("Connection Error", f"Could not connect to database:\n{e}")
            self.after(100, self._show_login)

    def _load_records(self) -> None:
        try:
            records = self.model.get_all_records()
            self.record_list.populate(records)
            self.status_var.set(f"Loaded {len(records)} records.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load records:\n{e}")

    def _on_add_new(self) -> None:
        DataRecordForm(
            self,
            fields_schema=self.model.fields,
            initial_data=None,
            rowkey=None,
            on_save=self._on_save_record,
        )

    def _on_edit_record(self, rowkey: tuple[str, str, str, str]) -> None:
        try:
            data = self.model.get_record(rowkey)
            if not data:
                messagebox.showwarning("Not Found", "Record not found in database.")
                return
            DataRecordForm(
                self,
                fields_schema=self.model.fields,
                initial_data=data,
                rowkey=rowkey,
                on_save=self._on_save_record,
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch record:\n{e}")

    def _on_save_record(self, data: dict[str, Any], rowkey: tuple[str, str, str, str] | None) -> None:
        try:
            self.model.save_record(data, rowkey)
            self._load_records()
            action = "updated" if rowkey else "saved"
            self.status_var.set(f"Record successfully {action}.")
            messagebox.showinfo("Saved", f"Record has been {action} successfully! 💕")
        except Exception as e:
            messagebox.showerror("Database Save Error", f"Could not save record:\n{e}")

    def _on_delete_record(self, rowkey: tuple[str, str, str, str]) -> None:
        try:
            self.model.delete_record(rowkey)
            self._load_records()
            self.status_var.set("Record deleted.")
            messagebox.showinfo("Deleted", "Record was successfully deleted.")
        except Exception as e:
            messagebox.showerror("Database Delete Error", f"Could not delete record:\n{e}")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
