# login.py
import tkinter as tk
from tkinter import ttk


class LoginWindow(tk.Toplevel):
    USERNAME = "Saba"
    PASSWORD = "Flowers"

    def __init__(self, parent, on_success):
        super().__init__(parent)

        self.parent = parent
        self.on_success = on_success

        self.title("SABA Login")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(bg="#FFF7FB")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.message_var = tk.StringVar()

        self.create_widgets()
        self.center_window()

        self.bind("<Return>", self.check_login)
        self.protocol("WM_DELETE_WINDOW", self.close_application)

        self.grab_set()
        self.deiconify()
        self.lift()
        self.focus_force()
        self.username_entry.focus_set()

    def center_window(self):
        self.update_idletasks()

        width = 400
        height = 300
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        frame = ttk.Frame(self, padding=(25, 20, 25, 15))
        frame.pack(fill=tk.BOTH, expand=True)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(5, weight=1)

        title_label = ttk.Label(
            frame,
            text="SABA Data Entry Login",
            font=("Arial", 15, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(0, 14))

        ttk.Label(frame, text="Username").grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 4),
        )

        self.username_entry = ttk.Entry(
            frame,
            textvariable=self.username_var,
        )
        self.username_entry.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 10),
        )

        ttk.Label(frame, text="Password").grid(
            row=3,
            column=0,
            sticky="w",
            pady=(0, 4),
        )

        self.password_entry = ttk.Entry(
            frame,
            textvariable=self.password_var,
            show="*",
        )
        self.password_entry.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(0, 5),
        )

        message_label = tk.Label(
            frame,
            textvariable=self.message_var,
            fg="#B23A3A",
            bg="#FFF7FB",
            font=("Arial", 9, "bold"),
        )
        message_label.grid(
            row=5,
            column=0,
            sticky="w",
            pady=(0, 4),
        )

        login_button = ttk.Button(
            frame,
            text="Login",
            command=self.check_login,
        )
        login_button.grid(
            row=6,
            column=0,
            sticky="e",
            pady=(2, 0),
        )

    def check_login(self, event=None):
        if (
            self.username_var.get() == self.USERNAME
            and self.password_var.get() == self.PASSWORD
        ):
            self.grab_release()
            self.destroy()
            self.on_success()
        else:
            self.message_var.set("Incorrect username or password.")
            self.password_var.set("")
            self.password_entry.focus_set()

    def close_application(self):
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()
        self.parent.destroy()
