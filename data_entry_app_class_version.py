from datetime import datetime
from pathlib import Path
import csv
import tkinter as tk
from tkinter import ttk


class BoundText(tk.Text):
    def __init__(self, *args, textvariable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._variable = textvariable

        if self._variable:
            self.insert("1.0", self._variable.get())
            self._variable.trace_add("write", self._set_content)
            self.bind("<<Modified>>", self._set_var)

    def _set_var(self, *_):
        if self.edit_modified():
            content = self.get("1.0", "end-1c")
            self._variable.set(content)
            self.edit_modified(False)

    def _set_content(self, *_):
        self.delete("1.0", tk.END)
        self.insert("1.0", self._variable.get())


class LabelInput(tk.Frame):
    def __init__(
        self,
        parent,
        label,
        var,
        input_class=ttk.Entry,
        input_args=None,
        label_args=None,
        **kwargs
    ):
        super().__init__(parent, **kwargs)

        input_args = input_args or {}
        label_args = label_args or {}

        self.variable = var


        if input_class in (ttk.Checkbutton, tk.Button):
            input_args["text"] = label
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky="ew")


        if input_class in (ttk.Checkbutton, tk.Button, ttk.Radiobutton):
            input_args["variable"] = self.variable
        else:
            input_args["textvariable"] = self.variable


        if input_class == ttk.Radiobutton:
            self.input = tk.Frame(self)
            values = input_args.pop("values", [])

            for value in values:
                button = ttk.Radiobutton(
                    self.input,
                    text=value,
                    value=value,
                    **input_args
                )
                button.pack(side=tk.LEFT, padx=5)
        else:
            self.input = input_class(self, **input_args)

        self.input.grid(row=1, column=0, sticky="ew")
        self.columnconfigure(0, weight=1)

    def grid(self, sticky="ew", **kwargs):
        super().grid(sticky=sticky, **kwargs)


class DataRecordForm(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self._vars = {
            "Date": tk.StringVar(),
            "Time": tk.StringVar(),
            "Technician": tk.StringVar(),
            "Lab": tk.StringVar(),
            "Plot": tk.IntVar(),
            "Seed Sample": tk.StringVar(),
            "Humidity": tk.DoubleVar(),
            "Light": tk.DoubleVar(),
            "Temperature": tk.DoubleVar(),
            "Equipment Fault": tk.BooleanVar(),
            "Plants": tk.IntVar(),
            "Blossoms": tk.IntVar(),
            "Fruit": tk.IntVar(),
            "Min Height": tk.DoubleVar(),
            "Max Height": tk.DoubleVar(),
            "Median Height": tk.DoubleVar(),
            "Notes": tk.StringVar(),
        }

        self.columnconfigure(0, weight=1)

        # Record Info
        record_info = self._add_frame("Record Info")

        LabelInput(record_info, "Date", var=self._vars["Date"]).grid(row=0, column=0, padx=5, pady=5)
        LabelInput(
            record_info,
            "Time",
            var=self._vars["Time"],
            input_class=ttk.Combobox,
            input_args={
                "values": ["8:00", "12:00", "16:00", "20:00"],
                "state": "readonly"
            }
        ).grid(row=0, column=1, padx=5, pady=5)

        LabelInput(record_info, "Technician", var=self._vars["Technician"]).grid(row=0, column=2, padx=5, pady=5)

        LabelInput(
            record_info,
            "Lab",
            var=self._vars["Lab"],
            input_class=ttk.Combobox,
            input_args={
                "values": ["A", "B", "C"],
                "state": "readonly"
            }
        ).grid(row=1, column=0, padx=5, pady=5)

        LabelInput(
            record_info,
            "Plot",
            var=self._vars["Plot"],
            input_class=ttk.Combobox,
            input_args={
                "values": list(range(1, 21)),
                "state": "readonly"
            }
        ).grid(row=1, column=1, padx=5, pady=5)

        LabelInput(record_info, "Seed Sample", var=self._vars["Seed Sample"]).grid(row=1, column=2, padx=5, pady=5)

        # Environment Data
        environment_info = self._add_frame("Environment Data")

        LabelInput(
            environment_info,
            "Humidity",
            var=self._vars["Humidity"],
            input_class=ttk.Spinbox,
            input_args={"from_": 0.5, "to": 52.0, "increment": 0.01}
        ).grid(row=0, column=0, padx=5, pady=5)

        LabelInput(
            environment_info,
            "Light",
            var=self._vars["Light"],
            input_class=ttk.Spinbox,
            input_args={"from_": 0, "to": 100, "increment": 0.01}
        ).grid(row=0, column=1, padx=5, pady=5)

        LabelInput(
            environment_info,
            "Temperature",
            var=self._vars["Temperature"],
            input_class=ttk.Spinbox,
            input_args={"from_": 4, "to": 40, "increment": 0.01}
        ).grid(row=0, column=2, padx=5, pady=5)

        LabelInput(
            environment_info,
            "Equipment Fault",
            var=self._vars["Equipment Fault"],
            input_class=ttk.Checkbutton
        ).grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Plant Data
        plant_info = self._add_frame("Plant Data")

        LabelInput(
            plant_info,
            "Plants",
            var=self._vars["Plants"],
            input_class=ttk.Spinbox,
            input_args={"from_": 0, "to": 20}
        ).grid(row=0, column=0, padx=5, pady=5)

        LabelInput(
            plant_info,
            "Blossoms",
            var=self._vars["Blossoms"],
            input_class=ttk.Spinbox,
            input_args={"from_": 0, "to": 1000}
        ).grid(row=0, column=1, padx=5, pady=5)

        LabelInput(
            plant_info,
            "Fruit",
            var=self._vars["Fruit"],
            input_class=ttk.Spinbox,
            input_args={"from_": 0, "to": 1000}
        ).grid(row=0, column=2, padx=5, pady=5)

        LabelInput(
            plant_info,
            "Min Height",
            var=self._vars["Min Height"],
            input_class=ttk.Spinbox,
            input_args={"from_": 0, "to": 1000, "increment": 0.01}
        ).grid(row=1, column=0, padx=5, pady=5)

        LabelInput(
            plant_info,
            "Max Height",
            var=self._vars["Max Height"],
            input_class=ttk.Spinbox,
            input_args={"from_": 0, "to": 1000, "increment": 0.01}
        ).grid(row=1, column=1, padx=5, pady=5)

        LabelInput(
            plant_info,
            "Median Height",
            var=self._vars["Median Height"],
            input_class=ttk.Spinbox,
            input_args={"from_": 0, "to": 1000, "increment": 0.01}
        ).grid(row=1, column=2, padx=5, pady=5)

        # Notes
        LabelInput(
            self,
            "Notes",
            var=self._vars["Notes"],
            input_class=BoundText,
            input_args={"width": 75, "height": 10}
        ).grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        # Buttons
        buttons = ttk.Frame(self)
        buttons.grid(row=4, column=0, sticky="ew", padx=5, pady=10)

        self.save_button = ttk.Button(buttons, text="Save", command=self.master._on_save)
        self.save_button.pack(side=tk.RIGHT)

    def _add_frame(self, label, cols=3):
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky="ew", padx=5, pady=5)

        for i in range(cols):
            frame.columnconfigure(i, weight=1)

        return frame

    def reset(self):
        for var in self._vars.values():
            if isinstance(var, tk.BooleanVar):
                var.set(False)
            elif isinstance(var, tk.IntVar):
                var.set(0)
            elif isinstance(var, tk.DoubleVar):
                var.set(0.0)
            else:
                var.set("")

    def get(self):
        data = {}
        fault = self._vars["Equipment Fault"].get()

        for key, variable in self._vars.items():
            if fault and key in ("Light", "Temperature", "Humidity"):
                data[key] = ""
            else:
                try:
                    data[key] = variable.get()
                except tk.TclError:
                    raise ValueError(f"Error in field: {key}. Data was not saved!")

        return data


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Saba Data Entry Application")
        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="Saba Data Entry Application",
            font=("TkDefaultFont", 16)
        ).grid(row=0, column=0, padx=10, pady=10)

        self.record_form = DataRecordForm(self)
        self.record_form.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.status).grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self._records_saved = 0

    def _on_save(self):
        datestring = datetime.today().strftime("%Y_%m_%d")
        filename = f"saba_data_record_{datestring}.csv"
        newfile = not Path(filename).exists()

        try:
            data = self.record_form.get()
        except ValueError as e:
            self.status.set(str(e))
            return

        with open(filename, "a", newline="", encoding="utf-8") as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())

            if newfile:
                csvwriter.writeheader()

            csvwriter.writerow(data)

        self._records_saved += 1
        self.status.set(f"{self._records_saved} record(s) saved this session")
        self.record_form.reset()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
