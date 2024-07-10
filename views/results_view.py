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
        self.direction_label = tk.Label(self.frame, text="Direction")
        self.direction_combobox = ttk.Combobox(self.frame, values=["Uplink", "Downlink", "uplink 3Mbps", "uplink 4Mbps", "downlink 5Mbps", "downlink 10Mbps"])
        self.direction_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")  # Adjusted row
        self.direction_combobox.grid(row=1, column=1, padx=20, pady=5, sticky="ew")  # Adjusted row
        self.direction_combobox.set("Uplink")

        # Combobox for Metric
        self.metric_label = tk.Label(self.frame, text="Metric")
        self.metric_label.grid(row=1, column=2, padx=20, pady=5, sticky="w")  # Adjusted row
        metrics = ["Latency", "Throughput", "Packet Loss", "Inter Arrival Time", "All"]
        self.metric_combobox = ttk.Combobox(self.frame, values=metrics)
        self.metric_combobox.grid(row=1, column=3, padx=20, pady=5, sticky="ew")  # Adjusted row

        # Combobox for bit rate
        self.bit_rate_label = tk.Label(self.frame, text="Bit Rate (Mbps)")
        self.bit_rate_label.grid(row=1, column=4, padx=20, pady=5, sticky="w")
        bit_rates = ["3", "4", "5", "10", "All"]
        self.bit_rate_combobox = ttk.Combobox(self.frame, values=bit_rates)
        self.bit_rate_combobox.grid(row=1, column=5, padx=20, pady=5, sticky="ew")

        self.button = tk.Button(self.frame, text="Show Plotted Data", command=self.show_plotted_data)
        self.button.grid(row=1, column=6, padx=20, pady=5, sticky="ew")

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

    def plot_ul(self):

        self.inner_frame_ul = tk.Frame(self.frame)
        self.inner_frame_ul.grid(row=2, column=0, padx=20, pady=5, sticky="ew", columnspan=7)

        medianprops1 = dict(color='navy')
        medianprops2 = dict(color='limegreen')

        

        # Create a Matplotlib figure and axes
        fig_latency_ul = Figure(figsize=(3.5, 2.5), dpi=100)     
        ax_latency_ul = fig_latency_ul.add_subplot(111)
        
        # Create boxplots separately
        box1 = ax_latency_ul.boxplot(
            [self.extract_all_latencies('latencies/uplink_3Mbps_1300bytes_latencies.txt')], 
            medianprops=medianprops1, positions=[1])
        box2 = ax_latency_ul.boxplot(
            [self.extract_all_latencies('latencies/uplink_4Mbps_1300bytes_latencies.txt')], 
            medianprops=medianprops2,positions=[2])
        
         # Create a Matplotlib figure and axes
        fig2_tp_ul = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2_tp_ul = fig2_tp_ul.add_subplot(111)
        
        # Create boxplots separately
        box3 = ax2_tp_ul.boxplot(
            [self.extract_all_throughputs('throughput/uplink_3Mbps_1300bytes_throughput.txt')], 
            medianprops=medianprops1, positions=[1])
        box4 = ax2_tp_ul.boxplot(
            [self.extract_all_throughputs('throughput/uplink_4Mbps_1300bytes_throughput.txt')], 
            medianprops=medianprops2,  positions=[2])

        fig3_pl_ul = Figure(figsize=(3.5, 2.5), dpi=100)
        ax3_pl_ul = fig3_pl_ul.add_subplot(111)
        
        # Create boxplots separately
        box5 = ax3_pl_ul.boxplot(
            [self.extract_packet_loss_percentages('packet_loss/uplink_3Mbps_1300bytes_packet_loss.txt')], 
            medianprops=medianprops1,  positions=[1])
        box6 = ax3_pl_ul.boxplot(
            [self.extract_packet_loss_percentages('packet_loss/uplink_4Mbps_1300bytes_packet_loss.txt')], 
            medianprops=medianprops2, positions=[2])

        fig4_iat_ul = Figure(figsize=(3.5, 2.5), dpi=100) 
        ax4_iat_ul = fig4_iat_ul.add_subplot(111)
        
        # Create boxplots separately
        box7 = ax4_iat_ul.boxplot(
            [self.extract_all_inter_arrival_times('inter_arrival_time/uplink_3Mbps_1300bytes_inter_arrival_times.txt')], 
            medianprops=medianprops1, positions=[1])
        box8 = ax4_iat_ul.boxplot(
            [self.extract_all_inter_arrival_times('inter_arrival_time/uplink_4Mbps_1300bytes_inter_arrival_times.txt')], 
            medianprops=medianprops2, positions=[2])



        '''# Create a Matplotlib figure and axes
        fig_latency_ul = Figure(figsize=(3.5, 2.5), dpi=100)     
        ax_latency_ul = fig_latency_ul.add_subplot(111)
        ax_latency_ul.boxplot([self.extract_all_latencies('latencies/uplink_1Mbps_1300bytes_latencies.txt'), self.extract_all_latencies('latencies/uplink_3Mbps_1300bytes_latencies.txt')], medianprops= medianprops1, medianprops = medianprops2)

        
        # Create a Matplotlib figure and axes
        fig2_tp_ul = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2_tp_ul = fig2_tp_ul.add_subplot(111)
        ax2_tp_ul.boxplot([self.extract_all_throughputs('throughput/uplink_1Mbps_1300bytes_throughput.txt'), self.extract_all_throughputs('throughput/uplink_3Mbps_1300bytes_throughput.txt')], medianprops= medianprops1) #, medianprops = medianprops2)

        fig3_pl_ul = Figure(figsize=(3.5, 2.5), dpi=100)
        ax3_pl_ul = fig3_pl_ul.add_subplot(111)
        ax3_pl_ul.boxplot([self.extract_packet_loss_percentages('packet_loss/uplink_1Mbps_1300bytes_packet_loss.txt'), self.extract_packet_loss_percentages('packet_loss/uplink_3Mbps_1300bytes_packet_loss.txt')], medianprops= medianprops1) #, medianprops = medianprops2)

        fig4_iat_ul = Figure(figsize=(3.5, 2.5), dpi=100) 
        ax4_iat_ul = fig4_iat_ul.add_subplot(111)
        ax4_iat_ul.boxplot([self.extract_all_inter_arrival_times('inter_arrival_time/uplink_1Mbps_1300bytes_inter_arrival_times.txt'), self.extract_all_inter_arrival_times('inter_arrival_times/uplink_3Mbps_1300bytes_inter_arrival_times.txt')], medianprops= medianprops1) #, medianprops = medianprops2)
        '''

        ax_latency_ul.set_title('Latency', fontsize=7)  # Set fontsize to 7 or any desired size
        ax2_tp_ul.set_title('Throughput', fontsize=7)
        ax3_pl_ul.set_title('Packet Loss', fontsize=7)
        ax4_iat_ul.set_title('Inter Sending Time', fontsize=7)



            # Add labels and title
            # Custom labels for the x-axis
       
        labels = ['3 Mbps', '4 Mbps']

            # Set the position of the ticks first
        ax_latency_ul.set_xticks([1, 2])

            # Then set the custom labels
        ax_latency_ul.set_xticklabels(labels, fontsize=7)
        ax2_tp_ul.set_xticklabels(labels, fontsize=7)
        ax3_pl_ul.set_xticklabels(labels, fontsize=7)
        ax4_iat_ul.set_xticklabels(labels, fontsize=7)

        ax_latency_ul.tick_params(axis='y', labelsize=7)
        ax2_tp_ul.tick_params(axis='y', labelsize=7)
        ax3_pl_ul.tick_params(axis='y', labelsize=7)
        ax4_iat_ul.tick_params(axis='y', labelsize=7)

        # Set y-axis labels with units
        ax_latency_ul.set_ylabel('(ms)', fontsize=7)
        ax2_tp_ul.set_ylabel('(Mbps)', fontsize=7)
        ax3_pl_ul.set_ylabel('(%)', fontsize=7)
        ax4_iat_ul.set_ylabel('(ms)',fontsize=7)

        # Adjust layout to make sure everything fits
        fig_latency_ul.tight_layout()
        fig2_tp_ul.tight_layout()
        fig3_pl_ul.tight_layout()
        fig4_iat_ul.tight_layout()


    


        # Embed the figure in the Tkinter window
        canvas_latency_ul = FigureCanvasTkAgg(fig_latency_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master
        canvas_latency_ul.draw()
        canvas_latency_ul.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        cursor_latency = mplcursors.cursor(canvas_latency_ul.figure, hover=True)
        cursor_latency.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))


        canvas2_tp_ul = FigureCanvasTkAgg(fig2_tp_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master
        canvas2_tp_ul.draw()
        canvas2_tp_ul.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        cursor_tp = mplcursors.cursor(canvas2_tp_ul.figure, hover=True)
        cursor_tp.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas3_pl_ul = FigureCanvasTkAgg(fig3_pl_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master
        canvas3_pl_ul.draw()
        canvas3_pl_ul.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        cursor_pl = mplcursors.cursor(canvas3_pl_ul.figure, hover=True)
        cursor_pl.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas4_iat_ul = FigureCanvasTkAgg(fig4_iat_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master 
        canvas4_iat_ul.draw()
        canvas4_iat_ul.get_tk_widget().grid(row=1, column=1, sticky="nsew")
        cursor_iat = mplcursors.cursor(canvas4_iat_ul.figure, hover=True)
        cursor_iat.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))


                # Configure the grid to expand equally
        self.inner_frame_ul.grid_rowconfigure(0, weight=1)
        self.inner_frame_ul.grid_rowconfigure(1, weight=1)
        self.inner_frame_ul.grid_columnconfigure(0, weight=1)
        self.inner_frame_ul.grid_columnconfigure(1, weight=1)
        
    def plot_dl(self):    
        
        self.inner_frame_dl = tk.Frame(self.frame)
        self.inner_frame_dl.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        medianprops1 = dict(color='crimson')
        medianprops2 = dict(color='darkorange')

        '''# Extract lists of numerical values
        mean_latency_5Mbps = self.extract_average_latencies('latencies/downlink_5Mbps_1300bytes_latencies.txt')
        std_latency_5Mbps = self.extract__latency_standard_deviation('latencies/downlink_5Mbps_1300bytes_latencies.txt')
        mean_latency_10Mbps = self.extract_average_latencies('latencies/downlink_10Mbps_1300bytes_latencies.txt')
        std_latency_10Mbps = self.extract__latency_standard_deviation('latencies/downlink_10Mbps_1300bytes_latencies.txt')

        # Create box plot data
        box_data_5Mbps = [
            [m - 1.5 * s for m, s in zip(mean_latency_5Mbps, std_latency_5Mbps)],  # Lower whisker
            [m - s for m, s in zip(mean_latency_5Mbps, std_latency_5Mbps)],        # Lower quartile
            mean_latency_5Mbps,                                                   # Median (mean)
            [m + s for m, s in zip(mean_latency_5Mbps, std_latency_5Mbps)],        # Upper quartile
            [m + 1.5 * s for m, s in zip(mean_latency_5Mbps, std_latency_5Mbps)]   # Upper whisker
        ]

        box_data_10Mbps = [
            [m - 1.5 * s for m, s in zip(mean_latency_10Mbps, std_latency_10Mbps)],  # Lower whisker
            [m - s for m, s in zip(mean_latency_10Mbps, std_latency_10Mbps)],        # Lower quartile
            mean_latency_10Mbps,                                                     # Median (mean)
            [m + s for m, s in zip(mean_latency_10Mbps, std_latency_10Mbps)],        # Upper quartile
            [m + 1.5 * s for m, s in zip(mean_latency_10Mbps, std_latency_10Mbps)]   # Upper whisker
        ]'''



        '''# Perform element-wise operations
        #lower_5Mbps = [m - s for m, s in zip(mean_latency_5Mbps, std_latency_5Mbps)]
        #upper_5Mbps = [m + s for m, s in zip(mean_latency_5Mbps, std_latency_5Mbps)]
        #lower_10Mbps = [m - s for m, s in zip(mean_latency_10Mbps, std_latency_10Mbps)]
        #upper_10Mbps = [m + s for m, s in zip(mean_latency_10Mbps, std_latency_10Mbps)]
        box1 = ax_latency_dl.boxplot(
            [lower_5Mbps, mean_latency_5Mbps, upper_5Mbps], 
            medianprops=medianprops1, positions=[1])
        box2 = ax_latency_dl.boxplot(
            [lower_10Mbps, mean_latency_10Mbps, upper_10Mbps], 
            medianprops=medianprops2, positions=[2])'''
        
        '''box1 = ax_latency_dl.boxplot(
            [box_data_5Mbps], 
            medianprops=medianprops1, positions=[1])
        box2 = ax_latency_dl.boxplot(
            [box_data_10Mbps], 
            medianprops=medianprops2, positions=[2])
        box1 = ax_latency_dl.boxplot(
            [[self.extract_average_latencies('latencies/downlink_5Mbps_1300bytes_latencies.txt') - self.extract__latency_standard_deviation('latencies/downlink_5Mbps_1300bytes_latencies.txt')],self.extract_average_latencies('latencies/downlink_5Mbps_1300bytes_latencies.txt'), [self.extract_average_latencies('latencies/downlink_5Mbps_1300bytes_latencies.txt') + self.extract__latency_standard_deviation('latencies/downlink_10Mbps_1300bytes_latencies.txt')]],
            medianprops=medianprops1, positions=[1])
        box2 = ax_latency_dl.boxplot(
            [[self.extract_average_latencies('latencies/downlink_10Mbps_1300bytes_latencies.txt') - self.extract__latency_standard_deviation('latencies/downlink_10Mbps_1300bytes_latencies.txt')],self.extract_average_latencies('latencies/downlink_10Mbps_1300bytes_latencies.txt'), [self.extract_average_latencies('latencies/downlink_10Mbps_1300bytes_latencies.txt') + self.extract__latency_standard_deviation('latencies/downlink_10Mbps_1300bytes_latencies.txt')]],
            medianprops=medianprops2, positions=[2])'''


        # Create a Matplotlib figure and axes
        fig_latency_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax_latency_dl = fig_latency_dl.add_subplot(111)
        box1 = ax_latency_dl.boxplot(
            [self.extract_all_latencies('latencies/downlink_5Mbps_1300bytes_latencies.txt')],
            medianprops=medianprops1, positions=[1])
        box2 = ax_latency_dl.boxplot(
            [self.extract_all_latencies('latencies/downlink_10Mbps_1300bytes_latencies.txt')],
            medianprops=medianprops2,positions=[2])
        
        
        #create a Matplotlib figure and axes
        fig2_tp_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2_tp_dl = fig2_tp_dl.add_subplot(111)
        box3 = ax2_tp_dl.boxplot(
            [self.extract_all_throughputs('throughput/downlink_5Mbps_1300bytes_throughput.txt')],
            medianprops=medianprops1,positions=[1])
        box4 = ax2_tp_dl.boxplot(
            [self.extract_all_throughputs('throughput/downlink_10Mbps_1300bytes_throughput.txt')],
            medianprops=medianprops2,positions=[2])


        # Create a Matplotlib figure and axes
        fig3_pl_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax3_pl_dl = fig3_pl_dl.add_subplot(111)
        box5 = ax3_pl_dl.boxplot(
            [self.extract_packet_loss_percentages('packet_loss/downlink_5Mbps_1300bytes_packet_loss.txt')],
            medianprops=medianprops1,positions=[1])
        box6 = ax3_pl_dl.boxplot(
            [self.extract_packet_loss_percentages('packet_loss/downlink_10Mbps_1300bytes_packet_loss.txt')],
            medianprops=medianprops2, positions=[2])
        
        # Create a Matplotlib figure and axes
        fig4_iat_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax4_iat_dl = fig4_iat_dl.add_subplot(111)
        box7 = ax4_iat_dl.boxplot(
            [self.extract_all_inter_arrival_times('inter_arrival_time/downlink_5Mbps_1300bytes_inter_arrival_times.txt')],
            medianprops=medianprops1, positions=[1])
        box8 = ax4_iat_dl.boxplot(
            [self.extract_all_inter_arrival_times('inter_arrival_time/downlink_10Mbps_1300bytes_inter_arrival_times.txt')],
            medianprops=medianprops2,positions=[2])
        

        ax_latency_dl.set_title('Latency', fontsize=7)  # Set fontsize to 7 or any desired size
        ax2_tp_dl.set_title('Throughput', fontsize=7)
        ax3_pl_dl.set_title('Packet Loss', fontsize=7)
        ax4_iat_dl.set_title('Inter Sending Time', fontsize=7)
            
    
    
                # Add labels and title
                # Custom labels for the x-axis
        
        
        labels = ['5 Mbps', '10 Mbps']



            # Set the position of the ticks first   
        ax_latency_dl.set_xticks([1, 2])

            # Then set the custom labels
        ax_latency_dl.set_xticklabels(labels, fontsize=7)
        ax2_tp_dl.set_xticklabels(labels, fontsize=7)
        ax3_pl_dl.set_xticklabels(labels, fontsize=7)
        ax4_iat_dl.set_xticklabels(labels, fontsize=7)

        ax_latency_dl.tick_params(axis='y', labelsize=7)
        ax2_tp_dl.tick_params(axis='y', labelsize=7)
        ax3_pl_dl.tick_params(axis='y', labelsize=7)
        ax4_iat_dl.tick_params(axis='y', labelsize=7)

        # Set y-axis labels with units
        ax_latency_dl.set_ylabel('(ms)', fontsize=7)
        ax2_tp_dl.set_ylabel('(Mbps)', fontsize=7)
        ax3_pl_dl.set_ylabel('(%)', fontsize=7)
        ax4_iat_dl.set_ylabel('(ms)',fontsize=7)

        # Adjust layout to make sure everything fits
        fig_latency_dl.tight_layout()
        fig2_tp_dl.tight_layout()
        fig3_pl_dl.tight_layout()
        fig4_iat_dl.tight_layout()

        '''# Define colors for each boxplot
        colors = ['crimson', 'darkorange']

        # Apply colors to each boxplot
        for ax in [ax_latency_dl, ax2_tp_dl, ax3_pl_dl, ax4_iat_dl]:
            for patch, color in zip(ax.artists, colors):
                patch.set_edgecolor(color)
                patch.set_facecolor('none')'''
        
        

        # Embed the figure in the Tkinter window
        canvas_latency_dl = FigureCanvasTkAgg(fig_latency_dl, master=self.inner_frame_dl)
        canvas_latency_dl.draw()
        canvas_latency_dl.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        #mplcursors.cursor(canvas_latency_dl.figure, hover=True)
        cursor_latency = mplcursors.cursor(canvas_latency_dl.figure, hover=True)
        cursor_latency.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))
        canvas2_tp_dl = FigureCanvasTkAgg(fig2_tp_dl, master=self.inner_frame_dl)
        canvas2_tp_dl.draw()
        canvas2_tp_dl.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        cursor_tp = mplcursors.cursor(canvas2_tp_dl.figure, hover=True) 
        cursor_tp.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))
    


        canvas3_pl_dl = FigureCanvasTkAgg(fig3_pl_dl, master=self.inner_frame_dl)
        canvas3_pl_dl.draw()
        canvas3_pl_dl.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        cursor_pl = mplcursors.cursor(canvas3_pl_dl.figure, hover=True)
        cursor_pl.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))
       
        canvas4_iat_dl = FigureCanvasTkAgg(fig4_iat_dl, master=self.inner_frame_dl)
        canvas4_iat_dl.draw()
        canvas4_iat_dl.get_tk_widget().grid(row=1, column=1, sticky="nsew")
        cursor_iat = mplcursors.cursor(canvas4_iat_dl.figure, hover=True)
        cursor_iat.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))
       
        # Configure the grid to expand equally
        self.inner_frame_dl.grid_rowconfigure(0, weight=1)
        self.inner_frame_dl.grid_rowconfigure(1, weight=1)
        self.inner_frame_dl.grid_columnconfigure(0, weight=1)
        self.inner_frame_dl.grid_columnconfigure(1, weight=1)

    def plot_dl_5Mbps(self):
        
        self.inner_frame_dl = tk.Frame(self.frame)
        self.inner_frame_dl.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        medianprops1 = dict(color='crimson')
        

        # Create a Matplotlib figure and axes
        fig_latency_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax_latency_dl = fig_latency_dl.add_subplot(111)
        box1 = ax_latency_dl.boxplot(
            [self.extract_all_latencies('latencies/downlink_5Mbps_1300bytes_latencies.txt')],
            medianprops=medianprops1, positions=[1])
       
        
        
        #create a Matplotlib figure and axes
        fig2_tp_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2_tp_dl = fig2_tp_dl.add_subplot(111)
        box3 = ax2_tp_dl.boxplot(
            [self.extract_all_throughputs('throughput/downlink_5Mbps_1300bytes_throughput.txt')],
            medianprops=medianprops1,positions=[1])
        


        # Create a Matplotlib figure and axes
        fig3_pl_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax3_pl_dl = fig3_pl_dl.add_subplot(111)
        box5 = ax3_pl_dl.boxplot(
            [self.extract_packet_loss_percentages('packet_loss/downlink_5Mbps_1300bytes_packet_loss.txt')],
            medianprops=medianprops1,positions=[1])
        
        
        # Create a Matplotlib figure and axes
        fig4_iat_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax4_iat_dl = fig4_iat_dl.add_subplot(111)
        box7 = ax4_iat_dl.boxplot(
            [self.extract_all_inter_arrival_times('inter_arrival_time/downlink_5Mbps_1300bytes_inter_arrival_times.txt')],
            medianprops=medianprops1, positions=[1])
        
        

        ax_latency_dl.set_title('Latency', fontsize=7)  # Set fontsize to 7 or any desired size
        ax2_tp_dl.set_title('Throughput', fontsize=7)
        ax3_pl_dl.set_title('Packet Loss', fontsize=7)
        ax4_iat_dl.set_title('Inter Sending Time', fontsize=7)
            
    
    
                # Add labels and title
                # Custom labels for the x-axis
        
        
        labels = ['5 Mbps']



            # Set the position of the ticks first   
        ax_latency_dl.set_xticks([1])

            # Then set the custom labels
        ax_latency_dl.set_xticklabels(labels, fontsize=7)
        ax2_tp_dl.set_xticklabels(labels, fontsize=7)
        ax3_pl_dl.set_xticklabels(labels, fontsize=7)
        ax4_iat_dl.set_xticklabels(labels, fontsize=7)

        ax_latency_dl.tick_params(axis='y', labelsize=7)
        ax2_tp_dl.tick_params(axis='y', labelsize=7)
        ax3_pl_dl.tick_params(axis='y', labelsize=7)
        ax4_iat_dl.tick_params(axis='y', labelsize=7)

        # Set y-axis labels with units
        ax_latency_dl.set_ylabel('(ms)', fontsize=7)
        ax2_tp_dl.set_ylabel('(Mbps)', fontsize=7)
        ax3_pl_dl.set_ylabel('(%)', fontsize=7)
        ax4_iat_dl.set_ylabel('(ms)',fontsize=7)

        # Adjust layout to make sure everything fits
        fig_latency_dl.tight_layout()
        fig2_tp_dl.tight_layout()
        fig3_pl_dl.tight_layout()
        fig4_iat_dl.tight_layout()


        # Embed the figure in the Tkinter window
        canvas_latency_dl = FigureCanvasTkAgg(fig_latency_dl, master=self.inner_frame_dl)
        canvas_latency_dl.draw()
        canvas_latency_dl.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        cursor_latency = mplcursors.cursor(canvas_latency_dl.figure, hover=True)
        cursor_latency.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))


        canvas2_tp_dl = FigureCanvasTkAgg(fig2_tp_dl, master=self.inner_frame_dl)
        canvas2_tp_dl.draw()
        canvas2_tp_dl.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        cursor_tp = mplcursors.cursor(canvas2_tp_dl.figure, hover=True)
        cursor_tp.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas3_pl_dl = FigureCanvasTkAgg(fig3_pl_dl, master=self.inner_frame_dl)
        canvas3_pl_dl.draw()
        canvas3_pl_dl.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        cursor_pl = mplcursors.cursor(canvas3_pl_dl.figure, hover=True)
        cursor_pl.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas4_iat_dl = FigureCanvasTkAgg(fig4_iat_dl, master=self.inner_frame_dl)
        canvas4_iat_dl.draw()
        canvas4_iat_dl.get_tk_widget().grid(row=1, column=1, sticky="nsew")
        cursor_iat = mplcursors.cursor(canvas4_iat_dl.figure, hover=True)
        cursor_iat.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        # Configure the grid to expand equally
        self.inner_frame_dl.grid_rowconfigure(0, weight=1)
        self.inner_frame_dl.grid_rowconfigure(1, weight=1)
        self.inner_frame_dl.grid_columnconfigure(0, weight=1)
        self.inner_frame_dl.grid_columnconfigure(1, weight=1)

    def plot_dl_10Mbps(self):
        self.inner_frame_dl = tk.Frame(self.frame)
        self.inner_frame_dl.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        medianprops1 = dict(color='crimson')
        

        # Create a Matplotlib figure and axes
        fig_latency_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax_latency_dl = fig_latency_dl.add_subplot(111)
        box1 = ax_latency_dl.boxplot(
            [self.extract_all_latencies('latencies/downlink_10Mbps_1300bytes_latencies.txt')],
            medianprops=medianprops1, positions=[1])
       
        
        
        #create a Matplotlib figure and axes
        fig2_tp_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2_tp_dl = fig2_tp_dl.add_subplot(111)
        box3 = ax2_tp_dl.boxplot(
            [self.extract_all_throughputs('throughput/downlink_10Mbps_1300bytes_throughput.txt')],
            medianprops=medianprops1,positions=[1])
        


        # Create a Matplotlib figure and axes
        fig3_pl_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax3_pl_dl = fig3_pl_dl.add_subplot(111)
        box5 = ax3_pl_dl.boxplot(
            [self.extract_packet_loss_percentages('packet_loss/downlink_10Mbps_1300bytes_packet_loss.txt')],
            medianprops=medianprops1,positions=[1])
        
        
        # Create a Matplotlib figure and axes
        fig4_iat_dl = Figure(figsize=(3.5, 2.5), dpi=100)
        ax4_iat_dl = fig4_iat_dl.add_subplot(111)
        box7 = ax4_iat_dl.boxplot(
            [self.extract_all_inter_arrival_times('inter_arrival_time/downlink_10Mbps_1300bytes_inter_arrival_times.txt')],
            medianprops=medianprops1, positions=[1])
        
        

        ax_latency_dl.set_title('Latency', fontsize=7)  # Set fontsize to 7 or any desired size
        ax2_tp_dl.set_title('Throughput', fontsize=7)
        ax3_pl_dl.set_title('Packet Loss', fontsize=7)
        ax4_iat_dl.set_title('Inter Sending Time', fontsize=7)
            
    
    
                # Add labels and title
                # Custom labels for the x-axis
        
        
        labels = ['10 Mbps']



            # Set the position of the ticks first   
        ax_latency_dl.set_xticks([1])

            # Then set the custom labels
        ax_latency_dl.set_xticklabels(labels, fontsize=7)
        ax2_tp_dl.set_xticklabels(labels, fontsize=7)
        ax3_pl_dl.set_xticklabels(labels, fontsize=7)
        ax4_iat_dl.set_xticklabels(labels, fontsize=7)

        ax_latency_dl.tick_params(axis='y', labelsize=7)
        ax2_tp_dl.tick_params(axis='y', labelsize=7)
        ax3_pl_dl.tick_params(axis='y', labelsize=7)
        ax4_iat_dl.tick_params(axis='y', labelsize=7)

        # Set y-axis labels with units
        ax_latency_dl.set_ylabel('(ms)', fontsize=7)
        ax2_tp_dl.set_ylabel('(Mbps)', fontsize=7)
        ax3_pl_dl.set_ylabel('(%)', fontsize=7)
        ax4_iat_dl.set_ylabel('(ms)',fontsize=7)

        # Adjust layout to make sure everything fits
        fig_latency_dl.tight_layout()
        fig2_tp_dl.tight_layout()
        fig3_pl_dl.tight_layout()
        fig4_iat_dl.tight_layout()


        # Embed the figure in the Tkinter window
        canvas_latency_dl = FigureCanvasTkAgg(fig_latency_dl, master=self.inner_frame_dl)
        canvas_latency_dl.draw()
        canvas_latency_dl.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        cursor_latency = mplcursors.cursor(canvas_latency_dl.figure, hover=True)
        cursor_latency.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas2_tp_dl = FigureCanvasTkAgg(fig2_tp_dl, master=self.inner_frame_dl)
        canvas2_tp_dl.draw()
        canvas2_tp_dl.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        cursor_tp = mplcursors.cursor(canvas2_tp_dl.figure, hover=True)
        cursor_tp.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas3_pl_dl = FigureCanvasTkAgg(fig3_pl_dl, master=self.inner_frame_dl)
        canvas3_pl_dl.draw()
        canvas3_pl_dl.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        cursor_pl = mplcursors.cursor(canvas3_pl_dl.figure, hover=True)
        cursor_pl.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))


        canvas4_iat_dl = FigureCanvasTkAgg(fig4_iat_dl, master=self.inner_frame_dl)
        canvas4_iat_dl.draw()
        canvas4_iat_dl.get_tk_widget().grid(row=1, column=1, sticky="nsew")
        cursor_iat = mplcursors.cursor(canvas4_iat_dl.figure, hover=True)
        cursor_iat.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        # Configure the grid to expand equally
        self.inner_frame_dl.grid_rowconfigure(0, weight=1)
        self.inner_frame_dl.grid_rowconfigure(1, weight=1)
        self.inner_frame_dl.grid_columnconfigure(0, weight=1)
        self.inner_frame_dl.grid_columnconfigure(1, weight=1)


    def plot_ul_3Mbps(self): 
        
        self.inner_frame_ul = tk.Frame(self.frame)
        self.inner_frame_ul.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        medianprops1 = dict(color='navy')

        # Create a Matplotlib figure and axes
        fig_latency_ul = Figure(figsize=(3.5, 2.5), dpi=100)     
        ax_latency_ul = fig_latency_ul.add_subplot(111)
        
        # Create boxplots separately
        box1 = ax_latency_ul.boxplot(
            [self.extract_all_latencies('latencies/uplink_3Mbps_1300bytes_latencies.txt')], 
            medianprops=medianprops1, positions=[1])
       
         # Create a Matplotlib figure and axes
        fig2_tp_ul = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2_tp_ul = fig2_tp_ul.add_subplot(111)
        
        # Create boxplots separately
        box3 = ax2_tp_ul.boxplot(
            [self.extract_all_throughputs('throughput/uplink_3Mbps_1300bytes_throughput.txt')], 
            medianprops=medianprops1, positions=[1])
        

        fig3_pl_ul = Figure(figsize=(3.5, 2.5), dpi=100)
        ax3_pl_ul = fig3_pl_ul.add_subplot(111)
        
        # Create boxplots separately
        box5 = ax3_pl_ul.boxplot(
            [self.extract_packet_loss_percentages('packet_loss/uplink_3Mbps_1300bytes_packet_loss.txt')], 
            medianprops=medianprops1,  positions=[1])
        

        fig4_iat_ul = Figure(figsize=(3.5, 2.5), dpi=100) 
        ax4_iat_ul = fig4_iat_ul.add_subplot(111)
        
        # Create boxplots separately
        box7 = ax4_iat_ul.boxplot(
            [self.extract_all_inter_arrival_times('inter_arrival_time/uplink_3Mbps_1300bytes_inter_arrival_times.txt')], 
            medianprops=medianprops1, positions=[1])
        

        ax_latency_ul.set_title('Latency', fontsize=7)  # Set fontsize to 7 or any desired size
        ax2_tp_ul.set_title('Throughput', fontsize=7)
        ax3_pl_ul.set_title('Packet Loss', fontsize=7)
        ax4_iat_ul.set_title('Inter Sending Time', fontsize=7)



            # Add labels and title
            # Custom labels for the x-axis
       
        labels = ['3 Mbps']

            # Set the position of the ticks first
        ax_latency_ul.set_xticks([1])

            # Then set the custom labels
        ax_latency_ul.set_xticklabels(labels, fontsize=7)
        ax2_tp_ul.set_xticklabels(labels, fontsize=7)
        ax3_pl_ul.set_xticklabels(labels, fontsize=7)
        ax4_iat_ul.set_xticklabels(labels, fontsize=7)

        ax_latency_ul.tick_params(axis='y', labelsize=7)
        ax2_tp_ul.tick_params(axis='y', labelsize=7)
        ax3_pl_ul.tick_params(axis='y', labelsize=7)
        ax4_iat_ul.tick_params(axis='y', labelsize=7)

        # Set y-axis labels with units
        ax_latency_ul.set_ylabel('(ms)', fontsize=7)
        ax2_tp_ul.set_ylabel('(Mbps)', fontsize=7)
        ax3_pl_ul.set_ylabel('(%)', fontsize=7)
        ax4_iat_ul.set_ylabel('(ms)',fontsize=7)

        # Adjust layout to make sure everything fits
        fig_latency_ul.tight_layout()
        fig2_tp_ul.tight_layout()
        fig3_pl_ul.tight_layout()
        fig4_iat_ul.tight_layout()

        # Embed the figure in the Tkinter window
        canvas_latency_ul = FigureCanvasTkAgg(fig_latency_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master
        canvas_latency_ul.draw()
        canvas_latency_ul.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        cursor_latency = mplcursors.cursor(canvas_latency_ul.figure, hover=True)
        cursor_latency.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas2_tp_ul = FigureCanvasTkAgg(fig2_tp_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master
        canvas2_tp_ul.draw()
        canvas2_tp_ul.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        cursor_tp = mplcursors.cursor(canvas2_tp_ul.figure, hover=True)
        cursor_tp.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))


        canvas3_pl_ul = FigureCanvasTkAgg(fig3_pl_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master
        canvas3_pl_ul.draw()
        canvas3_pl_ul.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        cursor_pl = mplcursors.cursor(canvas3_pl_ul.figure, hover=True)
        cursor_pl.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas4_iat_ul = FigureCanvasTkAgg(fig4_iat_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master 
        canvas4_iat_ul.draw()
        canvas4_iat_ul.get_tk_widget().grid(row=1, column=1, sticky="nsew")
        cursor_iat = mplcursors.cursor(canvas4_iat_ul.figure, hover=True)
        cursor_iat.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))


                # Configure the grid to expand equally
        self.inner_frame_ul.grid_rowconfigure(0, weight=1)
        self.inner_frame_ul.grid_rowconfigure(1, weight=1)
        self.inner_frame_ul.grid_columnconfigure(0, weight=1)
        self.inner_frame_ul.grid_columnconfigure(1, weight=1)  

    def plot_ul_4Mbps(self):
        self.inner_frame_ul = tk.Frame(self.frame)
        self.inner_frame_ul.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        medianprops1 = dict(color='navy')
        
        # Create a Matplotlib figure and axes
        fig_latency_ul = Figure(figsize=(3.5, 2.5), dpi=100)     
        ax_latency_ul = fig_latency_ul.add_subplot(111)
        
        # Create boxplots separately
        box1 = ax_latency_ul.boxplot(
            [self.extract_all_latencies('latencies/uplink_4Mbps_1300bytes_latencies.txt')], 
            medianprops=medianprops1, positions=[1])
       
         # Create a Matplotlib figure and axes
        fig2_tp_ul = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2_tp_ul = fig2_tp_ul.add_subplot(111)
        
        # Create boxplots separately
        box3 = ax2_tp_ul.boxplot(
            [self.extract_all_throughputs('throughput/uplink_4Mbps_1300bytes_throughput.txt')], 
            medianprops=medianprops1, positions=[1])
        

        fig3_pl_ul = Figure(figsize=(3.5, 2.5), dpi=100)
        ax3_pl_ul = fig3_pl_ul.add_subplot(111)
        
        # Create boxplots separately
        box5 = ax3_pl_ul.boxplot(
            [self.extract_packet_loss_percentages('packet_loss/uplink_4Mbps_1300bytes_packet_loss.txt')], 
            medianprops=medianprops1,  positions=[1])
        

        fig4_iat_ul = Figure(figsize=(3.5, 2.5), dpi=100) 
        ax4_iat_ul = fig4_iat_ul.add_subplot(111)
        
        # Create boxplots separately
        box7 = ax4_iat_ul.boxplot(
            [self.extract_all_inter_arrival_times('inter_arrival_time/uplink_4Mbps_1300bytes_inter_arrival_times.txt')], 
            medianprops=medianprops1, positions=[1])
        

        ax_latency_ul.set_title('Latency', fontsize=7)  # Set fontsize to 7 or any desired size
        ax2_tp_ul.set_title('Throughput', fontsize=7)
        ax3_pl_ul.set_title('Packet Loss', fontsize=7)
        ax4_iat_ul.set_title('Inter Sending Time', fontsize=7)

        labels = ['4 Mbps']

            # Set the position of the ticks first
        ax_latency_ul.set_xticks([1])

            # Then set the custom labels
        ax_latency_ul.set_xticklabels(labels, fontsize=7)
        ax2_tp_ul.set_xticklabels(labels, fontsize=7)
        ax3_pl_ul.set_xticklabels(labels, fontsize=7)
        ax4_iat_ul.set_xticklabels(labels, fontsize=7)

        ax_latency_ul.tick_params(axis='y', labelsize=7)
        ax2_tp_ul.tick_params(axis='y', labelsize=7)
        ax3_pl_ul.tick_params(axis='y', labelsize=7)
        ax4_iat_ul.tick_params(axis='y', labelsize=7)

        # Set y-axis labels with units
        ax_latency_ul.set_ylabel('(ms)', fontsize=7)
        ax2_tp_ul.set_ylabel('(Mbps)', fontsize=7)
        ax3_pl_ul.set_ylabel('(%)', fontsize=7)
        ax4_iat_ul.set_ylabel('(ms)',fontsize=7)

        # Adjust layout to make sure everything fits
        fig_latency_ul.tight_layout()
        fig2_tp_ul.tight_layout()
        fig3_pl_ul.tight_layout()
        fig4_iat_ul.tight_layout()

        # Embed the figure in the Tkinter window
        canvas_latency_ul = FigureCanvasTkAgg(fig_latency_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master
        canvas_latency_ul.draw()
        canvas_latency_ul.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        cursor_latency = mplcursors.cursor(canvas_latency_ul.figure, hover=True)
        cursor_latency.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas2_tp_ul = FigureCanvasTkAgg(fig2_tp_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master
        canvas2_tp_ul.draw()
        canvas2_tp_ul.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        cursor_tp = mplcursors.cursor(canvas2_tp_ul.figure, hover=True)
        cursor_tp.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas3_pl_ul = FigureCanvasTkAgg(fig3_pl_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master
        canvas3_pl_ul.draw()
        canvas3_pl_ul.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        cursor_pl = mplcursors.cursor(canvas3_pl_ul.figure, hover=True)
        cursor_pl.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))

        canvas4_iat_ul = FigureCanvasTkAgg(fig4_iat_ul, master=self.inner_frame_ul)  # Use the inner_frame as the master 
        canvas4_iat_ul.draw()
        canvas4_iat_ul.get_tk_widget().grid(row=1, column=1, sticky="nsew")
        cursor_iat = mplcursors.cursor(canvas4_iat_ul.figure, hover=True)
        cursor_iat.connect("add", lambda sel: sel.annotation.set(
            text=f'{sel.target[1]:.2f}',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        ))


                # Configure the grid to expand equally
        self.inner_frame_ul.grid_rowconfigure(0, weight=1)
        self.inner_frame_ul.grid_rowconfigure(1, weight=1)
        self.inner_frame_ul.grid_columnconfigure(0, weight=1)
        self.inner_frame_ul.grid_columnconfigure(1, weight=1) 

    def save_in_arrays_ul(self):
        if not os.path.exists("arrays"):
                os.makedirs("arrays")
        data_latency_ul_3Mbps, data_latency_ul_4Mbps, data_packetloss_ul_3Mbps, data_packetloss_ul_4Mbps, data_throughput_ul_3Mbps, data_throughput_ul_4Mbps, data_arrivaltime_ul_3Mbps, data_arrivaltime_ul_4Mbps = self.get_values_for_ul_plots()
        with open('arrays/data_latency_ul_3Mbps.txt', 'w') as file:
                for item in data_latency_ul_3Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_latency_ul_4Mbps.txt', 'w') as file:
                for item in data_latency_ul_4Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_packetloss_ul_3Mbps.txt', 'w') as file:
                for item in data_packetloss_ul_3Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_packetloss_ul_4Mbps.txt', 'w') as file:
                for item in data_packetloss_ul_4Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_throughput_ul_3Mbps.txt', 'w') as file:
                for item in data_throughput_ul_3Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_throughput_ul_4Mbps.txt', 'w') as file:
                for item in data_throughput_ul_4Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_arrivaltime_ul_3Mbps.txt', 'w') as file:
                for item in data_arrivaltime_ul_3Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_arrivaltime_ul_4Mbps.txt', 'w') as file:
                for item in data_arrivaltime_ul_4Mbps:
                    file.write("%s\n" % item)
        print("Data saved in arrays folder")

    def save_in_arrays_dl(self):
        if not os.path.exists("arrays"):
                os.makedirs("arrays")
        data_latency_dl_5Mbps, data_latency_dl_10Mbps, data_packetloss_dl_5Mbps, data_packetloss_dl_10Mbps, data_throughput_dl_5Mbps, data_throughput_dl_10Mbps, data_arrivaltime_dl_5Mbps, data_arrivaltime_dl_10Mbps = self.get_values_for_dl_plots()
        with open('arrays/data_latency_dl_5Mbps.txt', 'w') as file:
                for item in data_latency_dl_5Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_latency_dl_10Mbps.txt', 'w') as file:
                for item in data_latency_dl_10Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_packetloss_dl_5Mbps.txt', 'w') as file:
                for item in data_packetloss_dl_5Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_packetloss_dl_10Mbps.txt', 'w') as file:
                for item in data_packetloss_dl_10Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_throughput_dl_5Mbps.txt', 'w') as file:
                for item in data_throughput_dl_5Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_throughput_dl_10Mbps.txt', 'w') as file:
                for item in data_throughput_dl_10Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_arrivaltime_dl_5Mbps.txt', 'w') as file:
                for item in data_arrivaltime_dl_5Mbps:
                    file.write("%s\n" % item)
        with open('arrays/data_arrivaltime_dl_10Mbps.txt', 'w') as file:
                for item in data_arrivaltime_dl_10Mbps:
                    file.write("%s\n" % item)
        print("Data saved in arrays folder")

    def show_plotted_data(self):
        if self.direction_combobox.get() == "Uplink" and self.bit_rate_combobox.get() == "All" and self.metric_combobox.get() == "All":
            self.plot_ul()
            self.save_in_arrays_ul()            
        elif self.direction_combobox.get() == "Downlink" and self.bit_rate_combobox.get() == "All" and self.metric_combobox.get() == "All":
            self.plot_dl()
            self.save_in_arrays_dl()
        elif self.direction_combobox.get() == "uplink" and self.bit_rate_combobox.get() == "3":
            self.plot_ul_3Mbps()
        elif self.direction_combobox.get() == "uplink" and self.bit_rate_combobox.get() == "4":
            self.plot_ul_4Mbps()
        elif self.direction_combobox.get() == "downlink" and self.bit_rate_combobox.get() == "5":
            self.plot_dl_5Mbps()
        elif self.direction_combobox.get() == "downlink" and self.bit_rate_combobox.get() == "10":
            self.plot_dl_10Mbps()
        else:
            messagebox.showerror("Error", "No data for the selected parameters")
        

    
    def get_values_for_dl_plots(self):
        
        data_latency_dl_5Mbps = self.extract_all_latencies('latencies/downlink_5Mbps_1300bytes_latencies.txt')
        data_latency_dl_10Mbps = self.extract_all_latencies('latencies/downlink_10Mbps_1300bytes_latencies.txt')

        data_packetloss_dl_5Mbps = self.extract_packet_loss_percentages('packet_loss/downlink_5Mbps_1300bytes_packet_loss.txt')
        data_packetloss_dl_10Mbps = self.extract_packet_loss_percentages('packet_loss/downlink_10Mbps_1300bytes_packet_loss.txt')

        data_throughput_dl_5Mbps = self.extract_all_throughputs('throughput/downlink_5Mbps_1300bytes_throughput.txt')
        data_throughput_dl_10Mbps = self.extract_all_throughputs('throughput/downlink_10Mbps_1300bytes_throughput.txt')

        data_arrivaltime_dl_5Mbps = self.extract_all_inter_arrival_times('inter_arrival_time/downlink_5Mbps_1300bytes_inter_arrival_times.txt')
        data_arrivaltime_dl_10Mbps = self.extract_all_inter_arrival_times('inter_arrival_time/downlink_10Mbps_1300bytes_inter_arrival_times.txt')

        return data_latency_dl_5Mbps, data_latency_dl_10Mbps, data_packetloss_dl_5Mbps, data_packetloss_dl_10Mbps, data_throughput_dl_5Mbps, data_throughput_dl_10Mbps, data_arrivaltime_dl_5Mbps, data_arrivaltime_dl_10Mbps
        
    def get_values_for_ul_plots(self):
    
        
        data_latency_ul_3Mbps = self.extract_all_latencies('latencies/uplink_3Mbps_1300bytes_latencies.txt')
        data_latency_ul_4Mbps = self.extract_all_latencies('latencies/uplink_4Mbps_1300bytes_latencies.txt')

        data_packetloss_ul_3Mbps = self.extract_packet_loss_percentages('packet_loss/uplink_3Mbps_1300bytes_packet_loss.txt')
        data_packetloss_ul_4Mbps = self.extract_packet_loss_percentages('packet_loss/uplink_4Mbps_1300bytes_packet_loss.txt')

        data_throughput_ul_3Mbps = self.extract_all_throughputs('throughput/uplink_3Mbps_1300bytes_throughput.txt')
        data_throughput_ul_4Mbps = self.extract_all_throughputs('throughput/uplink_4Mbps_1300bytes_throughput.txt')

        data_arrivaltime_ul_3Mbps = self.extract_all_inter_arrival_times('inter_arrival_time/uplink_3Mbps_1300bytes_inter_arrival_times.txt')
        data_arrivaltime_ul_4Mbps = self.extract_all_inter_arrival_times('inter_arrival_time/uplink_4Mbps_1300bytes_inter_arrival_times.txt')

        return data_latency_ul_3Mbps, data_latency_ul_4Mbps, data_packetloss_ul_3Mbps, data_packetloss_ul_4Mbps, data_throughput_ul_3Mbps, data_throughput_ul_4Mbps, data_arrivaltime_ul_3Mbps, data_arrivaltime_ul_4Mbps
    
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
                        except ValueError:
                            # Handle the case where conversion to float fails
                            pass

            return all_inter_arrival_times
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return all_inter_arrival_times



   
    '''# Path to the file (adjust as necessary)
        file_path = 'uplink_3Mbps_1300bytes_throughput_50ms.txt'
        average_throughput_values = extract_average_throughput(file_path)
        print(average_throughput_values)

        # Path to the file (adjust as necessary)
        file_path = 'uplink_3Mbps_1300bytes_packet_loss.txt'
        packet_loss_percentages = extract_packet_loss_percentages(file_path)
        print(packet_loss_percentages)

        # Path to the file (adjust as necessary)
        file_path = 'uplink_3Mbps_1300bytes_inter_arrival_times.txt'
        average_times = extract_average_times(file_path)
        print(average_times)

        # Path to the file (adjust as necessary)
        file_path = 'uplink_3Mbps_1300bytes_inter_arrival_times.txt'
        all_inter_arrival_times = extract_all_inter_arrival_times(file_path)
        print(all_inter_arrival_times)

        all_latencies = extract_all_latencies(file_content)
        print(all_latencies)'''
            


      