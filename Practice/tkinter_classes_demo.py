import tkinter as tk
import json


class FormFrame(tk.Frame):
    def __init__(self, parent, on_submit, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.on_submit = on_submit

        self.name_var = tk.StringVar()
        self.age_var = tk.IntVar(value=21)

        # Name
        tk.Label(self, text="Name").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Age
        tk.Label(self, text="Age").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Spinbox(self, from_=10, to=150, textvariable=self.age_var).grid(
            row=1, column=1, padx=10, pady=5, sticky="ew"
        )

        # Button
        tk.Button(self, text="Submit", command=self.submit).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        self.columnconfigure(1, weight=1)

    def submit(self):
        data = {
            "name": self.name_var.get(),
            "age": self.age_var.get()
        }


        json_text = json.dumps(data)

        self.on_submit(data, json_text)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Form Demo")

        tk.Label(self, text="Please fill the form").grid(
            row=0, column=0, padx=10, pady=10, sticky="ew"
        )

        self.form = FormFrame(self, self.show_result)
        self.form.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.result_label = tk.Label(self, text="", justify="left")
        self.result_label.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.json_label = tk.Label(self, text="", fg="blue", justify="left")
        self.json_label.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def show_result(self, data, json_text):

        self.result_label.config(
            text=f"Name = {data['name']}\nAge = {data['age']}"
        )


        self.json_label.config(text=json_text)


if __name__ == "__main__":
    app = Application()
    app.mainloop()


