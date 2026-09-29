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

    style.configure(".", background=BG_PINK, font=("Segoe UI", 9))
    style.configure("TFrame", background=BG_PINK)
    style.configure("TLabel", background=BG_PINK, foreground="#333333")

    style.configure(
        "TButton",
        background=BTN_PINK,
        foreground="#4A235A",
        relief="flat",
        padding=6,
        font=("Segoe UI", 9, "bold"),
    )
    style.map(
        "TButton",
        background=[("active", BTN_HOVER), ("pressed", "#D99BB4")],
        relief=[("pressed", "sunken"), ("!pressed", "flat")],
    )

    style.configure(
        "Treeview",
        background="#FFFFFF",
        fieldbackground="#FFFFFF",
        foreground="#333333",
        rowheight=25,
        bordercolor=HEADER_PINK,
    )
    style.configure(
        "Treeview.Heading",
        background=HEADER_PINK,
        foreground="#4A235A",
        font=("Segoe UI", 9, "bold"),
        relief="flat",
    )
    style.map("Treeview.Heading", background=[("active", BTN_PINK)])
    style.map("Treeview", background=[("selected", "#E8C1D9")], foreground=[("selected", "#000000")])


class LoginDialog(tk.Toplevel):
    def __init__(self, parent: tk.Tk, on_success: Callable[[dict[str, Any]], None]):
        super().__init__(parent)
        self.parent = parent
        self.on_success = on_success
        self.title("Connect to Database")
        self.geometry("380x370")
        self.resizable(False, False)
        self.configure(bg=BG_PINK)

        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.parent.destroy)

    def _build_ui(self) -> None:
        title_lbl = ttk.Label(
            self,
            text="🌸 Database Login 🌸",
            font=("Segoe UI", 12, "bold"),
            foreground=ACCENT_PURPLE,
        )
        title_lbl.pack(pady=(18, 12))

        form = ttk.Frame(self, padding=(25, 5))
        form.pack(fill=tk.BOTH, expand=True)

        self.vars = {
            "Host": tk.StringVar(value="localhost"),
            "Port": tk.StringVar(value="5432"),
            "Database": tk.StringVar(value="saba_data_entry"),
            "User": tk.StringVar(value="postgres"),
            "Password": tk.StringVar(value=""),
        }

        for i, (lbl_text, var) in enumerate(self.vars.items()):
            ttk.Label(form, text=f"{lbl_text}:", width=12, anchor="w").grid(row=i, column=0, pady=5, sticky="w")
            show_char = "*" if lbl_text == "Password" else ""
            ent = ttk.Entry(form, textvariable=var, show=show_char)
            ent.grid(row=i, column=1, pady=5, sticky="ew")

        form.columnconfigure(1, weight=1)

        btn_box = ttk.Frame(self, padding=15)
        btn_box.pack(fill=tk.X)

        connect_btn = ttk.Button(btn_box, text="Connect 💕", command=self._on_submit)
        connect_btn.pack(side=tk.LEFT, expand=True, padx=5)

        cancel_btn = ttk.Button(btn_box, text="Exit", command=self.parent.destroy)
        cancel_btn.pack(side=tk.RIGHT, expand=True, padx=5)

    def _on_submit(self) -> None:
        params = {
            "host": self.vars["Host"].get().strip(),
            "port": int(self.vars["Port"].get().strip() or 5432),
            "database": self.vars["Database"].get().strip(),
            "user": self.vars["User"].get().strip(),
            "password": self.vars["Password"].get(),
        }
        self.grab_release()
        self.destroy()
        self.on_success(params)


class RecordList(ttk.Frame):
    def __init__(self, parent, callbacks: dict[str, Callable] | None = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks or {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.columns = ("Date", "Time", "Lab", "Plot", "Seed Sample", "Humidity", "Light", "Temperature")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", selectmode="browse")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=95, anchor="center")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        self.scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)

        self.btn_frame = ttk.Frame(self)
        self.btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        self.add_btn = ttk.Button(self.btn_frame, text="✨ Add Record", command=self._on_add)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.edit_btn = ttk.Button(self.btn_frame, text="✏️ Edit Record", command=self._on_edit)
        self.edit_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = ttk.Button(self.btn_frame, text="🗑️ Delete Record", command=self._on_delete)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        self.tree.bind("<Double-1>", lambda event: self._on_edit())

    def populate(self, records: list[dict[str, Any]]) -> None:
        self.tree.delete(*self.tree.get_children())
        for rec in records:
            vals = [rec.get(col, "") for col in self.columns]
            self.tree.insert("", tk.END, values=vals)

    def get_selected_key(self) -> tuple[str, str, str, str] | None:
        selected_item = self.tree.selection()
        if not selected_item:
            return None
        values = self.tree.item(selected_item[0], "values")
        if len(values) >= 4:
            return (str(values[0]), str(values[1]), str(values[2]), str(values[3]))
        return None

    def _on_add(self) -> None:
        if "on_add" in self.callbacks:
            self.callbacks["on_add"]()

    def _on_edit(self) -> None:
        key = self.get_selected_key()
        if not key:
            messagebox.showwarning("Selection Required", "Please select a record from the list to edit.")
            return
        if "on_edit" in self.callbacks:
            self.callbacks["on_edit"](key)

    def _on_delete(self) -> None:
        key = self.get_selected_key()
        if not key:
            messagebox.showwarning("Selection Required", "Please select a record from the list to delete.")
            return
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this record?\n\nDate: {key[0]}\nTime: {key[1]}\nLab: {key[2]}\nPlot: {key[3]}",
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
        on_save: Callable[[dict[str, Any], tuple[str, str, str, str] | None], None] | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(parent, *args, **kwargs)
        self.fields_schema = fields_schema
        self.initial_data = initial_data or {}
        self.rowkey = rowkey
        self.on_save_cb = on_save
        self.variables = {}

        self.title("Edit Record 💕" if rowkey else "New Record 💕")
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
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, padding=15)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        header_text = "Edit Plot Record" if self.rowkey else "New Plot Record"
        ttk.Label(
            self.scrollable_frame,
            text=f"🌸 {header_text} 🌸",
            font=("Segoe UI", 12, "bold"),
            foreground=ACCENT_PURPLE,
        ).pack(anchor="w", pady=(0, 15))

        for field, meta in self.fields_schema.items():
            row_frame = ttk.Frame(self.scrollable_frame)
            row_frame.pack(fill=tk.X, pady=3)

            lbl_text = f"{field}:"
            lbl = ttk.Label(row_frame, text=lbl_text, width=16, anchor="w")
            lbl.pack(side=tk.LEFT)

            field_type = meta.get("type", "str")

            if "values" in meta:
                var = tk.StringVar()
                cb = ttk.Combobox(row_frame, textvariable=var, values=meta["values"], state="readonly")
                cb.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                if meta["values"] and not self.initial_data:
                    cb.set(meta["values"][0])
                self.variables[field] = var
            elif field_type == "bool":
                var = tk.StringVar(value="False")
                cb = ttk.Combobox(row_frame, textvariable=var, values=["True", "False"], state="readonly")
                cb.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                self.variables[field] = var
            else:
                var = tk.StringVar()
                entry = ttk.Entry(row_frame, textvariable=var, state="normal")
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
                messagebox.showerror("Validation Error", f"Field '{field}' is required!", parent=self)
                return

        if self.on_save_cb:
            self.on_save_cb(data, self.rowkey)
        self.destroy()
