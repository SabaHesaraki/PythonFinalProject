from tkinter import ttk
import tkinter as tk

class FiveCharEntry(ttk.Entry):

    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.error=tk.StringVar()
        self.configure(validate="all",validatecommand=(self.register(self._validate),'%P'),
                       invalidcommand=(self.register(self._on_invalid),'%P')
        )

    def _validate(self,proposed):
        return len(proposed) <=5


    def _on_invalid(self,proposed):
        self.error.set(f'{proposed} is too long , only 5 characters allowed' )

if __name__=='__main__':
    root=tk.Tk()
    entry=FiveCharEntry(root)
    error_label=ttk.Label(root,textvariable=entry.error,foreground='red')
    entry.grid()
    error_label.grid()
    root.mainloop()