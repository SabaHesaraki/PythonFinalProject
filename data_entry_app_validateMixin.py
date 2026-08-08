import os
from decimal import Decimal, InvalidOperation
from datetime import datetime
from pathlib import Path
import csv
import tkinter as tk
from tkinter import ttk

try:
    from data_entry_main import ValidatedCombobox
except ImportError:
    ValidatedCombobox = None

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

class ValidateMixin:
    def __init__(self, *args, error_var=None, on_error_toggle=None, **kwargs):
        self.error = error_var or tk.StringVar()
        self.on_error_toggle = on_error_toggle
        super().__init__(*args, **kwargs)
        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)
        self.configure(
            validate="all",
            validatecommand=(vcmd, "%P", "%s", "%S", "%V", "%i", "%d"),
            invalidcommand=(invcmd, "%P", "%s", "%S", "%V", "%i", "%d"),
        )

    def _toggle_error(self, on=False):
        self.configure(foreground="red" if on else "black")
        if self.on_error_toggle:
            self.on_error_toggle(on)

    def _validate(self, proposed, current, char, event, index, action):
        self.error.set("")
        self._toggle_error(False)
        state = str(self.configure("state")[-1])
        if state == tk.DISABLED:
            return True
        if event == "focusout":
            return self._focusout_validate(event=event)
        elif event == "key":
            return self._key_validate(proposed=proposed, current=current, char=char, event=event, index=index, action=action)
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        if event == "focusout":
            self._focusout_invalid(event=event)
        elif event == "key":
            self._key_invalid(proposed=proposed, current=current, char=char, event=event, index=index, action=action)

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, **kwargs):
        return True

    def _focusout_invalid(self, **kwargs):
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        self._toggle_error(True)

    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event="focusout")
        return valid

class RequiredEntry(ValidateMixin, ttk.Entry):
    def _focusout_validate(self, event, **kwargs):
        if not self.get().strip():
            self.error.set("A valid entry is required")
            return False
        return True

class DateEntry(ValidateMixin, ttk.Entry):
    def _key_validate(self, action, index, char, **kwargs):
        try:
            idx = int(index)
        except ValueError:
            return False
        if action == "0":
            return True
        if idx in (0, 1, 2, 3, 5, 6, 8, 9):
            return char.isdigit()
        elif idx in (4, 7):
            return char == '-'
        return False

    def _focusout_validate(self, **kwargs):
        val = self.get().strip()
        if not val:
            self.error.set("A date value is required")
            return False
        try:
            datetime.strptime(val, "%Y-%m-%d")
        except ValueError:
            self.error.set("Use YYYY-MM-DD format")
            return False
        return True

class ValidateComboBox(ValidateMixin, ttk.Combobox):
    def _key_validate(self, proposed, action, **kwargs):
        if action == "0":
            self.set('')
            return True
        values = self.cget('values')
        matching = [x for x in values if x.lower().startswith(proposed.lower())]
        if len(matching) == 0:
            return False
        elif len(matching) == 1:
            self.set(matching[0])
            self.icursor(tk.END)
            return False
        return True

    def _focusout_validate(self, **kwargs):
        if not self.get().strip():
            self.error.set("Selecting a value is required")
            return False
        return True

if ValidatedCombobox is None:
    ValidatedCombobox = ValidateComboBox

class ValidateSpinbox(ValidateMixin, ttk.Spinbox):
    def __init__(self, *args, min_var=None, max_var=None, focus_update_var=None, from_='-Infinity', to='Infinity', **kwargs):
        super().__init__(*args, from_=from_, to=to, **kwargs)
        increment = Decimal(str(kwargs.get('increment', '1')))
        self.precision = abs(increment.normalize().as_tuple().exponent)
        self.variable = kwargs.get('textvariable')
        if not self.variable:
            self.variable = tk.DoubleVar()
            self.configure(textvariable=self.variable)
        if min_var:
            self.min_var = min_var
            self.min_var.trace_add('write', self._set_minimum)
        if max_var:
            self.max_var = max_var
            self.max_var.trace_add('write', self._set_maximum)
        self.focus_update_var = focus_update_var
        self.bind('<FocusOut>', self._set_focus_update_var)

    def _set_focus_update_var(self, event):
        value = self.get()
        if self.focus_update_var and not self.error.get():
            self.focus_update_var.set(value)

    def _set_minimum(self, *_):
        current = self.get()
        try:
            new_min = self.min_var.get()
            self.config(from_=new_min)
        except (tk.TclError, ValueError):
            pass
        if not current:
            self.delete(0, tk.END)
        else:
            self.variable.set(current)
        self.trigger_focusout_validation()

    def _set_maximum(self, *_):
        current = self.get()
        try:
            new_max = self.max_var.get()
            self.config(to=new_max)
        except (tk.TclError, ValueError):
            pass
        if not current:
            self.delete(0, tk.END)
        else:
            self.variable.set(current)
        self.trigger_focusout_validation()

    def _key_validate(self, char, index, current, proposed, action, **kwargs):
        if action == "0":
            return True
        try:
            min_val = Decimal(str(self.cget('from')))
        except (InvalidOperation, ValueError):
            min_val = Decimal('-Infinity')
        try:
            max_val = Decimal(str(self.cget('to')))
        except (InvalidOperation, ValueError):
            max_val = Decimal('Infinity')
        no_negative = min_val >= 0
        no_decimal = self.precision <= 0
        if any([(char not in '-1234567890.'), (char == '-' and (no_negative or index != '0')), (char == '.' and (no_decimal or '.' in current))]):
            return False
        if proposed in ('-', '.', '-.'):
            return True
        try:
            proposed_dec = Decimal(proposed)
        except InvalidOperation:
            return False
        proposed_precision = abs(proposed_dec.normalize().as_tuple().exponent)
        if proposed_dec > max_val or proposed_precision > self.precision:
            return False
        return True

    def _focusout_validate(self, **kwargs):
        value = self.get()
        try:
            min_val = Decimal(str(self.cget('from')))
            max_val = Decimal(str(self.cget('to')))
        except (InvalidOperation, ValueError):
            return True
        try:
            d_value = Decimal(value)
        except InvalidOperation:
            self.error.set(f"Invalid number: {value}")
            return False
        if d_value < min_val:
            self.error.set(f'Min allowed is {min_val}')
            return False
        if d_value > max_val:
            self.error.set(f'Max allowed is {max_val}')
            return False
        return True

class ValidatedRadioGroup(ttk.Frame):
    def __init__(self, *args, variable=None, error_var=None, values=None, button_args=None, on_error_toggle=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.variable = variable or tk.StringVar()
        self.error = error_var or tk.StringVar()
        self.values = values or list()
        self.button_args = button_args or dict()
        self.on_error_toggle = on_error_toggle
        for v in self.values:
            button = ttk.Radiobutton(self, value=v, text=v, variable=self.variable, **self.button_args)
            button.pack(side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x')
        self.bind('<FocusOut>', self.trigger_focusout_validation)

    def trigger_focusout_validation(self, *_):
        self.error.set("")
        if not self.variable.get():
            self.error.set("A selection is required")
            if self.on_error_toggle:
                self.on_error_toggle(True)
            return False
        if self.on_error_toggle:
            self.on_error_toggle(False)
        return True

class LabelInput(tk.Frame):
    def __init__(self, parent, label, var, input_class=ttk.Entry, input_args=None, label_args=None, disable_var=None, **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = var
        self.error_var = tk.StringVar()
        self.label_style = "NormalLabel.TLabel"
        self.error_label_style = "ErrorLabel.TLabel"
        if input_class in (ttk.Checkbutton, tk.Button):
            input_args["text"] = label
            self.label = None
        else:
            self.label = ttk.Label(self, text=label, style=self.label_style, **label_args)
            self.label.grid(row=0, column=0, sticky="w")
        if input_class in (ttk.Checkbutton, tk.Button, ttk.Radiobutton, ValidatedRadioGroup):
            input_args["variable"] = self.variable
        else:
            input_args["textvariable"] = self.variable
        if issubclass(input_class, (ValidateMixin, ValidatedRadioGroup)):
            input_args["error_var"] = self.error_var
            input_args["on_error_toggle"] = self._toggle_label_color
        if input_class == ttk.Radiobutton:
            self.input = tk.Frame(self)
            values = input_args.pop("values", [])
            for value in values:
                button = ttk.Radiobutton(self.input, text=value, value=value, **input_args)
                button.pack(side=tk.LEFT, padx=5)
        else:
            self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky="ew")
        self.error_message_label = ttk.Label(self, textvariable=self.error_var, foreground="red", font=("TkDefaultFont", 8))
        self.error_message_label.grid(row=2, column=0, sticky="w")
        self.columnconfigure(0, weight=1)
        if disable_var:
            self.disable_var = disable_var
            self.disable_var.trace_add("write", self._check_disable)
        self.error = getattr(self.input, "error", tk.StringVar())
        ttk.Label(self, textvariable=self.error, foreground="red", **label_args).grid(row=2, column=0, sticky="ew")

    def _check_disable(self, *_):
        if not hasattr(self, "disable_var"):
            return
        if self.disable_var.get():
            self.input.configure(state=tk.DISABLED)
            self.variable.set("")
            self.error.set("")
        else:
            self.input.configure(state=tk.NORMAL)

    def _toggle_label_color(self, is_error):
        if self.label:
            if is_error:
                self.label.configure(foreground="red")
            else:
                self.label.configure(foreground="black")

    def grid(self, sticky="ew", **kwargs):
        super().grid(sticky=sticky, **kwargs)

class DataRecordForm(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.inputs = {}
        self._vars = {
            "Date": tk.StringVar(),
            "Time": tk.StringVar(),
            "Technician": tk.StringVar(),
            "Lab": tk.StringVar(),
            "Plot": tk.StringVar(),
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
        record_info = self._add_frame("Record Info")
        self._add_input("Date", record_info, 0, 0, input_class=DateEntry)
        self._add_input("Time", record_info, 0, 1, input_class=ValidateComboBox, input_args={"values": ["8:00", "12:00", "16:00", "20:00"], "state": "readonly"})
        self._add_input("Technician", record_info, 0, 2, input_class=RequiredEntry)
        self._add_input("Lab", record_info, 1, 0, input_class=ValidateComboBox, input_args={"values": ["A", "B", "C"], "state": "readonly"})
        self._add_input("Plot", record_info, 1, 1, input_class=ValidatedCombobox, input_args={"values": [str(i) for i in range(1, 21)], "state": "readonly"})
        self._add_input("Seed Sample", record_info, 1, 2, input_class=RequiredEntry)
        environment_info = self._add_frame("Environment Data")
        self._add_input("Humidity", environment_info, 0, 0, input_class=ValidateSpinbox, input_args={"from_": 0.5, "to": 52.0, "increment": 0.01}, disable_var=self._vars['Equipment Fault'])
        self._add_input("Light", environment_info, 0, 1, input_class=ValidateSpinbox, input_args={"from_": 0.0, "to": 100.0, "increment": 0.01}, disable_var=self._vars['Equipment Fault'])
        self._add_input("Temperature", environment_info, 0, 2, input_class=ValidateSpinbox, input_args={"from_": 4.0, "to": 40.0, "increment": 0.01}, disable_var=self._vars['Equipment Fault'])
        self._add_input("Equipment Fault", environment_info, 1, 0, input_class=ttk.Checkbutton)
        plant_info = self._add_frame("Plant Data")
        self._add_input("Plants", plant_info, 0, 0, input_class=ValidateSpinbox, input_args={"from_": 0, "to": 20, "increment": 1})
        self._add_input("Blossoms", plant_info, 0, 1, input_class=ValidateSpinbox, input_args={"from_": 0, "to": 1000, "increment": 1})
        self._add_input("Fruit", plant_info, 0, 2, input_class=ValidateSpinbox, input_args={"from_": 0, "to": 1000, "increment": 1})
        min_height_var = tk.DoubleVar(value='-infinity')
        max_height_var = tk.DoubleVar(value='infinity')
        self._add_input("Min Height", plant_info, 1, 0, input_class=ValidateSpinbox, input_args={"from_": 0, "to": 1000, "increment": 0.01 , "max_var": max_height_var , "focus_update_var":min_height_var})
        self._add_input("Max Height", plant_info, 1, 1, input_class=ValidateSpinbox, input_args={"from_": 0, "to": 1000, "increment": 0.01 , "min_var": min_height_var , "focus_update_var":max_height_var})
        self._add_input("Median Height", plant_info, 1, 2, input_class=ValidateSpinbox, input_args={"from_": 0, "to": 1000, "increment": 0.01 , "min_var": min_height_var , "max_var":max_height_var})
        self._add_input("Notes", self, 3, 0, input_class=BoundText, input_args={"width": 75, "height": 10})
        buttons = ttk.Frame(self)
        buttons.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
        self.save_button = ttk.Button(buttons, text="Save", command=self.master._on_save)
        self.save_button.pack(side=tk.RIGHT)

    def _add_input(self, key, parent, row, column, **kwargs):
        widget = LabelInput(parent, key, var=self._vars[key], **kwargs)
        widget.grid(row=row, column=column, padx=5, pady=5)
        self.inputs[key] = widget
        return widget

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
        for child in self.winfo_children():
            self._reset_labels_recursive(child)
        current_date = datetime.today().strftime("%Y-%m-%d")
        self._vars["Date"].set(current_date)
        self.inputs["Date"].input.focus_set()

    def _reset_labels_recursive(self, widget):
        if isinstance(widget, LabelInput):
            widget._toggle_label_color(False)
            widget.error_var.set("")
        for w in widget.winfo_children():
            self._reset_labels_recursive(w)

    def validate_all(self):
        is_valid = True
        for child in self.winfo_children():
            is_valid = self._validate_recursive(child) and is_valid
        return is_valid

    def _validate_recursive(self, widget):
        valid = True
        if hasattr(widget, "trigger_focusout_validation"):
            valid = widget.trigger_focusout_validation() and valid
        for w in widget.winfo_children():
            valid = self._validate_recursive(w) and valid
        return valid

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

    def get_errors(self):
        errors = {}
        for key, label_input in self.inputs.items():
            input_widget = label_input.input
            if hasattr(input_widget, "trigger_focusout_validation"):
                input_widget.trigger_focusout_validation()
            if label_input.error_var.get():
                errors[key] = label_input.error_var.get()
        return errors

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Saba Data Entry Application")
        self.columnconfigure(0, weight=1)
        style = ttk.Style(self)
        style.configure("NormalLabel.TLabel", foreground="black")
        ttk.Label(self, text="Saba Data Entry Application", font=("TkDefaultFont", 16)).grid(row=0, column=0, padx=10, pady=10)
        self.record_form = DataRecordForm(self)
        self.record_form.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.status).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self._records_saved = 0

    def _on_save(self):
        errors = self.record_form.get_errors()
        if errors:
            self.status.set("Cannot save,error in fields :{}".format(','.join(errors.keys())))
            return
        if not self.record_form.validate_all():
            self.status.set("Please fix the errors shown in red above.")
            return
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
