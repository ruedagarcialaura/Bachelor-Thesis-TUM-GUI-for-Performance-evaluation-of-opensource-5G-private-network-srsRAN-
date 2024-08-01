import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

import re
import os
import mplcursors

 
class Results_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()


        # Combobox for Direction
        self.direction_label = tk.Label(self.frame, text="Traffic Direction:")
        self.direction_combobox = ttk.Combobox(self.frame, values=["Uplink", "Downlink"])
        self.direction_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")  
        self.direction_combobox.grid(row=1, column=1, padx=20, pady=5, sticky="ew")  
        self.direction_combobox.set("Uplink")

        # Combobox for bit rate
        self.bit_rate_label = tk.Label(self.frame, text="Sending bit Rate in Mbps:")
        self.bit_rate_label.grid(row=1, column=2, padx=20, pady=5, sticky="w")  
        bit_rates = ["3", "4", "5", "10", "All"]
        self.bit_rate_combobox = ttk.Combobox(self.frame, values=bit_rates)
        self.bit_rate_combobox.grid(row=1, column=3, padx=20, pady=5, sticky="ew")
        self.bit_rate_combobox.set("3")

        #metric combobox
        self.metric_label = tk.Label(self.frame, text="Metric:")
        self.metric_combobox = ttk.Combobox(self.frame, values=["Latency", "Throughput", "Packet Loss", "Inter Arrival Time", "All", "TX and RX Throughput"])
        self.metric_label.grid(row=1, column=4, padx=20, pady=5, sticky="w") 
        self.metric_combobox.grid(row=1, column=5, padx=20, pady=5, sticky="ew")
        self.metric_combobox.set("Latency")


        self.button = tk.Button(self.frame, text="PLOT", command=self.show_plots)
        self.button.grid(row=1, column=6, padx=20, pady=5, sticky="ew")

        #save button
        self.save_button = tk.Button(self.frame, text="SAVE", command=self.save_plots)
        self.save_button.grid(row=1, column=7, padx=20, pady=5, sticky="ew")

        #self.save_button2 = tk.Button(self.frame, text="Save TP comparison", command=self.save_plot_comparison)
        #self.save_button2.grid(row=1, column=8, padx=20, pady=5, sticky="ew")
        #print("Results view initialized")

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

        
    def plot_4_metrics(self):
        
        self.inner_frame = tk.Frame(self.frame)
        self.inner_frame.grid(row=4, column=0, padx=20, pady=5, sticky="ew", columnspan=13)
        medianprops1 = dict(color='crimson')
        

        # Create a Matplotlib figure and axes
        fig_latency = Figure(figsize=(3.5, 2.5), dpi=110)
        ax_latency = fig_latency.add_subplot(111)

        direction = self.direction_combobox.get()
        if direction == 'Uplink':
             direction_graph = 'uplink'
        elif direction == 'Downlink':
            direction_graph = 'downlink'

        bit_rate = self.bit_rate_combobox.get()


        box1 = ax_latency.boxplot(
            [self.extract_all_latencies(f'latencies/{direction}_{bit_rate}Mbps_1300bytes_1_latencies.txt')],
            medianprops=medianprops1, positions=[1])
        box2 = ax_latency.boxplot(
            [self.extract_all_latencies(f'latencies/{direction}_{bit_rate}Mbps_1300bytes_2_latencies.txt')],
            medianprops=medianprops1,positions=[2])
        box3 = ax_latency.boxplot(
            [self.extract_all_latencies(f'latencies/{direction}_{bit_rate}Mbps_1300bytes_3_latencies.txt')],
            medianprops=medianprops1,positions=[3])
        box4 = ax_latency.boxplot(
            [self.extract_all_latencies(f'latencies/{direction}_{bit_rate}Mbps_1300bytes_4_latencies.txt')],
            medianprops=medianprops1,positions=[4])
        box5 = ax_latency.boxplot(
            [self.extract_all_latencies(f'latencies/{direction}_{bit_rate}Mbps_1300bytes_5_latencies.txt')],
            medianprops=medianprops1,positions=[5])
        box6 = ax_latency.boxplot(
            [self.extract_all_latencies(f'latencies/{direction}_{bit_rate}Mbps_1300bytes_6_latencies.txt')],
            medianprops=medianprops1,positions=[6])
        box7 = ax_latency.boxplot(
            [self.extract_all_latencies(f'latencies/{direction}_{bit_rate}Mbps_1300bytes_7_latencies.txt')],
            medianprops=medianprops1,positions=[7])
        box8 = ax_latency.boxplot(
            [self.extract_all_latencies(f'latencies/{direction}_{bit_rate}Mbps_1300bytes_8_latencies.txt')],
            medianprops=medianprops1,positions=[8])
        box9 = ax_latency.boxplot(
            [self.extract_all_latencies(f'latencies/{direction}_{bit_rate}Mbps_1300bytes_9_latencies.txt')],
            medianprops=medianprops1,positions=[9])
        box10 = ax_latency.boxplot(
            [self.extract_all_latencies(f'latencies/{direction}_{bit_rate}Mbps_1300bytes_10_latencies.txt')],
            medianprops=medianprops1,positions=[10])
        
       
        
        
        #create a Matplotlib figure and axes
        fig2 = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2 = fig2.add_subplot(111)
        box1 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_1_throughput.txt')],
            medianprops=medianprops1,positions=[1])
        box2 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_2_throughput.txt')],
            medianprops=medianprops1,positions=[2])
        box3 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_3_throughput.txt')],
            medianprops=medianprops1,positions=[3])
        box4 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_4_throughput.txt')],
            medianprops=medianprops1,positions=[4])
        box5 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_5_throughput.txt')],
            medianprops=medianprops1,positions=[5])
        box6 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_6_throughput.txt')],
            medianprops=medianprops1,positions=[6])
        box7 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_7_throughput.txt')],
            medianprops=medianprops1,positions=[7])
        box8 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_8_throughput.txt')],
            medianprops=medianprops1,positions=[8])
        box9 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_9_throughput.txt')],
            medianprops=medianprops1,positions=[9])
        box10 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_10_throughput.txt')],
            medianprops=medianprops1,positions=[10])
        
        


        
        


        # Create a Matplotlib figure and axes
        fig3_pl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax3_pl = fig3_pl.add_subplot(111)
        box1 = ax3_pl.boxplot(
            [self.extract_packet_loss_percentages(f'packet_loss/{direction}_{bit_rate}Mbps_1300bytes_1_packet_loss.txt')],
            medianprops=medianprops1,positions=[1])
        box2 = ax3_pl.boxplot(
            [self.extract_packet_loss_percentages(f'packet_loss/{direction}_{bit_rate}Mbps_1300bytes_2_packet_loss.txt')],
            medianprops=medianprops1,positions=[2])
        box3 = ax3_pl.boxplot(
            [self.extract_packet_loss_percentages(f'packet_loss/{direction}_{bit_rate}Mbps_1300bytes_3_packet_loss.txt')],
            medianprops=medianprops1,positions=[3])
        box4 = ax3_pl.boxplot(
            [self.extract_packet_loss_percentages(f'packet_loss/{direction}_{bit_rate}Mbps_1300bytes_4_packet_loss.txt')],
            medianprops=medianprops1,positions=[4])
        box5 = ax3_pl.boxplot(
            [self.extract_packet_loss_percentages(f'packet_loss/{direction}_{bit_rate}Mbps_1300bytes_5_packet_loss.txt')],
            medianprops=medianprops1,positions=[5])
        box6 = ax3_pl.boxplot(
            [self.extract_packet_loss_percentages(f'packet_loss/{direction}_{bit_rate}Mbps_1300bytes_6_packet_loss.txt')],
            medianprops=medianprops1,positions=[6])
        box7 = ax3_pl.boxplot(
            [self.extract_packet_loss_percentages(f'packet_loss/{direction}_{bit_rate}Mbps_1300bytes_7_packet_loss.txt')],
            medianprops=medianprops1,positions=[7])
        box8 = ax3_pl.boxplot(
            [self.extract_packet_loss_percentages(f'packet_loss/{direction}_{bit_rate}Mbps_1300bytes_8_packet_loss.txt')],
            medianprops=medianprops1,positions=[8])
        box9 = ax3_pl.boxplot(
            [self.extract_packet_loss_percentages(f'packet_loss/{direction}_{bit_rate}Mbps_1300bytes_9_packet_loss.txt')],
            medianprops=medianprops1,positions=[9])
        box10 = ax3_pl.boxplot(
            [self.extract_packet_loss_percentages(f'packet_loss/{direction}_{bit_rate}Mbps_1300bytes_10_packet_loss.txt')],
            medianprops=medianprops1,positions=[10])
        
        
        
        fig4_iat = Figure(figsize=(3.5, 2.5), dpi=100)
        ax4_iat = fig4_iat.add_subplot(111)
        box1 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_1_rx_throughput.txt')],
            medianprops=medianprops1, positions=[1])
        box2 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_2_rx_throughput.txt')],
            medianprops=medianprops1, positions=[2])
        box3 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_3_rx_throughput.txt')],
            medianprops=medianprops1, positions=[3])
        box4 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_4_rx_throughput.txt')],
            medianprops=medianprops1, positions=[4])
        box5 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_5_rx_throughput.txt')],
            medianprops=medianprops1, positions=[5])
        box6 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_6_rx_throughput.txt')],
            medianprops=medianprops1, positions=[6])
        box7 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_7_rx_throughput.txt')],
            medianprops=medianprops1, positions=[7])
        box8 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_8_rx_throughput.txt')],
            medianprops=medianprops1, positions=[8])
        box9 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_9_rx_throughput.txt')],
            medianprops=medianprops1, positions=[9])
        box10 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_10_rx_throughput.txt')],
            medianprops=medianprops1, positions=[10])
        
        

        ax_latency.set_title('Latency', fontsize=7)  # Set fontsize to 7 or any desired size
        ax2.set_title('Sending Throughput', fontsize=7)
        ax3_pl.set_title('Packet Loss', fontsize=7)
        ax4_iat.set_title('Receiving Throughput', fontsize=7)
        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']   
        ax_latency.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

            # Then set the custom labels
        ax_latency.set_xticklabels(labels, fontsize=7)
        ax2.set_xticklabels(labels, fontsize=7)
        ax3_pl.set_xticklabels(labels, fontsize=7)
        ax4_iat.set_xticklabels(labels, fontsize=7)

        ax_latency.tick_params(axis='y', labelsize=7)
        ax2.tick_params(axis='y', labelsize=7)
        ax3_pl.tick_params(axis='y', labelsize=7)
        ax4_iat.tick_params(axis='y', labelsize=7)

        # Set y-axis labels with units
        ax_latency.set_ylabel('(ms)', fontsize=7)
        ax2.set_ylabel('(Mbps)', fontsize=7)
        ax3_pl.set_ylabel('(%)', fontsize=7)
        ax4_iat.set_ylabel('(Mbps)',fontsize=7)

        ax_latency.set_xlabel('Test Number', fontsize=7)
        ax2.set_xlabel('Test Number', fontsize=7)
        ax3_pl.set_xlabel('Test Number', fontsize=7)
        ax4_iat.set_xlabel('Test Number', fontsize=7)

        # Adjust layout to make sure everything fits
        fig_latency.tight_layout()
        fig2.tight_layout()
        fig3_pl.tight_layout()
        fig4_iat.tight_layout()


        # Embed the figure in the Tkinter window
        canvas_latency_dl = FigureCanvasTkAgg(fig_latency, master=self.inner_frame)
        canvas_latency_dl.draw()
        canvas_latency_dl.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        cursor_latency = mplcursors.cursor(canvas_latency_dl.figure, hover=True)
        cursor_latency.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))


        canvas2_tp_dl = FigureCanvasTkAgg(fig2, master=self.inner_frame)
        canvas2_tp_dl.draw()
        canvas2_tp_dl.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        cursor_tp = mplcursors.cursor(canvas2_tp_dl.figure, hover=True)
        cursor_tp.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas3_pl_dl = FigureCanvasTkAgg(fig3_pl, master=self.inner_frame)
        canvas3_pl_dl.draw()
        canvas3_pl_dl.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        cursor_pl = mplcursors.cursor(canvas3_pl_dl.figure, hover=True)
        cursor_pl.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas4_iat_dl = FigureCanvasTkAgg(fig4_iat, master=self.inner_frame)
        canvas4_iat_dl.draw()
        canvas4_iat_dl.get_tk_widget().grid(row=1, column=1, sticky="nsew")
        cursor_iat = mplcursors.cursor(canvas4_iat_dl.figure, hover=True)
        cursor_iat.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        # Configure the grid to expand equally
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_rowconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=1)

        return fig_latency, fig2, fig3_pl, fig4_iat

    def plot_throughput_comparison(self):
    
        self.inner_frame = tk.Frame(self.frame)
        self.inner_frame.grid(row=4, column=0, padx=20, pady=5, sticky="ew", columnspan=10)
        medianprops1 = dict(color='crimson')

        direction = self.direction_combobox.get()
        if direction == 'Uplink':
             direction_graph = 'uplink'
        elif direction == 'Downlink':
            direction_graph = 'downlink'

        bit_rate = self.bit_rate_combobox.get()


        fig2 = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2 = fig2.add_subplot(111)
        box1 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_1_throughput.txt')],
            medianprops=medianprops1,positions=[1])
        box2 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_2_throughput.txt')],
            medianprops=medianprops1,positions=[2])
        box3 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_3_throughput.txt')],
            medianprops=medianprops1,positions=[3])
        box4 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_4_throughput.txt')],
            medianprops=medianprops1,positions=[4])
        box5 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_5_throughput.txt')],
            medianprops=medianprops1,positions=[5])
        box6 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_6_throughput.txt')],
            medianprops=medianprops1,positions=[6])
        box7 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_7_throughput.txt')],
            medianprops=medianprops1,positions=[7])
        box8 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_8_throughput.txt')],
            medianprops=medianprops1,positions=[8])
        box9 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_9_throughput.txt')],
            medianprops=medianprops1,positions=[9])
        box10 = ax2.boxplot(
            [self.extract_all_throughputs(f'throughput/{direction}_{bit_rate}Mbps_1300bytes_10_throughput.txt')],
            medianprops=medianprops1,positions=[10])
        
        fig4_iat = Figure(figsize=(3.5, 2.5), dpi=100)
        ax4_iat = fig4_iat.add_subplot(111)
        box1 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_1_rx_throughput.txt')],
            medianprops=medianprops1, positions=[1])
        box2 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_2_rx_throughput.txt')],
            medianprops=medianprops1, positions=[2])
        box3 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_3_rx_throughput.txt')],
            medianprops=medianprops1, positions=[3])
        box4 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_4_rx_throughput.txt')],
            medianprops=medianprops1, positions=[4])
        box5 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_5_rx_throughput.txt')],
            medianprops=medianprops1, positions=[5])
        box6 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_6_rx_throughput.txt')],
            medianprops=medianprops1, positions=[6])
        box7 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_7_rx_throughput.txt')],
            medianprops=medianprops1, positions=[7])
        box8 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_8_rx_throughput.txt')],
            medianprops=medianprops1, positions=[8])
        box9 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_9_rx_throughput.txt')],
            medianprops=medianprops1, positions=[9])
        box10 = ax4_iat.boxplot(
            [self.extract_all_throughputs_rx(f'throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_10_rx_throughput.txt')],
            medianprops=medianprops1, positions=[10])
        
        ax2.set_title('Throughput', fontsize=7)
        ax4_iat.set_title('Arrival Throughput', fontsize=7)
        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']   
        ax2.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

            # Then set the custom labels
        ax2.set_xticklabels(labels, fontsize=7)
        ax4_iat.set_xticklabels(labels, fontsize=7)

        ax2.tick_params(axis='y', labelsize=7)
        ax4_iat.tick_params(axis='y', labelsize=7)

        # Set y-axis labels with units
        ax2.set_ylabel('(Mbps)', fontsize=7)
        ax4_iat.set_ylabel('(Mbps)',fontsize=7)

        ax2.set_xlabel('Test Number', fontsize=7)
        ax4_iat.set_xlabel('Test Number', fontsize=7)

        # Adjust layout to make sure everything fits
        fig2.tight_layout()
        fig4_iat.tight_layout()

        canvas2_tp_dl = FigureCanvasTkAgg(fig2, master=self.inner_frame)
        canvas2_tp_dl.draw()
        canvas2_tp_dl.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        cursor_tp = mplcursors.cursor(canvas2_tp_dl.figure, hover=True)
        cursor_tp.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas4_iat_dl = FigureCanvasTkAgg(fig4_iat, master=self.inner_frame)
        canvas4_iat_dl.draw()
        canvas4_iat_dl.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        cursor_iat = mplcursors.cursor(canvas4_iat_dl.figure, hover=True)
        cursor_iat.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        # Configure the grid to expand equally
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_rowconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=1)

        return fig2, fig4_iat
  
    def plot_1_metric(self): 
        
        self.inner_frame = tk.Frame(self.frame)
        self.inner_frame.grid(row=4, column=0, padx=20, pady=5, sticky="ew", columnspan=10)
        medianprops1 = dict(color='limegreen')

        # Create a Matplotlib figure and axes
        figure = Figure(figsize=(3.5, 2.5), dpi=110)     
        ax = figure.add_subplot(111)

        direction = self.direction_combobox.get()
        if direction == 'Uplink':
             direction_graph = 'uplink'
        elif direction == 'Downlink':
            direction_graph = 'downlink'

        bit_rate = self.bit_rate_combobox.get()

        metric = self.metric_combobox.get()
        if metric == 'Latency':
            metric_graph = 'latencies'
        elif metric == 'Throughput':
            metric_graph = 'throughput'
        elif metric == 'Packet Loss':
            metric_graph = 'packet_loss'
        elif metric == 'Inter Arrival Time':
            metric_graph = 'inter_arrival_times'
        #elif metric == 'TX and RX Throughput':
         #   self.plot_throughput_comparison()
        
        # Create boxplots separately
        box1 = ax.boxplot(
            [self.extract_all_values(f'{metric_graph}/{direction_graph}_{bit_rate}Mbps_1300bytes_1_{metric_graph}.txt')], 
            medianprops=medianprops1, positions=[1])
        box2 = ax.boxplot(
            [self.extract_all_values(f'{metric_graph}/{direction_graph}_{bit_rate}Mbps_1300bytes_2_{metric_graph}.txt')],
            medianprops=medianprops1, positions=[2])
        box3 = ax.boxplot(
            [self.extract_all_values(f'{metric_graph}/{direction_graph}_{bit_rate}Mbps_1300bytes_3_{metric_graph}.txt')],
            medianprops=medianprops1, positions=[3])
        box4 = ax.boxplot(
            [self.extract_all_values(f'{metric_graph}/{direction_graph}_{bit_rate}Mbps_1300bytes_4_{metric_graph}.txt')],
            medianprops=medianprops1, positions=[4])
        box5 = ax.boxplot(
            [self.extract_all_values(f'{metric_graph}/{direction_graph}_{bit_rate}Mbps_1300bytes_5_{metric_graph}.txt')],
            medianprops=medianprops1, positions=[5])
        box6 = ax.boxplot(
            [self.extract_all_values(f'{metric_graph}/{direction_graph}_{bit_rate}Mbps_1300bytes_6_{metric_graph}.txt')],
            medianprops=medianprops1, positions=[6])
        box7 = ax.boxplot(
            [self.extract_all_values(f'{metric_graph}/{direction_graph}_{bit_rate}Mbps_1300bytes_7_{metric_graph}.txt')],
            medianprops=medianprops1, positions=[7])
        box8 = ax.boxplot(
            [self.extract_all_values(f'{metric_graph}/{direction_graph}_{bit_rate}Mbps_1300bytes_8_{metric_graph}.txt')],
            medianprops=medianprops1, positions=[8])
        box9 = ax.boxplot(
            [self.extract_all_values(f'{metric_graph}/{direction_graph}_{bit_rate}Mbps_1300bytes_9_{metric_graph}.txt')],
            medianprops=medianprops1, positions=[9])
        box10 = ax.boxplot(
            [self.extract_all_values(f'{metric_graph}/{direction_graph}_{bit_rate}Mbps_1300bytes_10_{metric_graph}.txt')],
            medianprops=medianprops1, positions=[10])
        

        #appearance of the graph
        ax.set_title(f'{metric}', fontsize=7)      
        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  
        ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])        
        ax.set_xticklabels(labels, fontsize=7)
        ax.tick_params(axis='y', labelsize=7)
        if metric == 'Latency' or metric == 'Inter Arrival Time':
            ax.set_ylabel('(ms)', fontsize=7)
        elif metric == 'Throughput':
            ax.set_ylabel('(Mbps)', fontsize=7)
        elif metric == 'Packet Loss':
            ax.set_ylabel('(%)', fontsize=7)
        ax.set_xlabel('Test Number', fontsize=7)
        figure.tight_layout()

        # Embed the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(figure, master=self.inner_frame)  
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)
        cursor = mplcursors.cursor(canvas.figure, hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))
        
        return figure 

    def show_plots(self):
        if self.metric_combobox.get() == "All":
            self.plot_4_metrics()
        elif (self.metric_combobox.get() != "All" and self.metric_combobox.get() != "TX and RX Throughput") and ((self.direction_combobox.get() == "Uplink" and self.bit_rate_combobox.get() == "3") or (self.direction_combobox.get() == "Uplink" and self.bit_rate_combobox.get() == "4") or (self.direction_combobox.get() == "Downlink" and self.bit_rate_combobox.get() == "5") or (self.direction_combobox.get() == "Downlink" and self.bit_rate_combobox.get() == "10")):
            self.plot_1_metric()
        elif self.metric_combobox.get() == "TX and RX Throughput":
            self.plot_throughput_comparison()
        else:
            messagebox.showerror("Error", "Please select the correct options")
            print(f"error: {self.direction_combobox.get()}, {self.bit_rate_combobox.get()}, {self.metric_combobox.get()}")
               
    def save_plots(self):
        if not os.path.exists("plots"):
                os.makedirs("plots")
        if self.metric_combobox.get() == "All":
            fig_latency, fig2, fig3_pl, fig4_iat = self.plot_4_metrics()
            if self.bit_rate_combobox.get() == "5" and self.direction_combobox.get() == "Downlink":
                fig_latency.savefig('plots/latency_5Mbps_dl.png', dpi=600)
                fig2.savefig('plots/throughput_5Mbps_dl.png', dpi=600)
                fig3_pl.savefig('plots/packetloss_5Mbps_dl.png', dpi=600)
                fig4_iat.savefig('plots/inter_arrival_time_5Mbps_dl.png', dpi=600)
            elif self.bit_rate_combobox.get() == "10" and self.direction_combobox.get() == "Downlink":
                fig_latency.savefig('plots/latency_10Mbps_dl.png', dpi=600)
                fig2.savefig('plots/throughput_10Mbps_dl.png', dpi=600)
                fig3_pl.savefig('plots/packetloss_10Mbps_dl.png', dpi=600)
                fig4_iat.savefig('plots/inter_arrival_time_10Mbps_dl.png', dpi=600)
            elif self.bit_rate_combobox.get() == "3" and self.direction_combobox.get() == "Uplink":
                fig_latency.savefig('plots/latency_3Mbps_ul.png', dpi=600)
                fig2.savefig('plots/throughput_3Mbps_ul.png', dpi=600)
                fig3_pl.savefig('plots/packetloss_3Mbps_ul.png', dpi=600)
                fig4_iat.savefig('plots/inter_arrival_time_3Mbps_ul.png', dpi=600)
            elif self.bit_rate_combobox.get() == "4" and self.direction_combobox.get() == "Uplink":
                fig_latency.savefig('plots/latency_4Mbps_ul.png', dpi=600)
                fig2.savefig('plots/throughput_4Mbps_ul.png', dpi=600)
                fig3_pl.savefig('plots/packetloss_4Mbps_ul.png', dpi=600)
                fig4_iat.savefig('plots/inter_arrival_time_4Mbps_ul.png', dpi=600)
            print("Plots saved in plots folder")
        elif (self.metric_combobox.get() != "All" and self.metric_combobox.get() != "TX and RX Throughput") and ((self.direction_combobox.get() == "Uplink" and self.bit_rate_combobox.get() == "3") or (self.direction_combobox.get() == "Uplink" and self.bit_rate_combobox.get() == "4") or (self.direction_combobox.get() == "Downlink" and self.bit_rate_combobox.get() == "5") or (self.direction_combobox.get() == "Downlink" and self.bit_rate_combobox.get() == "10")):
            figure = self.plot_1_metric()
            if self.metric_combobox.get() == "Latency":
                if self.bit_rate_combobox.get() == "5" and self.direction_combobox.get() == "Downlink":
                    figure.savefig('plots/latency_5Mbps_dl.png', dpi=600)
                elif self.bit_rate_combobox.get() == "10" and self.direction_combobox.get() == "Downlink":
                    figure.savefig('plots/latency_10Mbps_dl.png', dpi=600)
                elif self.bit_rate_combobox.get() == "3" and self.direction_combobox.get() == "Uplink":
                    figure.savefig('plots/latency_3Mbps_ul.png', dpi=600)
                elif self.bit_rate_combobox.get() == "4" and self.direction_combobox.get() == "Uplink":
                    figure.savefig('plots/latency_4Mbps_ul.png', dpi=600)
            elif self.metric_combobox.get() == "Throughput":
                if self.bit_rate_combobox.get() == "5" and self.direction_combobox.get() == "Downlink":
                    figure.savefig('plots/throughput_5Mbps_dl.png', dpi=600)
                elif self.bit_rate_combobox.get() == "10" and self.direction_combobox.get() == "Downlink":
                    figure.savefig('plots/throughput_10Mbps_dl.png', dpi=600)
                elif self.bit_rate_combobox.get() == "3" and self.direction_combobox.get() == "Uplink":
                    figure.savefig('plots/throughput_3Mbps_ul.png', dpi=600)
                elif self.bit_rate_combobox.get() == "4" and self.direction_combobox.get() == "Uplink":
                    figure.savefig('plots/throughput_4Mbps_ul.png', dpi=600)
            elif self.metric_combobox.get() == "Packet Loss":
                if self.bit_rate_combobox.get() == "5" and self.direction_combobox.get() == "Downlink":
                    figure.savefig('plots/packetloss_5Mbps_dl.png', dpi=600)
                elif self.bit_rate_combobox.get() == "10" and self.direction_combobox.get() == "Downlink":
                    figure.savefig('plots/packetloss_10Mbps_dl.png', dpi=600)
                elif self.bit_rate_combobox.get() == "3" and self.direction_combobox.get() == "Uplink":
                    figure.savefig('plots/packetloss_3Mbps_ul.png', dpi=600)
                elif self.bit_rate_combobox.get() == "4" and self.direction_combobox.get() == "Uplink":
                    figure.savefig('plots/packetloss_4Mbps_ul.png', dpi=600)
            elif self.metric_combobox.get() == "Inter Arrival Time":
                if self.bit_rate_combobox.get() == "5" and self.direction_combobox.get() == "Downlink":
                    figure.savefig('plots/inter_arrival_time_5Mbps_dl.png', dpi=600)
                elif self.bit_rate_combobox.get() == "10" and self.direction_combobox.get() == "Downlink":
                    figure.savefig('plots/inter_arrival_time_10Mbps_dl.png', dpi=600)
                elif self.bit_rate_combobox.get() == "3" and self.direction_combobox.get() == "Uplink":
                    figure.savefig('plots/inter_arrival_time_3Mbps_ul.png', dpi=600)
                elif self.bit_rate_combobox.get() == "4" and self.direction_combobox.get() == "Uplink":
                    figure.savefig('plots/inter_arrival_time_4Mbps_ul.png', dpi=600)
        elif self.metric_combobox.get() == "TX and RX Throughput":
            tp_tx, tp_rx = self.plot_throughput_comparison()
            if self.bit_rate_combobox.get() == "5" and self.direction_combobox.get() == "Downlink":
                tp_tx.savefig('plots/throughput_tx_5Mbps_dl.png', dpi=600)
                tp_rx.savefig('plots/throughput_rx_5Mbps_dl.png', dpi=600)
            elif self.bit_rate_combobox.get() == "10" and self.direction_combobox.get() == "Downlink":
                tp_tx.savefig('plots/throughput_tx_10Mbps_dl.png', dpi=600)
                tp_rx.savefig('plots/throughput_rx_10Mbps_dl.png', dpi=600)
            elif self.bit_rate_combobox.get() == "3" and self.direction_combobox.get() == "Uplink":
                tp_tx.savefig('plots/throughput_tx_3Mbps_ul.png', dpi=600)
                tp_rx.savefig('plots/throughput_rx_3Mbps_ul.png', dpi=600)
            elif self.bit_rate_combobox.get() == "4" and self.direction_combobox.get() == "Uplink":
                tp_tx.savefig('plots/throughput_tx_4Mbps_ul.png', dpi=600)
                tp_rx.savefig('plots/throughput_rx_4Mbps_ul.png', dpi=600
            )


    
 


    def extract_average_latencies(self, file_path):
        # Compile the regular expression to match the average latencies
        pattern = re.compile(r'The average latency is: (\d+\.\d+) milliseconds')
        average_latency_values = []

        # Open the file and read it line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Search for matches using the pattern
                match = pattern.search(line)
                if match:
                    # Convert the matched value to float and add it to the list
                    average_latency_values.append(float(match.group(1)))

        return average_latency_values
    
    def extract__latency_standard_deviation(self, file_path):
        # Compile the regular expression to match the standard deviation
        pattern = re.compile(r'The standard deviation is: (\d+\.\d+) milliseconds')
        latency_standard_deviation = []

        # Open the file and read it line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Search for matches using the pattern
                match = pattern.search(line)
                if match:
                    # Convert the matched value to float and add it to the list
                    latency_standard_deviation.append(float(match.group(1)))

        return latency_standard_deviation
    
    def extract_average_inter_arrival_times(self, file_path):
        # Compile the regular expression to match the average times
        pattern = re.compile(r'The average inter arrival time is: (\d+\.\d+) milliseconds')
        average_inter_arrival__times = []

        # Open the file and read it line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Search for matches using the pattern
                match = pattern.search(line)
                if match:
                    # Convert the matched value to float and add it to the list
                    average_inter_arrival__times.append(float(match.group(1)))

        return average_inter_arrival__times
    
    def extract_inter_arrival_time_standard_deviation(self, file_path):
        # Compile the regular expression to match the standard deviation
        pattern = re.compile(r'The standard deviation is: (\d+\.\d+) milliseconds')
        inter_arrival_time_standard_deviation = []

        # Open the file and read it line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Search for matches using the pattern
                match = pattern.search(line)
                if match:
                    # Convert the matched value to float and add it to the list
                    inter_arrival_time_standard_deviation.append(float(match.group(1)))

        return inter_arrival_time_standard_deviation
    
    def extract_average_throughput(self, file_path):
        # Compile the regular expression to match the average throughput
        pattern = re.compile(r'The average throughput is: (\d+\.\d+) Mbps')
        average_throughput_values = []

        # Open the file and read it line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Search for matches using the pattern
                match = pattern.search(line)
                if match:
                    # Convert the matched value to float and add it to the list
                    average_throughput_values.append(float(match.group(1)))

        return average_throughput_values
    
    def extract_throughput_standard_deviation(self, file_path):
        # Compile the regular expression to match the standard deviation
        pattern = re.compile(r'The standard deviation is: (\d+\.\d+) Mbps')
        throughput_standard_deviation = []

        # Open the file and read it line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Search for matches using the pattern
                match = pattern.search(line)
                if match:
                    # Convert the matched value to float and add it to the list
                    throughput_standard_deviation.append(float(match.group(1)))

        return throughput_standard_deviation
    

    def extract_all_values(self, file_path):
        if self.metric_combobox.get() == "Latency":
            all_latencies = []
            try:
                # Open the file and read it line by line
                with open(file_path, 'r') as file:
                    collecting = False
                    for line in file:
                    # Check if the line is a start marker
                        if line.startswith("Latencies for"):
                            collecting = True
                            continue
                        # Check if the line is an end marker
                        elif line.startswith("The average latency is:") or line.startswith("The standard deviation is:"):
                            collecting = False
                            continue
                        # If we are between the markers, collect the values
                        if collecting:
                            try:
                                # Convert the line to a float and append it to the list
                                latency_value = float(line.strip())
                                all_latencies.append(latency_value)
                            except ValueError:
                                # Handle the case where conversion to float fails
                                pass
                return all_latencies
            except FileNotFoundError:
                print(f"File not found: {file_path}")
                return all_latencies
        elif self.metric_combobox.get() == "Throughput":
            all_throughputs = []
            try:
                # Open the file and read it line by line
                with open(file_path, 'r') as file:
                    collecting = False
                    for line in file:
                        # Check if the line is a start marker
                        if line.startswith("Sending Throughput for"):
                            collecting = True
                            continue
                        # Check if the line is an end marker
                        elif line.startswith("The average throughput is:"):
                            collecting = False
                            continue
                        # If we are between the markers, collect the values
                        if collecting:
                            try:
                                # Convert the line to a float and append it to the list
                                throughput_value = float(line.strip())
                                all_throughputs.append(throughput_value)                
                            except ValueError:
                                # Handle the case where conversion to float fails
                                pass
                #print(all_throughputs)
                return all_throughputs
                
            except FileNotFoundError:
                print(f"File not found: {file_path}")
                # Filtrar valores mayores que 10
                return all_throughputs
            
        elif self.metric_combobox.get() == "Packet Loss":
            packet_loss_percentages = []
            try:
                # Compile the regular expression to match the packet loss percentages
                pattern = re.compile(r'corresponds to (\d+\.\d+)%')
                

                # Open the file and read it line by line
                with open(file_path, 'r') as file:
                    for line in file:
                        # Search for matches using the pattern
                        match = pattern.search(line)
                        if match:
                            # Convert the matched value to float and add it to the list
                            packet_loss_percentages.append(float(match.group(1)))

                return packet_loss_percentages
            except FileNotFoundError:
                print(f"File not found: {file_path}")
                return packet_loss_percentages 
        elif self.metric_combobox.get() == "Inter Arrival Time":
            all_inter_arrival_times = []
            try:
                # Open the file and read it line by line
                with open(file_path, 'r') as file:
                    collecting = False
                    
                    for line in file:
                        # Check if the line is a start marker
                        if line.startswith("Inter arrival times for"):
                            collecting = True
                            continue
                        # Check if the line is an end marker
                        elif line.startswith("The average inter arrival time is:"):
                            collecting = False
                            continue
                        # If we are between the markers, collect the values
                        if collecting:
                            try:
                                # Convert the line to a float and append it to the list
                                time_value = float(line.strip())
                                all_inter_arrival_times.append(time_value)
                            except ValueError:
                                # Handle the case where conversion to float fails
                                pass

                return all_inter_arrival_times
            except FileNotFoundError:
                print(f"File not found: {file_path}")
                return all_inter_arrival_times
    
    def extract_all_latencies(self, file_path):
        all_latencies = []
        try:
                # Open the file and read it line by line
                with open(file_path, 'r') as file:
                    collecting = False
                    for line in file:
                    # Check if the line is a start marker
                        if line.startswith("Latencies for"):
                            collecting = True
                            continue
                        # Check if the line is an end marker
                        elif line.startswith("The average latency is:") or line.startswith("The standard deviation is:"):
                            collecting = False
                            continue
                        # If we are between the markers, collect the values
                        if collecting:
                            try:
                                # Convert the line to a float and append it to the list
                                latency_value = float(line.strip())
                                all_latencies.append(latency_value)
                            except ValueError:
                                # Handle the case where conversion to float fails
                                pass
                return all_latencies
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return all_latencies

    def extract_all_throughputs_rx(self,file_path):
        all_throughputs = []
        try:
            # Open the file and read it line by line
            with open(file_path, 'r') as file:
                collecting = False
                for line in file:
                    # Check if the line is a start marker
                    if line.startswith("Receiving Throughput for"):
                        collecting = True
                        continue
                    # Check if the line is an end marker
                    elif line.startswith("The average throughput is:"):
                        collecting = False
                        continue
                    # If we are between the markers, collect the values
                    if collecting:
                        try:
                            # Convert the line to a float and append it to the list
                            throughput_value = float(line.strip())
                            all_throughputs.append(throughput_value)
                            #all_throughputs = [value for value in all_throughputs if value <= 10]
                        except ValueError:
                            # Handle the case where conversion to float fails
                            pass
            return all_throughputs
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return all_throughputs
        
    def extract_all_throughputs(self,file_path):
        all_throughputs = []
        try:
            # Open the file and read it line by line
            with open(file_path, 'r') as file:
                collecting = False
                for line in file:
                    # Check if the line is a start marker
                    if line.startswith("Sending Throughput for"):
                        collecting = True
                        continue
                    # Check if the line is an end marker
                    elif line.startswith("The average throughput is:"):
                        collecting = False
                        continue
                    # If we are between the markers, collect the values
                    if collecting:
                        try:
                            # Convert the line to a float and append it to the list
                            throughput_value = float(line.strip())
                            all_throughputs.append(throughput_value)
                            #all_throughputs = [value for value in all_throughputs if value <= 10]
                        except ValueError:
                            # Handle the case where conversion to float fails
                            pass
            return all_throughputs
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return all_throughputs
            
    def extract_packet_loss_percentages(self,file_path):
        packet_loss_percentages = []
        try:
            # Compile the regular expression to match the packet loss percentages
            pattern = re.compile(r'corresponds to (\d+\.\d+)%')
            

            # Open the file and read it line by line
            with open(file_path, 'r') as file:
                for line in file:
                    # Search for matches using the pattern
                    match = pattern.search(line)
                    if match:
                        # Convert the matched value to float and add it to the list
                        packet_loss_percentages.append(float(match.group(1)))

            return packet_loss_percentages
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return packet_loss_percentages 

    def extract_all_inter_arrival_times(self,file_path):
        all_inter_arrival_times = []
        try:
            # Open the file and read it line by line
            with open(file_path, 'r') as file:
                collecting = False
                
                for line in file:
                    # Check if the line is a start marker
                    if line.startswith("Inter arrival times for"):
                        collecting = True
                        continue
                    # Check if the line is an end marker
                    elif line.startswith("The average inter arrival time is:"):
                        collecting = False
                        continue
                    # If we are between the markers, collect the values
                    if collecting:
                        try:
                            # Convert the line to a float and append it to the list
                            time_value = float(line.strip())
                            all_inter_arrival_times.append(time_value)
                            #all_inter_arrival_times = [value for value in all_inter_arrival_times if value <= 25]
                        except ValueError:
                            # Handle the case where conversion to float fails
                            pass

            return all_inter_arrival_times
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return all_inter_arrival_times


      