import tkinter as tk
from tkinter import messagebox, ttk


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.parent = parent
        self.on_success = on_success

        self.title("Database Login")
        self.geometry("340x180")
        self.resizable(False, False)

        self.username_var = tk.StringVar(value="postgres")
        self.secret_key_var = tk.StringVar()

        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Username:").grid(
            row=0, column=0, sticky="w", padx=5, pady=6
        )
        self.user_entry = ttk.Entry(
            frame, textvariable=self.username_var, width=22
        )
        self.user_entry.grid(row=0, column=1, padx=5, pady=6)


        ttk.Label(frame, text="Secret Key:").grid(
            row=1, column=0, sticky="w", padx=5, pady=6
        )
        self.key_entry = ttk.Entry(
            frame, textvariable=self.secret_key_var, show="*", width=22
        )
        self.key_entry.grid(row=1, column=1, padx=5, pady=6)


        btn_box = ttk.Frame(frame)
        btn_box.grid(row=2, column=0, columnspan=2, pady=(15, 0))

        login_btn = ttk.Button(btn_box, text="Connect", command=self._login)
        login_btn.pack(side="left", padx=5)

        cancel_btn = ttk.Button(btn_box, text="Exit", command=self.parent.destroy)
        cancel_btn.pack(side="left", padx=5)


        self.bind("<Return>", lambda _: self._login())
        self.transient(parent)
        self.grab_set()
        self.key_entry.focus_set()

    def _login(self):
        user = self.username_var.get().strip()
        auth_key = self.secret_key_var.get()

        if not user:
            messagebox.showwarning(
                "Warning", "Username cannot be empty!", parent=self
            )
            return

        self.destroy()

        self.on_success(user, auth_key)
