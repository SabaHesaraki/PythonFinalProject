import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Menu):
    def __init__(self, parent, settings, **kwargs):
        super().__init__(parent, **kwargs)
        self.settings = settings

        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label="About...", command=self.show_about)

        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="Select File...", command=self._event('<<FileSelect>>'))
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self._event('<<FileQuit>>'))

        options_menu = tk.Menu(self, tearoff=False)
        options_menu.add_checkbutton(
            label='Autofill Date',
            variable=self.settings['autofill date'],
        )
        options_menu.add_checkbutton(
            label='Autofill Sheet data',
            variable=self.settings['autofill sheet data'],
        )

        self.add_cascade(label="File", menu=file_menu)
        self.add_cascade(label="Options", menu=options_menu)
        self.add_cascade(label="Help", menu=help_menu)

    def show_about(self):
        about_message = "Saba Data Entry"
        about_detail = 'by Saba Hesaraki\nFor assistance please contact the author'
        messagebox.showinfo(title="About", message=about_message, detail=about_detail)

    def _event(self, sequence):
        def callback(*_):

            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback
