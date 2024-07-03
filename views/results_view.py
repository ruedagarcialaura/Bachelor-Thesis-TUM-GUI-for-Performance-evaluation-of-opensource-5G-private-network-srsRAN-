import tkinter as tk

class Results_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.results_view_label = tk.Label(self.frame, text= "Welcome to the Results view")
        self.results_view_label.grid()

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()