import tkinter as tk
from tkinter import ttk
from datetime import datetime
from decimal import Decimal, InvalidOperation

from .constants import FiledTypes as FT


class ValidatedMixin:
    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var or tk.StringVar()

        super().__init__(*args, **kwargs)

        validate_command = self.register(self._validate)
        invalid_command = self.register(self._invalid)

        self.configure(
            validate="all",
            validatecommand=(
                validate_command,
                "%P",
                "%s",
                "%S",
                "%V",
                "%i",
                "%d"
            ),
            invalidcommand=(
                invalid_command,
                "%P",
                "%s",
                "%S",
                "%V",
                "%i",
                "%d"
            )
        )

    def _toggle_error(self, enabled=False):
        try:
            self.configure(
                foreground="red" if enabled else "black"
            )
        except tk.TclError:
            pass

    def _validate(
        self,
        proposed,
        current,
        char,
        event,
        index,
        action
    ):
        self._toggle_error(False)
        self.error.set("")

        if event == "focusout":
            return self._focusout_validate(
                event=event
            )

        if event == "key":
            return self._key_validate(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )

        return True

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, **kwargs):
        return True

    def _invalid(
        self,
        proposed,
        current,
        char,
        event,
        index,
        action
    ):
        if event == "focusout":
            self._focusout_invalid(
                event=event
            )

        elif event == "key":
            self._key_invalid(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )

    def _focusout_invalid(self, **kwargs):
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        self._toggle_error(True)

    def trigger_focusout_validation(self):
        valid = self._validate(
            "",
            "",
            "",
            "focusout",
            "",
            ""
        )

        if not valid:
            self._focusout_invalid(
                event="focusout"
            )

        return valid


class DateEntry(ValidatedMixin, ttk.Entry):
    def _key_validate(self, action, index, char, **kwargs):
        if action == "0":
            return True

        if index in ("0", "1", "2", "3", "5", "6", "8", "9"):
            return char.isdigit()

        if index in ("4", "7"):
            return char == "-"

        return False

    def _focusout_validate(self, **kwargs):
        value = self.get()

        if not value:
            self.error.set("A value is required")
            return False

        try:
            datetime.strptime(
                value,
                "%Y-%m-%d"
            )
        except ValueError:
            self.error.set("Invalid date")
            return False

        return True


class RequiredEntry(ValidatedMixin, ttk.Entry):
    def _focusout_validate(self, **kwargs):
        if not self.get().strip():
            self.error.set("A value is required")
            return False

        return True


class ValidatedCombobox(ValidatedMixin, ttk.Combobox):
    def _key_validate(self, proposed, action, **kwargs):
        if action == "0":
            self.set("")
            return True

        values = self.cget("values")

        matches = [
            value
            for value in values
            if value.lower().startswith(
                proposed.lower()
            )
        ]

        if not matches:
            return False

        if len(matches) == 1:
            self.set(matches[0])
            self.icursor(tk.END)
            return False

        return True

    def _focusout_validate(self, **kwargs):
        if not self.get().strip():
            self.error.set("A value is required")
            return False

        return True


class ValidatedSpinbox(ValidatedMixin, tk.Spinbox):
    def __init__(
        self,
        *args,
        min_var=None,
        max_var=None,
        focus_update_var=None,
        from_="-Infinity",
        to="Infinity",
        **kwargs
    ):
        increment = kwargs.get("increment", "1.0")

        super().__init__(
            *args,
            from_=from_,
            to=to,
            **kwargs
        )

        self.resolution = Decimal(
            str(increment)
        )

        self.precision = (
            self.resolution
            .normalize()
            .as_tuple()
            .exponent
        )

        self.variable = (
            kwargs.get("textvariable")
            or tk.DoubleVar()
        )

        self.min_var = min_var
        self.max_var = max_var
        self.focus_update_var = focus_update_var

        if self.min_var is not None:
            self.min_var.trace_add(
                "write",
                self._set_minimum
            )

        if self.max_var is not None:
            self.max_var.trace_add(
                "write",
                self._set_maximum
            )

        self.bind(
            "<FocusOut>",
            self._set_focus_update_var
        )

    def _set_focus_update_var(self, event=None):
        value = self.get()

        if (
            self.focus_update_var is not None
            and value
            and not self.error.get()
        ):
            try:
                self.focus_update_var.set(value)
            except tk.TclError:
                pass

    def _set_minimum(self, *args):
        current = self.get()

        try:
            minimum = self.min_var.get()
            self.configure(from_=minimum)
        except (tk.TclError, ValueError):
            pass

        if not current:
            self.delete(0, tk.END)
        else:
            self.variable.set(current)

        self.trigger_focusout_validation()

    def _set_maximum(self, *args):
        current = self.get()

        try:
            maximum = self.max_var.get()
            self.configure(to=maximum)
        except (tk.TclError, ValueError):
            pass

        if not current:
            self.delete(0, tk.END)
        else:
            self.variable.set(current)

        self.trigger_focusout_validation()

    def _key_validate(
        self,
        char,
        index,
        current,
        proposed,
        action,
        **kwargs
    ):
        if action == "0":
            return True

        minimum = Decimal(
            str(self.cget("from"))
        )
        maximum = Decimal(
            str(self.cget("to"))
        )

        no_negative = minimum >= 0
        no_decimal = self.precision >= 0

        if char not in "-1234567890.":
            return False

        if char == "-" and (
            no_negative or index != "0"
        ):
            return False

        if char == "." and (
            no_decimal or "." in current
        ):
            return False

        if proposed in ("-", "."):
            return True

        try:
            proposed_value = Decimal(proposed)
        except InvalidOperation:
            return False

        precision = (
            proposed_value
            .as_tuple()
            .exponent
        )

        if proposed_value > maximum:
            return False

        if precision < self.precision:
            return False

        return True

    def _focusout_validate(self, **kwargs):
        value = self.get()

        if not value:
            self.error.set("A value is required")
            return False

        minimum = Decimal(
            str(self.cget("from"))
        )
        maximum = Decimal(
            str(self.cget("to"))
        )

        try:
            numeric_value = Decimal(value)
        except InvalidOperation:
            self.error.set(
                f"Invalid number string: {value}"
            )
            return False

        if numeric_value < minimum:
            self.error.set(
                f"Value is too low (min {minimum})"
            )
            return False

        if numeric_value > maximum:
            self.error.set(
                f"Value is too high (max {maximum})"
            )
            return False

        return True


class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    field_types = {
        FT.string: (
            RequiredEntry,
            tk.StringVar
        ),
        FT.string_list: (
            ValidatedCombobox,
            tk.StringVar
        ),
        FT.iso_date_string: (
            DateEntry,
            tk.StringVar
        ),
        FT.long_string: (
            tk.Text,
            lambda: None
        ),
        FT.decimal: (
            ValidatedSpinbox,
            tk.DoubleVar
        ),
        FT.integer: (
            ValidatedSpinbox,
            tk.IntVar
        ),
        FT.boolean: (
            ttk.Checkbutton,
            tk.BooleanVar
        )
    }

    def __init__(
        self,
        parent,
        label="",
        input_class=None,
        input_var=None,
        input_args=None,
        label_args=None,
        field_spec=None,
        var=None,
        **kwargs
    ):
        if input_var is None and var is not None:
            input_var = var

        super().__init__(
            parent,
            **kwargs
        )

        input_args = dict(
            input_args or {}
        )
        label_args = dict(
            label_args or {}
        )

        if field_spec:
            field_type = field_spec.get(
                "type",
                FT.string
            )

            default_class, variable_type = (
                self.field_types[field_type]
            )

            input_class = (
                input_class
                or default_class
            )

            self.variable = (
                input_var
                if input_var is not None
                else variable_type()
            )

            if (
                "min" in field_spec
                and "from_" not in input_args
            ):
                input_args["from_"] = field_spec["min"]

            if (
                "max" in field_spec
                and "to" not in input_args
            ):
                input_args["to"] = field_spec["max"]

            if (
                "inc" in field_spec
                and "increment" not in input_args
            ):
                input_args["increment"] = field_spec["inc"]

            if (
                "values" in field_spec
                and "values" not in input_args
            ):
                input_args["values"] = field_spec["values"]

        else:
            self.variable = input_var

        if input_class in (
            ttk.Checkbutton,
            ttk.Button,
            ttk.Radiobutton
        ):
            input_args["text"] = label
            input_args["variable"] = self.variable

        else:
            self.label = ttk.Label(
                self,
                text=label,
                **label_args
            )

            self.label.grid(
                row=0,
                column=0,
                sticky="ew"
            )

            if self.variable is not None:
                input_args["textvariable"] = self.variable

        self.input = input_class(
            self,
            **input_args
        )

        self.input.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.columnconfigure(
            0,
            weight=1
        )

        self.error = getattr(
            self.input,
            "error",
            tk.StringVar()
        )

        error_style = ttk.Style(self)
        error_style.configure(
            "Error.TLabel",
            foreground="red"
        )

        self.error_label = ttk.Label(
            self,
            textvariable=self.error,
            style="Error.TLabel"
        )

        self.error_label.grid(
            row=2,
            column=0,
            sticky="ew"
        )

    def grid(self, sticky="ew", **kwargs):
        super().grid(
            sticky=sticky,
            **kwargs
        )

    def get(self):
        try:
            if self.variable is not None:
                return self.variable.get()

            if isinstance(self.input, tk.Text):
                return self.input.get(
                    "1.0",
                    tk.END
                ).strip()

            return self.input.get()

        except (
            TypeError,
            tk.TclError
        ):
            return ""

    def set(self, value, *args, **kwargs):
        if isinstance(self.variable, tk.BooleanVar):
            self.variable.set(
                bool(value)
            )

        elif self.variable is not None:
            self.variable.set(
                value,
                *args,
                **kwargs
            )

        elif isinstance(
            self.input,
            (
                ttk.Checkbutton,
                ttk.Radiobutton
            )
        ):
            if value:
                self.input.select()
            else:
                self.input.deselect()

        elif isinstance(self.input, tk.Text):
            self.input.delete(
                "1.0",
                tk.END
            )
            self.input.insert(
                "1.0",
                value
            )

        else:
            self.input.delete(
                0,
                tk.END
            )
            self.input.insert(
                0,
                value
            )
