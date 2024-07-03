import tkinter as tk
#from tkinter import font as tkFont
#from tkinter import ttk

# Import the views
from views.GUI_view import GUI_view
from views.home_view import Home_view
from views.iperf3_view import Iperf3_view
from views.latency_view import Latency_view
from views.results_view import Results_view
from views.packet_loss_view import Packet_loss_view

from views.graph import Wireshark_capture


class GUI:
    #Constructor: define la estructura básica de la GUI, con un frame(marco principal) y botones para cambiar de vista
    def __init__(self, root):
        self.root = root
        self.root.columnconfigure(0, weight=1)  # Hace que la columna central se expanda
        self.root.rowconfigure(1, weight=1)  # Hace que la fila debajo de los botones se expanda
        self.root.title("srsRAN Measurements")
        self.root.geometry("1250x600")
                

        # Create the main frame (Marco principal)
        self.frame = tk.Frame(self.root, borderwidth=2, relief="groove", bg="lightgray")
        self.frame.grid(row=0, sticky="ew")     

        # Create buttons to switch between views
        self.button1 = tk.Button(self.frame, text="GUI", command=self.show_GUI_view)
        self.button1.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.button2 = tk.Button(self.frame, text="Connect to the network", command=self.show_home_view) # font=customFont, bg=buttonColor, fg=textColor)
        self.button2.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.button3 = tk.Button(self.frame, text="Capture  traffic", command=self.show_iperf3_view)
        self.button3.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
        self.button4 = tk.Button(self.frame, text="Calculations", command=self.show_latency_view)
        self.button4.grid(row=0, column=3, padx=0, pady=0, sticky="nsew")
        self.button5 = tk.Button(self.frame, text="Results", command=self.show_results_view)
        self.button5.grid(row=0, column=4, padx=0, pady=0, sticky="nsew")
        self.button6 = tk.Button(self.frame, text="Packet Loss", command=self.show_packet_loss_view)
        self.button6.grid(row=0, column=5, padx=0, pady=0, sticky="nsew")
        
        
        
        # Create the views
        self.home_view = Home_view(self.root)
        self.latency_view = Latency_view(self.root)
        self.GUI_view = GUI_view(self.root)
        self.iperf3_view = Iperf3_view(self.root)
        self.results_view = Results_view(self.root)
        self.packet_loss_view = Packet_loss_view(self.root)
        
        #Show the main view at startup
        self.show_GUI_view()
        

    #Methods to show each view

    
    def show_GUI_view(self):
        self.hide_all_views()
        self.GUI_view.show()

    def show_home_view(self):
        self.hide_all_views()
        self.home_view.show()
    
    def show_iperf3_view(self):
        self.hide_all_views()
        self.iperf3_view.show()

    def show_latency_view(self):
        self.hide_all_views()
        self.latency_view.show()

    def show_results_view(self):
        self.hide_all_views()
        self.results_view.show()   

    def show_packet_loss_view(self):
        self.hide_all_views()
        self.packet_loss_view.show()

    def hide_all_views(self):
        self.GUI_view.hide()
        self.home_view.hide()
        self.iperf3_view.hide()
        self.latency_view.hide()
        self.results_view.hide()
        self.packet_loss_view.hide()

    
   

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()