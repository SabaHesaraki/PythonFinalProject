import tkinter as tk
from tkinter import ttk
from pathlib import Path

root = tk.Tk()

paths = sorted(Path('.').glob('**/*'), key=lambda p: len(p.parts))

status = tk.StringVar()
tk.Label(root, textvariable=status).pack(side=tk.BOTTOM)

def show_directory_status(*_):
    item_id = tv.focus()

    if not item_id:
        return
    clicked_path = Path(item_id)
    if clicked_path.is_dir():
        try:
            num_children = len(list(clicked_path.iterdir()))
            status.set(f"Directory: {clicked_path.name}, {num_children} children")
        except PermissionError:
            status.set(f"Directory: {clicked_path.name} (Access Denied)")


def sort(tv, col, parent='', reverse=False):
    sort_index = list()
    for iid in tv.get_children(parent):
        sort_value = tv.set(iid, col) if col != '#0' else tv.item(iid, 'text')
        sort_index.append((sort_value, iid))

    sort_index.sort(reverse=reverse)

    for index, (_, iid) in enumerate(sort_index):
        tv.move(iid, parent, index)
        sort(tv, col, parent=iid, reverse=reverse)

    if parent == '':
        tv.heading(col, command=lambda: sort(tv, col, reverse=not reverse))


tv = ttk.Treeview(root, columns=['size', 'modified'], selectmode='browse')
tv.heading("#0", text="Name", command=lambda: sort(tv, '#0'))
tv.heading("size", text="Size", anchor="center", command=lambda: sort(tv, 'size'))
tv.heading("modified", text="Modified", anchor="e", command=lambda: sort(tv, 'modified'))

tv.column("#0", stretch=True)
tv.column("size", width=200)
tv.pack(fill="both", expand=True)

for path in paths:
    meta = path.stat()
    parent = str(path.parent)
    if parent == '.':
        parent = ''
    tv.insert(
        parent,
        'end',
        iid=str(path),
        text=str(path.name),
        values=[meta.st_size, meta.st_mtime]
    )

tv.bind('<<TreeviewOpen>>', show_directory_status)
tv.bind('<<TreeviewClose>>', lambda _: status.set(""))

root.mainloop()
