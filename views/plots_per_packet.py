import matplotlib.pyplot as plt
import tkinter as tk
from views.results_view import Results_view


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

import re
import os
import mplcursors



class Plots_per_packet(tk.Frame):
    def __init__(self, root):
        self.root = root
        #self.ssh_ue = None

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
        bit_rates = ["3", "4", "5", "10"]
        self.bit_rate_combobox = ttk.Combobox(self.frame, values=bit_rates)
        self.bit_rate_combobox.grid(row=1, column=3, padx=20, pady=5, sticky="ew")
        self.bit_rate_combobox.set("3")


        #Iteration options
        self.entry_label_iteration = tk.Label(self.frame, text="Enter the iteration number: ")
        self.entry_label_iteration.grid(row=1, column=4, padx=20, pady=20, sticky="nsew")
        iterations = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.entry_iteration = ttk.Combobox(self.frame, values=iterations)
        self.entry_iteration.grid(row=1, column=5, padx=20, pady=20, sticky="nsew")
        self.entry_iteration.set("1")

        #plot button
        self.plot_button = tk.Button(self.frame, text="Plot", command=self.plot_4_metrics_gui)
        self.plot_button.grid(row=1, column=6, padx=20, pady=20, sticky="nsew")

        #save button
        self.save_button = tk.Button(self.frame, text="Save plots", command=self.save_plots)
        self.save_button.grid(row=1, column=7, padx=20, pady=5, sticky="ew")

        
    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

    def plot_latencies_scatter_with_lines_gui(self, ax, packet_numbers, latencies):
        bit_rate = self.bit_rate_combobox.get()
        ax.plot(packet_numbers, latencies, marker='o', linestyle='', color='g', markersize=1)
        ax.set_xlabel('Packet Number')
        ax.set_ylabel('(ms)')
        ax.set_title(f'Latency per packet at {bit_rate}Mbps')
        ax.grid(False)
        ax.set_xticks(range(0, len(packet_numbers), 1000))
        #ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
    

    def plot_tp_bar_gui(self, ax, slot_numbers, throughput):
        ax.bar(slot_numbers, throughput, color='red')
        ax.set_xlabel('Time slots (ms)')
        ax.set_ylabel('(Mbps)')
        ax.set_title('Tx Throughput per time slot')
        ax.grid(False)
        ax.set_xticks(range(0, len(slot_numbers), 500))

    def plot_iat_histogram_gui(self, ax, inter_arrival_times):
        filtered_times = [time for time in inter_arrival_times if time < 5]
        bit_rate = self.bit_rate_combobox.get()
        bins = 50
        ax.hist(filtered_times, bins=bins, color='royalblue', edgecolor='royalblue', alpha=0.9)
        ax.set_xlabel('Inter Arrival Time (ms)')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Inter Arrival Time histogram at {bit_rate}Mbps')
        ax.grid(False)

    def plot_tp_bar_rx_gui(self, ax, slot_numbers, throughput):
        ax.bar(slot_numbers, throughput, color='darkorange')
        ax.set_xlabel('Time slots (ms)')
        ax.set_ylabel('(Mbps)')
        ax.set_title('Rx Throughput per time slot')
        ax.grid(False)
        ax.set_xticks(range(0, len(slot_numbers), 500))


    def plot_4_metrics_gui(self):
        self.inner_frame = tk.Frame(self.frame)
        self.inner_frame.grid(row=4, column=0, padx=20, pady=5, sticky="ew", columnspan=15)

        fig_latency = Figure(figsize=(3.5, 2.5), dpi=110)
        ax_latency = fig_latency.add_subplot(111)
        fig2 = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2 = fig2.add_subplot(111)
        fig3_pl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax3_pl = fig3_pl.add_subplot(111)
        fig4_iat = Figure(figsize=(3.5, 2.5), dpi=100)
        ax4_iat = fig4_iat.add_subplot(111)

        direction = self.direction_combobox.get()
        if direction == 'Uplink':
             direction_graph = 'uplink'
        elif direction == 'Downlink':
            direction_graph = 'downlink'

        bit_rate = self.bit_rate_combobox.get()
        iteration = self.entry_iteration.get()

        #figure1
        latencies = Results_view.extract_all_latencies(Results_view,f"latencies/{direction}_{bit_rate}Mbps_1300bytes_{iteration}_latencies.txt")
        packet_numbers_latencies = list(range(1, len(latencies) + 1))
        #figure2
        throughput = Results_view.extract_all_throughputs(Results_view,f"throughput/{direction}_{bit_rate}Mbps_1300bytes_{iteration}_throughput.txt")
        slot_numbers = list(range(1, len(throughput) + 1))

        #figure3
        inter_arrival_times = Results_view.extract_all_inter_arrival_times(Results_view,f"inter_arrival_times/{direction}_{bit_rate}Mbps_1300bytes_{iteration}_inter_arrival_times.txt")

        #figure4
        throughputs_rx = Results_view.extract_all_throughputs_rx(Results_view,f"throughput_rx/{direction}_{bit_rate}Mbps_1300bytes_{iteration}_rx_throughput.txt")
        slot_number_throughputs = list(range(1, len(throughputs_rx) + 1))


        self.plot_latencies_scatter_with_lines_gui(ax_latency, packet_numbers_latencies, latencies)
        self.plot_tp_bar_gui(ax2, slot_numbers, throughput)
        self.plot_iat_histogram_gui(ax3_pl, inter_arrival_times)
        self.plot_tp_bar_rx_gui(ax4_iat, slot_number_throughputs, throughputs_rx)

        fig_latency.tight_layout()
        fig2.tight_layout()
        fig3_pl.tight_layout()
        fig4_iat.tight_layout()

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

        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_rowconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=1)

        return fig_latency, fig2, fig3_pl, fig4_iat

   
    def save_plots(self):
        if not os.path.exists("plots_per_packet"):
                os.makedirs("plots_per_packet")
        
        fig_latency, fig2, fig3_pl, fig4_iat = self.plot_4_metrics_gui()
        if self.bit_rate_combobox.get() == "5" and self.direction_combobox.get() == "Downlink":
                fig_latency.savefig('plots_per_packet/latency_5Mbps_dl.png', dpi=600)
                fig2.savefig('plots_per_packet/throughput_5Mbps_dl.png', dpi=600)
                fig3_pl.savefig('plots_per_packet/inter_arrival_time_5Mbps_dl.png', dpi=600)
                fig4_iat.savefig('plots_per_packet/throughput_rx_5Mbps_dl.png', dpi=600)
        elif self.bit_rate_combobox.get() == "10" and self.direction_combobox.get() == "Downlink":
                fig_latency.savefig('plots_per_packet/latency_10Mbps_dl.png', dpi=600)
                fig2.savefig('plots_per_packet/throughput_10Mbps_dl.png', dpi=600)
                fig3_pl.savefig('plots_per_packet/inter_arrival_time_10Mbps_dl.png', dpi=600)
                fig4_iat.savefig('plots_per_packet/throughput_rx_10Mbps_dl.png.png', dpi=600)
        elif self.bit_rate_combobox.get() == "3" and self.direction_combobox.get() == "Uplink":
                fig_latency.savefig('plots_per_packet/latency_3Mbps_ul.png', dpi=600)
                fig2.savefig('plots_per_packet/throughput_3Mbps_ul.png', dpi=600)
                fig3_pl.savefig('plots_per_packet/inter_arrival_time_3Mbps_ul.png', dpi=600)
                fig4_iat.savefig('plots_per_packet/throughput_rx_3Mbps_ul.png', dpi=600)
        elif self.bit_rate_combobox.get() == "4" and self.direction_combobox.get() == "Uplink":
                fig_latency.savefig('plots_per_packet/latency_4Mbps_ul.png', dpi=600)
                fig2.savefig('plots_per_packet/throughput_4Mbps_ul.png', dpi=600)
                fig3_pl.savefig('plots_per_packet/inter_arrival_time_4Mbps_ul.png', dpi=600)
                fig4_iat.savefig('plots_per_packet/throughput_rx_4Mbps_ul.png.png', dpi=600)
        print("Plots saved in plots_per_packet folder")    
    
