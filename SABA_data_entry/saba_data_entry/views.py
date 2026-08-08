import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkinter.simpledialog import Dialog
from . import widgets as w


class DataRecordForm(tk.Frame):
    """The input form for data records."""

    def __init__(self, parent, fields, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.settings = settings
        self.inputs = {}

        self.columnconfigure(0, weight=1)

        self.create_record_information_section(fields)
        self.create_environment_section(fields)
        self.create_plant_section(fields)
        self.create_notes_section(fields)

        # Fill default values
        self.reset()

    # ---------------------------------------------------------
    # Record Information
    # ---------------------------------------------------------

    def create_record_information_section(self, fields):
        recordinfo = tk.LabelFrame(
            self,
            text="Record Information",
            padx=5,
            pady=5
        )

        recordinfo.grid(
            row=0,
            column=0,
            padx=5,
            pady=(0, 5),
            sticky="ew"
        )

        recordinfo.columnconfigure(0, weight=1)
        recordinfo.columnconfigure(1, weight=1)
        recordinfo.columnconfigure(2, weight=1)

        self.inputs["Date"] = w.LabelInput(
            recordinfo,
            "Date",
            field_spec=fields["Date"]
        )
        self.inputs["Date"].grid(
            row=0,
            column=0,
            padx=3,
            pady=3,
            sticky="ew"
        )

        self.inputs["Time"] = w.LabelInput(
            recordinfo,
            "Time",
            field_spec=fields["Time"]
        )
        self.inputs["Time"].grid(
            row=0,
            column=1,
            padx=3,
            pady=3,
            sticky="ew"
        )

        self.inputs["Technician"] = w.LabelInput(
            recordinfo,
            "Technician",
            field_spec=fields["Technician"]
        )
        self.inputs["Technician"].grid(
            row=0,
            column=2,
            padx=3,
            pady=3,
            sticky="ew"
        )

        self.inputs["Lab"] = w.LabelInput(
            recordinfo,
            "Lab",
            field_spec=fields["Lab"]
        )
        self.inputs["Lab"].grid(
            row=1,
            column=0,
            padx=3,
            pady=3,
            sticky="ew"
        )

        self.inputs["Plot"] = w.LabelInput(
            recordinfo,
            "Plot",
            field_spec=fields["Plot"]
        )
        self.inputs["Plot"].grid(
            row=1,
            column=1,
            padx=3,
            pady=3,
            sticky="ew"
        )

        self.inputs["Seed sample"] = w.LabelInput(
            recordinfo,
            "Seed sample",
            field_spec=fields["Seed sample"]
        )
        self.inputs["Seed sample"].grid(
            row=1,
            column=2,
            padx=3,
            pady=3,
            sticky="ew"
        )

    # ---------------------------------------------------------
    # Environment Data
    # ---------------------------------------------------------

    def create_environment_section(self, fields):
        environmentinfo = tk.LabelFrame(
            self,
            text="Environment Data",
            padx=5,
            pady=5
        )

        environmentinfo.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        environmentinfo.columnconfigure(0, weight=1)
        environmentinfo.columnconfigure(1, weight=1)
        environmentinfo.columnconfigure(2, weight=1)

        self.inputs["Humidity"] = w.LabelInput(
            environmentinfo,
            "Humidity (g/m³)",
            field_spec=fields["Humidity"]
        )
        self.inputs["Humidity"].grid(
            row=0,
            column=0,
            padx=3,
            pady=3,
            sticky="ew"
        )

        self.inputs["Light"] = w.LabelInput(
            environmentinfo,
            "Light (klx)",
            field_spec=fields["Light"]
        )
        self.inputs["Light"].grid(
            row=0,
            column=1,
            padx=3,
            pady=3,
            sticky="ew"
        )

        self.inputs["Temperature"] = w.LabelInput(
            environmentinfo,
            "Temperature (°C)",
            field_spec=fields["Temperature"]
        )
        self.inputs["Temperature"].grid(
            row=0,
            column=2,
            padx=3,
            pady=3,
            sticky="ew"
        )

        self.inputs["Equipment Fault"] = w.LabelInput(
            environmentinfo,
            "Equipment Fault",
            field_spec=fields["Equipment Fault"]
        )
        self.inputs["Equipment Fault"].grid(
            row=1,
            column=0,
            columnspan=3,
            padx=3,
            pady=8,
            sticky="w"
        )

    # ---------------------------------------------------------
    # Plant Data
    # ---------------------------------------------------------

    def create_plant_section(self, fields):
        plantinfo = tk.LabelFrame(
            self,
            text="Plant Data",
            padx=5,
            pady=5
        )

        plantinfo.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        plantinfo.columnconfigure(0, weight=1)
        plantinfo.columnconfigure(1, weight=1)
        plantinfo.columnconfigure(2, weight=1)

        self.inputs["Plants"] = w.LabelInput(
            plantinfo,
            "Plants",
            field_spec=fields["Plants"]
        )
        self.inputs["Plants"].grid(
            row=0,
            column=0,
            padx=3,
            pady=3,
            sticky="ew"
        )

        self.inputs["Blossoms"] = w.LabelInput(
            plantinfo,
            "Blossoms",
            field_spec=fields["Blossoms"]
        )
        self.inputs["Blossoms"].grid(
            row=0,
            column=1,
            padx=3,
            pady=3,
            sticky="ew"
        )

        self.inputs["Fruit"] = w.LabelInput(
            plantinfo,
            "Fruit",
            field_spec=fields["Fruit"]
        )
        self.inputs["Fruit"].grid(
            row=0,
            column=2,
            padx=3,
            pady=3,
            sticky="ew"
        )

        # Variables used to validate height ranges
        min_height_var = tk.DoubleVar(value="-infinity")
        max_height_var = tk.DoubleVar(value="infinity")

        self.inputs["Min Height"] = w.LabelInput(
            plantinfo,
            "Min Height (cm)",
            field_spec=fields["Min Height"],
            input_args={
                "max_var": max_height_var,
                "focus_update_var": min_height_var
            }
        )
        self.inputs["Min Height"].grid(
            row=1,
            column=0,
            padx=3,
            pady=8,
            sticky="ew"
        )

        self.inputs["Max Height"] = w.LabelInput(
            plantinfo,
            "Max Height (cm)",
            field_spec=fields["Max Height"],
            input_args={
                "min_var": min_height_var,
                "focus_update_var": max_height_var
            }
        )
        self.inputs["Max Height"].grid(
            row=1,
            column=1,
            padx=3,
            pady=8,
            sticky="ew"
        )

        self.inputs["Median Height"] = w.LabelInput(
            plantinfo,
            "Median Height (cm)",
            field_spec=fields["Median Height"],
            input_args={
                "min_var": min_height_var,
                "max_var": max_height_var
            }
        )
        self.inputs["Median Height"].grid(
            row=1,
            column=2,
            padx=3,
            pady=8,
            sticky="ew"
        )

    # ---------------------------------------------------------
    # Notes
    # ---------------------------------------------------------

    def create_notes_section(self, fields):
        self.inputs["Notes"] = w.LabelInput(
            self,
            "Notes",
            field_spec=fields["Notes"],
            input_args={
                "width": 75,
                "height": 10
            }
        )

        self.inputs["Notes"].grid(
            row=3,
            column=0,
            padx=5,
            pady=(5, 0),
            sticky="ew"
        )

    # ---------------------------------------------------------
    # Data methods
    # ---------------------------------------------------------

    def get(self):

        data = {}

        for key, widget in self.inputs.items():
            data[key] = widget.get()

        return data

    def reset(self):

        lab = self.inputs["Lab"].get()
        time = self.inputs["Time"].get()
        technician = self.inputs["Technician"].get()
        plot = self.inputs["Plot"].get()

        plot_values = self.inputs["Plot"].input.cget("values")

        for widget in self.inputs.values():
            widget.set("")

        if self.settings["autofill date"].get():
            current_date = datetime.today().strftime("%Y-%m-%d")

            self.inputs["Date"].set(current_date)
            self.inputs["Time"].input.focus()

        if (
            self.settings["autofill sheet data"].get()
            and plot
            and plot_values
            and plot != plot_values[-1]
        ):
            self.inputs["Lab"].set(lab)
            self.inputs["Time"].set(time)
            self.inputs["Technician"].set(technician)

            next_plot_index = plot_values.index(plot) + 1
            self.inputs["Plot"].set(plot_values[next_plot_index])

            self.inputs["Seed sample"].input.focus()

    def get_errors(self):

        errors = {}

        for key, widget in self.inputs.items():

            if hasattr(widget.input, "trigger_focusout_validation"):
                widget.input.trigger_focusout_validation()

            if widget.error.get():
                errors[key] = widget.error.get()

        return errors


class MainMenu(tk.Menu):

    def __init__(self, parent, settings, callbacks, **kwargs):
        super().__init__(parent, **kwargs)

        # File menu
        file_menu = tk.Menu(self, tearoff=False)

        file_menu.add_command(
            label="Select file…",
            command=callbacks["file->select"]
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Quit",
            command=callbacks["file->quit"]
        )

        self.add_cascade(
            label="File",
            menu=file_menu
        )

        # Options menu
        options_menu = tk.Menu(self, tearoff=False)

        options_menu.add_checkbutton(
            label="Autofill Date",
            variable=settings["autofill date"]
        )

        options_menu.add_checkbutton(
            label="Autofill Sheet data",
            variable=settings["autofill sheet data"]
        )

        self.add_cascade(
            label="Options",
            menu=options_menu
        )

        # Help menu
        help_menu = tk.Menu(self, tearoff=False)

        help_menu.add_command(
            label="About…",
            command=self.show_about
        )

        self.add_cascade(
            label="Help",
            menu=help_menu
        )

    def show_about(self):
        """Show information about the application."""

        about_message = "Saba Data Entry"

        about_detail = (
            "by Saba Hesaraki\n"
            "For assistance please contact the author."
        )

        messagebox.showinfo(
            title="About",
            message=about_message,
            detail=about_detail
        )

class LoginDialog(Dialog):

    def __init__(self, parent , title , error=""):

       self._pw=tk.StringVar()
       self._user=tk.StringVar()
       self._error=tk.StringVar(value=error)
       super().__init__(parent , title=title)

    def body(self,frame):
        ttk.Label(frame,text="Loin to Saba's App").grid(row=0)

        if self._error.get():
            ttk.Label(frame,textvariable=self._error).grid(row=1)
        user_inp=w.LabelInput(frame,'User name:',input_class=w.RequiredEntry , var=self._user)

        user_inp.grid()

        w.LabelInput(frame,'Password:',input_class=w.RequiredEntry , var=self._pw).grid()

        return user_inp.input

    def buttonbox(self):
        box=ttk.Frame(self)
        ttk.Button(box,text="Login",command=self.ok , default=tk.ACTIVE).grid(padx=5,pady=5)
        ttk.Button(box,text="Cancel",command=self.cancel).grid(row=0, column=1,padx=5,pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def apply(self):
        self.result=(self._user.get(),self._pw.get())
