import platform
import tkinter as tk
from tkinter import font, ttk


class GenericMainMenu(tk.Menu):

    def __init__(self, parent, settings, callbacks, **kwargs):
        self._keybinds = {
            "<Control-o>": self._event("<<FileOpen>>"),
            "<Control-n>": self._event("<<NewRecord>>"),
            "<Control-r>": self._event("<<RecordList>>"),
            "<Control-q>": self._event("<<FileQuit>>"),
        }
        self.parent = parent
        self.settings = settings
        self.callbacks = callbacks
        self._menus = {}

        super().__init__(parent, **kwargs)

        self._create_icons()
        self._build_menu()
        self._bind_accelerators()

    def _event(self, sequence):
        def callback(*_):
            root = self.winfo_toplevel()
            root.event_generate(sequence)

        return callback

    def _bind_accelerators(self):
        for seq, callback in self._keybinds.items():
            if callback:
                self.parent.bind_all(seq, callback)

    def _create_icons(self):
        self.icons = {}

    def _add_file_open(self, menu):
        menu.add_command(
            label="Open file...",
            command=self._event("<<FileOpen>>"),
            accelerator="Ctrl+O",
        )

    def _add_go_record_list(self, menu):
        menu.add_command(
            label="Record List",
            command=self._event("<<RecordList>>"),
            accelerator="Ctrl+R",
            image=self.icons.get("record_list"),
            compound=tk.LEFT,
        )

    def _add_go_new_record(self, menu):
        menu.add_command(
            label="New Record",
            command=self._event("<<NewRecord>>"),
            accelerator="Ctrl+N",
            image=self.icons.get("new_record"),
            compound=tk.LEFT,
        )

    def _add_quit(self, menu):
        menu.add_command(
            label="Quit",
            command=self._event("<<FileQuit>>"),
            accelerator="Ctrl+Q",
            image=self.icons.get("quit"),
            compound=tk.LEFT,
        )

    def _add_font_size_menu(self, menu):
        size_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Font Size", menu=size_menu)
        for size in range(6, 17):
            size_menu.add_radiobutton(
                label=str(size),
                value=size,
                variable=self.settings.get("font size"),
            )

    def _add_font_family_menu(self, menu):
        family_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Font Family", menu=family_menu)
        for family in font.families():
            family_menu.add_radiobutton(
                label=family,
                value=family,
                variable=self.settings.get("font family"),
            )

    def _add_themes_menu(self, menu):
        theme_var = self.settings.get("theme")
        if theme_var is not None:
            theme_menu = tk.Menu(menu, tearoff=False)
            menu.add_cascade(label="Theme", menu=theme_menu)
            for theme_name in ttk.Style().theme_names():
                theme_menu.add_radiobutton(
                    label=theme_name,
                    value=theme_name,
                    variable=theme_var,
                )

    def _add_autofill_date(self, menu):
        if "autofill date" in self.settings:
            menu.add_checkbutton(
                label="Autofill Date",
                variable=self.settings["autofill date"],
            )

    def _add_autofill_sheet(self, menu):
        if "autofill sheet data" in self.settings:
            menu.add_checkbutton(
                label="Autofill Sheet Data",
                variable=self.settings["autofill sheet data"],
            )

    def _add_about(self, menu):
        menu.add_command(
            label="About",
            command=self._event("<<HelpAbout>>"),
        )

    def _build_menu(self):
        pass


class WindowsMainMenu(GenericMainMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keybinds.pop("<Control-q>", None)

    def _create_icons(self):
        super()._create_icons()
        self.icons.pop("new_record", None)
        self.icons.pop("record_list", None)

    def _add_quit(self, menu):
        menu.add_command(
            label="Exit",
            command=self._event("<<FileQuit>>"),
            image=self.icons.get("quit"),
            compound=tk.LEFT,
        )

    def _build_menu(self):
        self._menus["File"] = tk.Menu(self, tearoff=False)
        self._add_file_open(self._menus["File"])
        self._menus["File"].add_separator()
        self._add_quit(self._menus["File"])

        self._menus["Tools"] = tk.Menu(self, tearoff=False)
        self._add_autofill_date(self._menus["Tools"])
        self._add_autofill_sheet(self._menus["Tools"])
        self._add_font_size_menu(self._menus["Tools"])
        self._add_font_family_menu(self._menus["Tools"])
        self._add_themes_menu(self._menus["Tools"])

        self._menus["Help"] = tk.Menu(self, tearoff=False)
        self._add_about(self._menus["Help"])

        self.add_cascade(label="File", menu=self._menus["File"])
        self.add_command(
            label="Record List",
            command=self._event("<<RecordList>>"),
        )
        self.add_command(
            label="New Record",
            command=self._event("<<NewRecord>>"),
        )
        self.add_cascade(label="Tools", menu=self._menus["Tools"])
        self.add_cascade(label="Help", menu=self._menus["Help"])


class LinuxMainMenu(GenericMainMenu):

    styles = {
        "background": "#333",
        "foreground": "white",
        "activebackground": "#777",
        "activeforeground": "white",
        "relief": tk.GROOVE,
    }

    def _build_menu(self):
        self._menus["File"] = tk.Menu(self, tearoff=False, **self.styles)
        self._add_file_open(self._menus["File"])
        self._menus["File"].add_separator()
        self._add_quit(self._menus["File"])

        self._menus["Edit"] = tk.Menu(self, tearoff=False, **self.styles)
        self._add_autofill_date(self._menus["Edit"])
        self._add_autofill_sheet(self._menus["Edit"])

        self._menus["Go"] = tk.Menu(self, tearoff=False, **self.styles)
        self._add_go_record_list(self._menus["Go"])
        self._add_go_new_record(self._menus["Go"])

        self._menus["View"] = tk.Menu(self, tearoff=False, **self.styles)
        self._add_font_size_menu(self._menus["View"])
        self._add_font_family_menu(self._menus["View"])
        self._add_themes_menu(self._menus["View"])

        self._menus["Help"] = tk.Menu(self, tearoff=False, **self.styles)
        self._add_about(self._menus["Help"])

        self.add_cascade(label="File", menu=self._menus["File"])
        self.add_cascade(label="Edit", menu=self._menus["Edit"])
        self.add_cascade(label="Go", menu=self._menus["Go"])
        self.add_cascade(label="View", menu=self._menus["View"])
        self.add_cascade(label="Help", menu=self._menus["Help"])


class MacOsMainMenu(GenericMainMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keybinds = {
            "<Command-o>": self._event("<<FileOpen>>"),
            "<Command-n>": self._event("<<NewRecord>>"),
            "<Command-r>": self._event("<<RecordList>>"),
        }

    def _add_file_open(self, menu):
        menu.add_command(
            label="Open file...",
            command=self._event("<<FileOpen>>"),
            accelerator="Cmd+O",
        )

    def _add_go_record_list(self, menu):
        menu.add_command(
            label="Record List",
            command=self._event("<<RecordList>>"),
            accelerator="Cmd+R",
        )

    def _add_go_new_record(self, menu):
        menu.add_command(
            label="New Record",
            command=self._event("<<NewRecord>>"),
            accelerator="Cmd+N",
        )

    def _build_menu(self):
        self._menus["File"] = tk.Menu(self, tearoff=False)
        self._add_file_open(self._menus["File"])

        self._menus["Edit"] = tk.Menu(self, tearoff=False)
        self._add_autofill_date(self._menus["Edit"])
        self._add_autofill_sheet(self._menus["Edit"])

        self._menus["Go"] = tk.Menu(self, tearoff=False)
        self._add_go_record_list(self._menus["Go"])
        self._add_go_new_record(self._menus["Go"])

        self._menus["View"] = tk.Menu(self, tearoff=False)
        self._add_font_size_menu(self._menus["View"])
        self._add_font_family_menu(self._menus["View"])

        self._menus["Help"] = tk.Menu(self, tearoff=False)
        self._add_about(self._menus["Help"])

        self.add_cascade(label="File", menu=self._menus["File"])
        self.add_cascade(label="Edit", menu=self._menus["Edit"])
        self.add_cascade(label="Go", menu=self._menus["Go"])
        self.add_cascade(label="View", menu=self._menus["View"])
        self.add_cascade(label="Help", menu=self._menus["Help"])


def get_main_menu_for_os(os_name):
    menus = {
        "Linux": LinuxMainMenu,
        "Darwin": MacOsMainMenu,
        "Windows": WindowsMainMenu,
    }
    return menus.get(os_name, GenericMainMenu)


MainMenu = get_main_menu_for_os(platform.system())
