import tkinter as tk


root = tk.Tk()
root.title("Banana Interest Survey")
root.geometry("640x480+300+300")
root.resizable(False, False)

root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)
root.rowconfigure(9, weight=1)

title = tk.Label(
    root,
    text="Please take the survey",
    font=("Arial", 16, "bold"),
    bg="brown",
    fg="#FF0",
)
title.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 15))

name_var = tk.StringVar()
name_label = tk.Label(root, text="What is your name?")
name_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

name_inp = tk.Entry(root, textvariable=name_var)
name_inp.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

eats_bananas_var = tk.BooleanVar(value=False)
eater_inp = tk.Checkbutton(
    root,
    text="Check this box if you eat bananas",
    variable=eats_bananas_var,
)
eater_inp.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

num_label = tk.Label(root, text="How many bananas do you eat per day?")
num_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

num_var = tk.IntVar(value=3)
num_inp = tk.Spinbox(root, textvariable=num_var, from_=0, to=1000, increment=1)
num_inp.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

color_var = tk.StringVar(value="Any")
color_label = tk.Label(root, text="What is the best color for a banana?")
color_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

color_choices = ("Any", "Green", "Green-Yellow", "Yellow", "Brown Spotted", "Black")
color_inp = tk.OptionMenu(root, color_var, *color_choices)
color_inp.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

plantain_label = tk.Label(root, text="Do you eat plantains?")
plantain_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

plantain_var = tk.BooleanVar(value=False)
plantain_frame = tk.Frame(root)
plantain_frame.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=5)

plantain_yes_inp = tk.Radiobutton(
    plantain_frame,
    text="Yes",
    variable=plantain_var,
    value=True,
)
plantain_yes_inp.pack(side="left", padx=(0, 10))

plantain_no_inp = tk.Radiobutton(
    plantain_frame,
    text="No",
    variable=plantain_var,
    value=False,
)
plantain_no_inp.pack(side="left")

banana_haiku_label = tk.Label(root, text="Write a haiku about bananas")
banana_haiku_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

banana_haiku_inp = tk.Text(root, height=4)
banana_haiku_inp.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

output_var = tk.StringVar(value="")
output_line = tk.Label(root, textvariable=output_var, anchor="w", justify="left")
output_line.grid(row=11, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))


def on_submit():
    name = name_var.get().strip() or "friend"

    try:
        number = num_var.get()
    except tk.TclError:
        number = 0

    eats_bananas = eats_bananas_var.get()
    plantains = "Yes" if plantain_var.get() else "No"
    color = color_var.get()

    haiku = banana_haiku_inp.get("1.0", tk.END).strip()

    if eats_bananas:
        message = (
            f"Thanks for taking the survey, {name}.\n"
            f"Enjoy your {number} {color} bananas!\n"
            f"Plantains: {plantains}"
        )
    else:
        message = (
            f"Thanks for taking the survey, {name}.\n"
            f"You do not eat bananas.\n"
            f"Plantains: {plantains}"
        )

    output_var.set(message)

    if haiku:
        print("Banana haiku:")
        print(haiku)


submit_btn = tk.Button(root, text="Submit Survey", command=on_submit)
submit_btn.grid(row=10, column=0, columnspan=2, pady=10)

root.mainloop()
