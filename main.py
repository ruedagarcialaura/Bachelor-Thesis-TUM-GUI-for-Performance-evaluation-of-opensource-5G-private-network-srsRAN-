import tkinter as tk
#from tkinter import font as tkFont
#from tkinter import ttk

# Import the views
from views.home_view import Home_view
from views.latency_view import Latency_view
from views.throughput_view import Throughput_view
from views.iperf3_view import Iperf3_view
from views.inter_arrival_time_view import Inter_arrival_time_view
#from views.wireshark_capture import Wireshark_capture
from views.graph import Wireshark_capture
from views.packet_loss_view import Packet_loss_view


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
        self.button1 = tk.Button(self.frame, text="Connect to the network", command=self.show_home_view) # font=customFont, bg=buttonColor, fg=textColor)
        self.button1.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        #self.button2 = tk.Button(self.frame, text="capture Traffic", command=self.show_wireshark_capture)
        #self.button2.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.button3 = tk.Button(self.frame, text="Latency", command=self.show_latency_view)
        self.button3.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
        self.button4 = tk.Button(self.frame, text="Inter Arrival Time", command=self.show_inter_arrival_time_view)
        self.button4.grid(row=0, column=3, padx=0, pady=0, sticky="nsew")
        self.button5 = tk.Button(self.frame, text="Capture  traffic", command=self.show_iperf3_view)
        self.button5.grid(row=0, column=4, padx=0, pady=0, sticky="nsew")
        self.button6 = tk.Button(self.frame, text="Throughput", command=self.show_throughput_view)
        self.button6.grid(row=0, column=5, padx=0, pady=0, sticky="nsew")
        self.button7 = tk.Button(self.frame, text="Packet Loss", command=self.show_packet_loss_view)
        self.button7.grid(row=0, column=6, padx=0, pady=0, sticky="nsew")
        
        
        
        # Create the views
        self.home_view = Home_view(self.root)
        self.latency_view = Latency_view(self.root)
        self.throughput_view = Throughput_view(self.root)
        self.iperf3_view = Iperf3_view(self.root)
        self.inter_arrival_time_view = Inter_arrival_time_view(self.root)
        self.wireshark_capture = Wireshark_capture(self.root)
        self.packet_loss_view = Packet_loss_view(self.root)
        
        #Show the main view at startup
        self.show_home_view()
        

    #Methods to show each view
    def show_home_view(self):
        self.hide_all_views()
        self.home_view.show()

    def show_latency_view(self):
        self.hide_all_views()
        self.latency_view.show()

    def show_throughput_view(self):
        self.hide_all_views()
        self.throughput_view.show()

    def show_iperf3_view(self):
        self.hide_all_views()
        self.iperf3_view.show()

    def show_inter_arrival_time_view(self):
        self.hide_all_views()
        self.inter_arrival_time_view.show()   

    def show_wireshark_capture(self):
        self.hide_all_views()
        self.wireshark_capture.show()

    def show_packet_loss_view(self):
        self.hide_all_views()
        self.packet_loss_view.show()

    def hide_all_views(self):
        self.latency_view.hide()
        self.throughput_view.hide()
        self.iperf3_view.hide()
        self.inter_arrival_time_view.hide()
        self.home_view.hide()
        self.wireshark_capture.hide()
        self.packet_loss_view.hide()

    
   

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()