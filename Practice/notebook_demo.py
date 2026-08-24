import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tkinter Notebook")
root.geometry("600x400")

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=20, pady=20)

banana_facts = [
    "Banana trees are of the genus Musa.",
    "Bananas are technically berries.",
    "All bananas contain small amounts of radioactive potassium.",
    "Bananas are used in paper and textile manufacturing."
]


plantain_facts = [
    "Plantains are also of genus Musa.",
    "Plantains are starchier and less sweet than bananas.",
    'Plantains are called "Cooking Bananas" since they are rarely eaten raw.'
]


b_label = ttk.Label(
    notebook,
    text="\n\n" + "\n".join(banana_facts),
    padding=20
)

p_label = ttk.Label(
    notebook,
    text="\n\n" + "\n".join(plantain_facts),
    padding=20
)

notebook.add(
    b_label,
    text="Bananas",
    padding=20,
    underline=0
)

notebook.add(
    p_label,
    text="Plantains",
    padding=20,
    underline=0
)

notebook.enable_traversal()

notebook.select(0)

root.mainloop()
