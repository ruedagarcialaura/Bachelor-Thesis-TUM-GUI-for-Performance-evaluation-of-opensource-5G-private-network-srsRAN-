import tkinter as tk
from tkinter import ttk

class Results_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.results_view_label = tk.Label(self.frame, text= "Welcome to the Results view")
        self.results_view_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Combobox para Packet Size
        self.packet_size_label = tk.Label(self.frame, text="Packet Size")
        self.packet_size_label.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.packet_size_combobox = ttk.Combobox(self.frame, values=["256", "1000"])
        self.packet_size_combobox.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        # Combobox para Direction
        self.direction_label = tk.Label(self.frame, text="Direction")
        self.direction_label.grid(row=1, column=2, padx=20, pady=20, sticky="ew")
        self.direction_combobox = ttk.Combobox(self.frame, values=["Uplink", "Downlink"])
        self.direction_combobox.grid(row=1, column=3, padx=20, pady=20, sticky="ew")

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()