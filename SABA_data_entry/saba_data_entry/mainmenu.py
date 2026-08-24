# mainmenu.py
import tkinter as tk
from tkinter import font, ttk
import image_utils


class MainMenu(tk.Menu):
    """Main menu of the application with font and theme options."""

    def __init__(self, parent, settings, callbacks):
        self.styles = {
            "tearoff": False,
            "background": "#FFF7FB",
            "foreground": "#58445F",
            "activebackground": "#F5C6D6",
            "activeforeground": "#4D3D50",
            "relief": tk.FLAT,
        }

        super().__init__(
            parent,
            tearoff=False,
            background="#E8DDF2",
            foreground="#58445F",
            activebackground="#F5C6D6",
            activeforeground="#4D3D50",
            relief=tk.FLAT,
        )

        self.callbacks = callbacks
        self.settings = settings

        self.add_icon = image_utils.load_xbm("add_16.xbm")
        self.quit_icon = image_utils.load_xbm("quit_16.xbm")

        self.file_menu = tk.Menu(self, **self.styles)
        self.file_menu.add_command(
            label="Open CSV File",
            command=self.callbacks["on_file_select"],
        )
        self.file_menu.add_command(
            label="New Record",
            image=self.add_icon,
            compound=tk.LEFT,
            command=self.callbacks["on_new_record"],
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Quit",
            image=self.quit_icon,
            compound=tk.LEFT,
            command=self.callbacks["on_quit"],
        )
        self.add_cascade(label="File", menu=self.file_menu)

        self.options_menu = tk.Menu(self, **self.styles)

        size_menu = tk.Menu(self.options_menu, **self.styles)
        self.options_menu.add_cascade(label="Font Size", menu=size_menu)
        for size in range(6, 17):
            size_menu.add_radiobutton(
                label=str(size),
                value=size,
                variable=self.settings["font size"],
            )

        family_menu = tk.Menu(self.options_menu, **self.styles)
        self.options_menu.add_cascade(label="Font Family", menu=family_menu)
        for family in font.families():
            family_menu.add_radiobutton(
                label=family,
                value=family,
                variable=self.settings["font family"],
            )

        theme_var = self.settings.get("theme")
        if theme_var is not None:
            theme_menu = tk.Menu(self.options_menu, **self.styles)
            self.options_menu.add_cascade(label="Theme", menu=theme_menu)
            style = ttk.Style(self)
            for theme_name in style.theme_names():
                theme_menu.add_radiobutton(
                    label=theme_name,
                    value=theme_name,
                    variable=theme_var,
                )

        self.add_cascade(label="Options", menu=self.options_menu)

        self.help_menu = tk.Menu(self, **self.styles)
        self.help_menu.add_command(
            label="About",
            command=self.callbacks["on_about"],
        )
        self.add_cascade(label="Help", menu=self.help_menu)
