import tkinter as tk

class GUI_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.title_label = tk.Label(self.frame, text= "Performance Evaluation of srsRAN",font=("Helvetica", 16, "bold"), fg="blue")
        self.title_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=3)

        self.intructions_label1 = tk.Label(self.frame, text= "Using this tool you can obtain data from your 5G RAN network and analyze it")
        self.intructions_label1.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=3)

        self.intructions_label2 = tk.Label(self.frame, text= "Following the buttons on the top you can navigate through the different views.")
        self.intructions_label2.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=3)

        self.intructions_label3 = tk.Label(self.frame, text= "1st Connect to you srsRAN network by clicking on the ```Connect to the network```button")
        self.intructions_label3.grid(row=3, column=0, padx=20, pady=20, sticky="ew", columnspan=3)

        self.intructions_label4 = tk.Label(self.frame, text= " 2nd- Start wireshark on both the User Equipment and the Core Network User interfaces to capture the traffic. Generate this traffic using Iperf3: -Start the server part - Generate traffic from the client side. ONce the iperf3 test is done, stop wireshark on both sides by clicking on ```Stop Capture```.")
        self.intructions_label4.grid(row=4, column=0, padx=20, pady=20, sticky="ew", columnspan=3)
        
        self.intructions_label5 = tk.Label(self.frame, text= "3rd- Analyze the data by clicking on the ```Calculations``` button. Here you can calculate the average latency, packets loss, average throughput and the inter arrival time of your captured traffic.")
        self.intructions_label5.grid(row=5, column=0, padx=20, pady=20, sticky="ew", columnspan=3)

        self.intructions_label6 = tk.Label(self.frame, text= " 4th- Check the results by clicking on the ```Results``` button. Here you will see the data obtained plotted for a more visual approach.")
        self.intructions_label6.grid(row=6, column=0, padx=20, pady=20, sticky="ew", columnspan=3)

        self.intructions_label7 = tk.Label(self.frame, text= "Have fun and enjoy the tool!")
        self.intructions_label7.grid(row=7, column=0, padx=20, pady=20, sticky="ew", columnspan=3)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

        '''# Combobox para Packet Size
        self.packet_size_label = tk.Label(self.frame, text="Packet Size")
        self.packet_size_label.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.packet_size_combobox = ttk.Combobox(self.frame, values=["256", "1000"])
        self.packet_size_combobox.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        # Combobox para Direction
        self.direction_label = tk.Label(self.frame, text="Direction")
        self.direction_label.grid(row=1, column=2, padx=20, pady=20, sticky="ew")
        self.direction_combobox = ttk.Combobox(self.frame, values=["Uplink", "Downlink"])
        self.direction_combobox.grid(row=1, column=3, padx=20, pady=20, sticky="ew")'''

    
