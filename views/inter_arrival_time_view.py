import tkinter as tk
import subprocess

class Inter_arrival_time_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.inter_arrival_time_view_label = tk.Label(self.frame, text= "Welcome to the Inter Arrival Time view")
        self.inter_arrival_time_view_label.grid()

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()