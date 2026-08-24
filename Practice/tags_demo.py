import tkinter as tk


root = tk.Tk()
root.title("Simple Python Terminal")

text = tk.Text(
    root,
    height=20,
    width=50,
    bg="black",
    fg="lightgreen",
    insertbackground="white"
)
text.pack(padx=10, pady=10)

text.tag_configure(
    "prompt",
    foreground="magenta"
)

text.tag_configure(
    "output",
    foreground="yellow"
)

text.insert("end", ">>> ", ("prompt",))


def on_return(event=None):
    command = text.get(
        "prompt.last",
        "end-1c"
    ).replace(">>> ", "", 1).strip()

    if command:
        try:
            output = str(eval(command))
        except Exception as error:
            output = str(error)

        text.insert(
            "end",
            f"\n{output}",
            ("output",)
        )

    text.insert(
        "end",
        "\n>>> ",
        ("prompt",)
    )

    text.see("end")

    return "break"


text.bind(
    "<Return>",
    on_return
)

text.focus_set()

root.mainloop()
