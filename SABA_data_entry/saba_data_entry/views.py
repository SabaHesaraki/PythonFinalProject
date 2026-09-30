from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Callable

BG_PINK = "#FFF0F5"
HEADER_PINK = "#F8D7E3"
BTN_PINK = "#F3C5D8"
BTN_HOVER = "#E8AFC6"
ACCENT_PURPLE = "#8E44AD"


def setup_pastel_theme(root: tk.Tk) -> None:
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    root.configure(bg=BG_PINK)

    style.configure(".", background=BG_PINK, font=("Segoe UI", 10))
    style.configure("TFrame", background=BG_PINK)
    style.configure("TLabel", background=BG_PINK, foreground="#4A235A")

    style.configure(
        "TButton",
        background=BTN_PINK,
        foreground="#4A235A",
        borderwidth=1,
        relief="raised",
        font=("Segoe UI", 10, "bold"),
    )
    style.map(
        "TButton",
        background=[("active", BTN_HOVER), ("pressed", "#D99BB4")],
        relief=[("pressed", "sunken")],
    )

    style.configure(
        "Treeview",
        background="#FFFFFF",
        fieldbackground="#FFFFFF",
        foreground="#2C3E50",
        rowheight=26,
    )
    style.map(
        "Treeview",
        background=[("selected", HEADER_PINK)],
        foreground=[("selected", "#4A235A")],
    )

    style.configure(
        "Treeview.Heading",
        background=HEADER_PINK,
        foreground="#6C3483",
        font=("Segoe UI", 10, "bold"),
    )
    style.map(
        "Treeview.Heading",
        background=[("active", BTN_PINK)],
    )


class LoginDialog(tk.Toplevel):

    def __init__(
        self, parent: tk.Tk, on_success: Callable[[dict[str, Any]], None]
    ):
        super().__init__(parent)
        self.parent = parent
        self.on_success = on_success

        self.title("Connect to Database")
        self.geometry("380x370")
        self.resizable(False, False)
        self.configure(bg=BG_PINK)

        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.parent.destroy)

        self._build_ui()
        self.center_window()

    def center_window(self) -> None:
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"+{x}+{y}")

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame,
            text="PostgreSQL Login ",
            font=("Segoe UI", 13, "bold"),
            foreground=ACCENT_PURPLE,
        ).pack(pady=(0, 15))

        self.entries = {}
        fields = [
            ("Host", "localhost"),
            ("Port", "5432"),
            ("Database", "saba_data_entry"),
            ("User", "postgres"),
            ("Password", ""),
        ]

        for label, default in fields:
            row = ttk.Frame(frame)
            row.pack(fill=tk.X, pady=4)
            ttk.Label(row, text=f"{label}:", width=10, anchor="w").pack(
                side=tk.LEFT
            )
            show = "*" if label == "Password" else ""
            ent = ttk.Entry(row, show=show)
            ent.insert(0, default)
            ent.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.entries[label.lower()] = ent

        btn_box = ttk.Frame(frame)
        btn_box.pack(fill=tk.X, pady=(20, 0))

        submit_btn = ttk.Button(
            btn_box, text="Connect ", command=self._on_submit
        )
        submit_btn.pack(side=tk.LEFT, expand=True, padx=5, ipady=3)

        exit_btn = ttk.Button(btn_box, text="Exit", command=self.parent.destroy)
        exit_btn.pack(side=tk.RIGHT, expand=True, padx=5, ipady=3)

        self.entries["password"].focus_set()

    def _on_submit(self) -> None:
        params = {k: v.get().strip() for k, v in self.entries.items()}
        try:
            params["port"] = int(params["port"])
        except ValueError:
            messagebox.showerror(
                "Error", "Port must be an integer!", parent=self
            )
            return

        self.grab_release()
        self.destroy()
        self.on_success(params)


class RecordList(ttk.Frame):

    def __init__(
        self,
        parent,
        callbacks: dict[str, Callable] | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks or {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        cols = (
            "Date",
            "Time",
            "Lab",
            "Plot",
            "Seed Sample",
            "Humidity",
            "Light",
            "Temperature",
        )
        self.tree = ttk.Treeview(
            self, columns=cols, show="headings", selectmode="browse"
        )

        for c in cols:
            self.tree.heading(c, text=c)
            width = 80 if c in ("Lab", "Plot", "Time") else 100
            self.tree.column(c, width=width, anchor="center")

        self.scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        self.scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)

        self.btn_frame = ttk.Frame(self)
        # رفع ارور: تغییر fill=tk.X به sticky="ew"
        self.btn_frame.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10)
        )

        self.add_btn = ttk.Button(
            self.btn_frame, text="✨ Add Record", command=self._on_add
        )
        self.add_btn.pack(side=tk.LEFT, padx=4, ipady=2)

        self.edit_btn = ttk.Button(
            self.btn_frame, text="✏️ Edit Record", command=self._on_edit
        )
        self.edit_btn.pack(side=tk.LEFT, padx=4, ipady=2)

        self.delete_btn = ttk.Button(
            self.btn_frame, text="🗑️ Delete Record", command=self._on_delete
        )
        self.delete_btn.pack(side=tk.LEFT, padx=4, ipady=2)

        self.tree.bind("<Double-1>", lambda e: self._on_edit())

    def populate(self, records: list[dict[str, Any]]) -> None:
        self.tree.delete(*self.tree.get_children())
        for r in records:
            values = [r.get(col, "") for col in self.tree["columns"]]
            self.tree.insert("", tk.END, values=values)

    def get_selected_key(self) -> tuple[str, str, str, str] | None:
        selected = self.tree.selection()
        if not selected:
            return None
        values = self.tree.item(selected[0], "values")
        if not values or len(values) < 4:
            return None
        return (str(values[0]), str(values[1]), str(values[2]), str(values[3]))

    def _on_add(self) -> None:
        if "on_add" in self.callbacks:
            self.callbacks["on_add"]()

    def _on_edit(self) -> None:
        key = self.get_selected_key()
        if not key:
            messagebox.showwarning(
                "Notice", "Please select a record from the list to edit."
            )
            return
        if "on_edit" in self.callbacks:
            self.callbacks["on_edit"](key)

    def _on_delete(self) -> None:
        key = self.get_selected_key()
        if not key:
            messagebox.showwarning(
                "Notice", "Please select a record from the list to delete."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete record:\nDate: {key[0]} | Time: {key[1]} | Lab: {key[2]} | Plot: {key[3]}?",
        )
        if confirm and "on_delete" in self.callbacks:
            self.callbacks["on_delete"](key)


class DataRecordForm(tk.Toplevel):

    def __init__(
        self,
        parent,
        fields_schema: dict[str, Any],
        initial_data: dict[str, Any] | None = None,
        rowkey: tuple[str, str, str, str] | None = None,
        on_save: (
            Callable[[dict[str, Any], tuple[str, str, str, str] | None], None]
            | None
        ) = None,
        *args,
        **kwargs,
    ):
        super().__init__(parent, *args, **kwargs)
        self.fields_schema = fields_schema
        self.initial_data = initial_data or {}
        self.rowkey = rowkey
        self.on_save_cb = on_save
        self.variables: dict[str, tk.StringVar] = {}

        self.title("Edit Record " if rowkey else "New Record 💕")
        self.geometry("470x650")
        self.minsize(420, 520)
        self.configure(bg=BG_PINK)

        self._build_ui()
        if self.initial_data:
            self.load_record(self.initial_data)

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, highlightthickness=0, bg=BG_PINK)
        scrollbar = ttk.Scrollbar(
            main_frame, orient="vertical", command=canvas.yview
        )
        self.scrollable_frame = ttk.Frame(canvas, padding=15)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas_window = canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(canvas_window, width=e.width),
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        header_text = "Edit Plot Record" if self.rowkey else "New Plot Record"
        ttk.Label(
            self.scrollable_frame,
            text=f" {header_text} ",
            font=("Segoe UI", 12, "bold"),
            foreground=ACCENT_PURPLE,
        ).pack(anchor="w", pady=(0, 15))

        pk_fields = {"Date", "Time", "Lab", "Plot"}

        for field, meta in self.fields_schema.items():
            row_frame = ttk.Frame(self.scrollable_frame)
            row_frame.pack(fill=tk.X, pady=3)

            req_marker = " *" if meta.get("req", False) else ""
            lbl_text = f"{field}{req_marker}:"
            lbl = ttk.Label(row_frame, text=lbl_text, width=16, anchor="w")
            lbl.pack(side=tk.LEFT)

            field_type = meta.get("type", "str")
            is_pk_in_edit = self.rowkey is not None and field in pk_fields

            if "values" in meta:
                var = tk.StringVar()
                state = "disabled" if is_pk_in_edit else "readonly"
                cb = ttk.Combobox(
                    row_frame,
                    textvariable=var,
                    values=meta["values"],
                    state=state,
                )
                cb.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                if meta["values"] and not self.initial_data:
                    cb.set(meta["values"][0])
                self.variables[field] = var
            elif field_type == "bool":
                var = tk.StringVar(value="False")
                cb = ttk.Combobox(
                    row_frame,
                    textvariable=var,
                    values=["True", "False"],
                    state="readonly",
                )
                cb.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                self.variables[field] = var
            else:
                var = tk.StringVar()
                state = "readonly" if is_pk_in_edit else "normal"
                entry = ttk.Entry(row_frame, textvariable=var, state=state)
                entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                self.variables[field] = var

        btn_box = ttk.Frame(self.scrollable_frame)
        btn_box.pack(fill=tk.X, pady=(20, 10))

        save_btn = ttk.Button(btn_box, text="Save Record 💾", command=self._save)
        save_btn.pack(side=tk.LEFT, expand=True, padx=5, ipady=3)

        cancel_btn = ttk.Button(btn_box, text="Cancel", command=self.destroy)
        cancel_btn.pack(side=tk.RIGHT, expand=True, padx=5, ipady=3)

    def load_record(self, data: dict[str, Any]) -> None:
        for k, v in data.items():
            if k in self.variables:
                self.variables[k].set("" if v is None else str(v))

    def get_data(self) -> dict[str, Any]:
        return {k: var.get().strip() for k, var in self.variables.items()}

    def _save(self) -> None:
        data = self.get_data()


        for field, meta in self.fields_schema.items():
            if meta.get("req", False) and not data.get(field):
                messagebox.showerror(
                    "Validation Error",
                    f"Field '{field}' is required!",
                    parent=self,
                )
                return


        numeric_values: dict[str, float] = {}
        for field, meta in self.fields_schema.items():
            val_str = data.get(field, "")
            if not val_str:
                continue

            ftype = meta.get("type")
            frange = meta.get("range")

            if ftype == "int":
                try:
                    val_int = int(val_str)
                    if frange and not (frange[0] <= val_int <= frange[1]):
                        messagebox.showerror(
                            "Validation Error",
                            f"Field '{field}' must be between {frange[0]} and"
                            f" {frange[1]}!",
                            parent=self,
                        )
                        return
                    numeric_values[field] = float(val_int)
                except ValueError:
                    messagebox.showerror(
                        "Validation Error",
                        f"Field '{field}' must be an integer!",
                        parent=self,
                    )
                    return

            elif ftype == "decimal":
                try:
                    val_float = float(val_str)
                    if frange and not (frange[0] <= val_float <= frange[1]):
                        messagebox.showerror(
                            "Validation Error",
                            f"Field '{field}' must be between {frange[0]} and"
                            f" {frange[1]}!",
                            parent=self,
                        )
                        return
                    numeric_values[field] = val_float
                except ValueError:
                    messagebox.showerror(
                        "Validation Error",
                        f"Field '{field}' must be a number!",
                        parent=self,
                    )
                    return

        # ۳ Min Height <= Median Height <= Max Height
        min_h = numeric_values.get("Min Height")
        med_h = numeric_values.get("Median Height")
        max_h = numeric_values.get("Max Height")

        if min_h is not None and max_h is not None and min_h > max_h:
            messagebox.showerror(
                "Validation Error",
                "Min Height cannot be greater than Max Height!",
                parent=self,
            )
            return

        if med_h is not None:
            if min_h is not None and med_h < min_h:
                messagebox.showerror(
                    "Validation Error",
                    "Median Height cannot be less than Min Height!",
                    parent=self,
                )
                return
            if max_h is not None and med_h > max_h:
                messagebox.showerror(
                    "Validation Error",
                    "Median Height cannot be greater than Max Height!",
                    parent=self,
                )
                return

        if self.on_save_cb:
            self.on_save_cb(data, self.rowkey)
        self.destroy()
