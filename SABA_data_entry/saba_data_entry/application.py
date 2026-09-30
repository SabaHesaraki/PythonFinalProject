from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk
from typing import Any

from .mainmenu import MainMenu
from .models import SQLModel, SettingsModel
from .views import DataRecordForm, LoginDialog, RecordList, setup_pastel_theme


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("SABA Data Entry Application 🌸")
        self.geometry("920x620")
        self.minsize(750, 480)

        self.settings = SettingsModel()
        self.model = SQLModel()

        setup_pastel_theme(self)

        self._init_settings_vars()


        self._build_ui()


        self._build_main_menu()


        self.after(100, self._show_login)

    def _init_settings_vars(self) -> None:

        current_font = tkfont.nametofont("TkDefaultFont")

        self.settings_vars: dict[str, Any] = {
            "font size": tk.IntVar(
                value=self.settings.get("font size") or current_font.cget("size")
            ),
            "font family": tk.StringVar(
                value=self.settings.get("font family") or current_font.cget("family")
            ),
            "theme": tk.StringVar(
                value=self.settings.get("theme") or ttk.Style().theme_use()
            ),
            "autofill date": tk.BooleanVar(value=True),
            "autofill sheet data": tk.BooleanVar(
                value=bool(self.settings.get("autofill sheet data"))
            ),
        }

        self.settings_vars["theme"].trace_add("write", self._on_theme_changed)
        self.settings_vars["font size"].trace_add("write", self._on_font_changed)
        self.settings_vars["font family"].trace_add("write", self._on_font_changed)

    def _on_theme_changed(self, *_) -> None:
        new_theme = self.settings_vars["theme"].get()
        try:
            ttk.Style().theme_use(new_theme)
            self.settings.set("theme", new_theme)
        except Exception:
            pass

    def _on_font_changed(self, *_) -> None:
        fam = self.settings_vars["font family"].get()
        sz = self.settings_vars["font size"].get()
        try:
            for fname in ("TkDefaultFont", "TkTextFont", "TkMenuFont"):
                tkfont.nametofont(fname).configure(family=fam, size=sz)
            self.settings.set("font family", fam)
            self.settings.set("font size", sz)
        except Exception:
            pass

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        callbacks = {
            "on_add": self._on_add_new,
            "on_edit": self._on_edit_record,
            "on_delete": self._on_delete_record,
        }
        self.record_list = RecordList(self, callbacks=callbacks)
        self.record_list.grid(row=0, column=0, sticky="nsew")

        self.status_var = tk.StringVar(value="Waiting for database login...")
        self.status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor="w",
            padding=(8, 4),
            foreground="#6C3483",
        )
        self.status_bar.grid(row=1, column=0, sticky="ew")

    def _build_main_menu(self) -> None:

        event_handlers = {
            "<<NewRecord>>": lambda e=None: self._on_add_new(),
            "<<RecordList>>": lambda e=None: self.record_list.focus_set(),
            "<<FileOpen>>": lambda e=None: self._show_login(),
            "<<FileQuit>>": lambda e=None: self._on_quit(),
            "<<HelpAbout>>": lambda e=None: self.show_about(),
        }


        for ev, fn in event_handlers.items():
            self.bind(ev, fn)
            self.bind_all(ev, fn)


        self.main_menu = MainMenu(
            self,
            settings=self.settings_vars,
            callbacks={},
        )
        self.config(menu=self.main_menu)

        action_map = {
            "New Record": self._on_add_new,
            "Record List": lambda: self.record_list.focus_set(),
            "Open file...": self._show_login,
            "About": self.show_about,
            "Exit": self._on_quit,
            "Quit": self._on_quit,
        }

        try:
            total_items = self.main_menu.index("end")
            if total_items is not None:
                for idx in range(total_items + 1):
                    try:
                        lbl = self.main_menu.entrycget(idx, "label")
                        if lbl in action_map:
                            self.main_menu.entryconfigure(idx, command=action_map[lbl])
                    except Exception:
                        pass
        except Exception:
            pass

        if hasattr(self.main_menu, "_menus"):
            for sub_menu in self.main_menu._menus.values():
                try:
                    sub_total = sub_menu.index("end")
                    if sub_total is not None:
                        for s_idx in range(sub_total + 1):
                            try:
                                lbl = sub_menu.entrycget(s_idx, "label")
                                if lbl in action_map:
                                    sub_menu.entryconfigure(s_idx, command=action_map[lbl])
                            except Exception:
                                pass
                except Exception:
                    pass

    def _on_quit(self) -> None:
        self.destroy()

    def _show_login(self) -> None:
        LoginDialog(self, on_success=self._connect_db)

    def _connect_db(self, db_params: dict[str, Any]) -> None:
        try:
            self.model.connect(**db_params)
            self.status_var.set(" Connected to PostgreSQL database successfully!")
            self._refresh_records()
        except Exception as e:
            self.status_var.set(" Database connection failed!")
            messagebox.showerror(
                "Connection Error", f"Could not connect to database:\n{e}"
            )
            self._show_login()

    def _refresh_records(self) -> None:
        try:
            records = self.model.get_all_records()
            self.record_list.populate(records)
        except Exception as e:
            messagebox.showerror("Query Error", f"Could not fetch records:\n{e}")

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
            record_data = self.model.get_record(rowkey)
            DataRecordForm(
                self,
                fields_schema=self.model.fields,
                initial_data=record_data,
                rowkey=rowkey,
                on_save=self._on_save_record,
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve record for edit:\n{e}")

    def _on_delete_record(self, rowkey: tuple[str, str, str, str]) -> None:
        try:
            self.model.delete_record(rowkey)
            self.status_var.set(f"Record {rowkey} deleted successfully.")
            self._refresh_records()
        except Exception as e:
            messagebox.showerror("Delete Error", f"Could not delete record:\n{e}")

    def _on_save_record(
        self,
        record_data: dict[str, Any],
        rowkey: tuple[str, str, str, str] | None,
    ) -> None:
        try:
            self.model.save_record(record_data, rowkey=rowkey)
            action = "updated" if rowkey else "saved"
            self.status_var.set(f"Record successfully {action}!")
            self._refresh_records()
        except Exception as e:
            messagebox.showerror("Database Save Error", f"Could not save the record:\n{e}")

    def show_about(self) -> None:
        messagebox.showinfo(
            title="About",
            message="SABA Data Entry Application \nVersion 2.0\nDeveloped with Tkinter & PostgreSQL",
        )
