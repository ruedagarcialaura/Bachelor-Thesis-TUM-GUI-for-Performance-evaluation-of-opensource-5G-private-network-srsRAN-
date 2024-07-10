import tkinter as tk
import tkinter.ttk as ttk

class GUI_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.title_label = tk.Label(self.frame, text="Performance Evaluation of srsRAN", font=("Helvetica", 16, "bold"), fg="blue")
        self.title_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew", columnspan=3)

        # Adjust font size for instructions and reduce vertical padding
        font_settings = ("Helvetica", 10)  # Define a common font setting for instructions
        wrap_length = 500  # Define a common wrap length in pixels

        self.intructions_label1 = tk.Label(self.frame, text="Utilize this tool to acquire data from your 5G RAN network for comprehensive analysis.", font=font_settings, wraplength=wrap_length)
        self.intructions_label1.grid(row=1, column=0, padx=20, pady=5, sticky="ew", columnspan=3)

        self.intructions_label2 = tk.Label(self.frame, text="Following the buttons on the top you can navigate through the different views.", font=font_settings, wraplength=wrap_length)
        self.intructions_label2.grid(row=2, column=0, padx=20, pady=5, sticky="ew", columnspan=3)

        self.separator_horizontal = ttk.Separator(self.frame, orient='horizontal')
        self.separator_horizontal.grid(row=3, column=0, columnspan=10, sticky='ew', pady=10)

        self.intructions_label3 = tk.Label(self.frame, text="STEP 1: Connect to your srsRAN network by clicking on the 'Connect to the network' button.", font=font_settings, wraplength=wrap_length)
        self.intructions_label3.grid(row=4, column=0, padx=20, pady=5, sticky="w", columnspan=3)

        self.intructions_label4 = tk.Label(self.frame, text="STEP 2: 1st.Start Wireshark on both the user Equipment and the Core Network User interfaces to capture the traffic. 2nd.Generate this traffic using Iperf3:Start the server part. 3rd.Generate traffic from the client side. 4th.Once the iperf3 test is done,stop Wireshark on both sides by clicking on 'Stop Capture'.", font=font_settings, wraplength=wrap_length)
        self.intructions_label4.grid(row=5, column=0, padx=20, pady=5, sticky="w", columnspan=3)

        self.intructions_label5 = tk.Label(self.frame, text="STEP 3: Analyze the data by clicking on the 'Calculations' button. Here you can calculate the average latency, packets loss, average throughput, and the inter-arrival time of your captured traffic.", font=font_settings, wraplength=wrap_length)
        self.intructions_label5.grid(row=6, column=0, padx=20, pady=5, sticky="w", columnspan=3)

        self.intructions_label6 = tk.Label(self.frame, text="STEP 4: Check the results by clicking on the 'Results' button. Here, you will see the obtained data presented in a plotted format for a more visual analysis. You can choose to view either your downlink or uplink data.", font=font_settings, wraplength=wrap_length)
        self.intructions_label6.grid(row=7, column=0, padx=20, pady=5, sticky="w", columnspan=3)


        self.separator_horizontal = ttk.Separator(self.frame, orient='horizontal')
        self.separator_horizontal.grid(row=8, column=0, columnspan=10, sticky='ew', pady=10)

        self.intructions_label7 = tk.Label(self.frame, text="Have fun and enjoy the tool!", font=font_settings, wraplength=wrap_length, justify=tk.CENTER)
        self.intructions_label7.grid(row=9, column=0, padx=20, pady=5, sticky="ew", columnspan=3)

        self.intructions_label8 = tk.Label(self.frame, text="Developed by Laura Rueda García, 2024", font=font_settings, wraplength=wrap_length, justify=tk.CENTER)
        self.intructions_label8.grid(row=10, column=0, padx=20, pady=5, sticky="ew", columnspan=3)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

