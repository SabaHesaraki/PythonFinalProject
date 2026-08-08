import tkinter as tk
from tkinter import ttk
from datetime import datetime


class DateEntry(ttk.Entry):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.error = tk.StringVar()

        self.configure(
            validate="all",
            validatecommand=(
                self.register(self._validate),
                "%P",
                "%V"
            ),
            invalidcommand=(
                self.register(self._on_invalid),
                "%V"
            )
        )

    def _toggle_error(self, error=""):
        self.error.set(error)
        self.config(foreground="red" if error else "black")

    def _validate(self, proposed, event):

        if event == "key":
            self._toggle_error()


            if proposed == "":
                return True


            if len(proposed) > 8:
                return False


            for index, char in enumerate(proposed):
                if index in (2, 5):
                    if char != "/":
                        return False
                else:
                    if not char.isdigit():
                        return False

            return True


        if event == "focusout":
            try:
                if len(proposed) != 8:
                    raise ValueError

                datetime.strptime(proposed, "%m/%d/%y")
                self._toggle_error()
                return True

            except ValueError:
                return False


        return True

    def _on_invalid(self, event):

        if event != "key":
            self._toggle_error(
                "Invalid date. Use MM/DD/YY, for example: 08/03/26"
            )


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Date Entry Validation")

    entry = DateEntry(root, width=15)
    entry.pack(padx=12, pady=(12, 4))

    error_label = ttk.Label(
        root,
        textvariable=entry.error,
        foreground="red"
    )
    error_label.pack(padx=12, pady=(0, 8))


    ttk.Entry(root).pack(padx=12, pady=(0, 12))

    root.mainloop()

