import re
import os
import matplotlib.pyplot as plt
import tkinter as tk


class Packet_loss_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        #self.ssh_ue = None

        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.packet_loss_view_label = tk.Label(self.frame, text= "Welcome to the Packet Loss view")
        self.packet_loss_view_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.plot_button = tk.Button(self.frame, text="Plot", command=self.plot_data)
        self.plot_button.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

    def extract_packet_loss_from_folder(self, folder_path):
        packet_loss_pattern = re.compile(r'(\d+)/(\d+) \((\d+(?:\.\d+)?)%\)')
        uplink_packet_loss_percentages = {}
        downlink_packet_loss_percentages = {}

        for filename in os.listdir(folder_path):
            print(f"Checking file: {filename}")
            if filename.endswith('.txt'):
                bit_rate = re.search(r'(\d+)Mbps', filename)
                if bit_rate:
                    bit_rate_value = int(bit_rate.group(1))
                    with open(os.path.join(folder_path, filename), 'r') as file:
                        percentages = []
                        for line in file:
                            if 'receiver' in line:
                                print(f"Found receiver line: {line.strip()}")
                                match = packet_loss_pattern.search(line)
                                if match:
                                    packet_loss_percentage = float(match.group(3))
                                    percentages.append(packet_loss_percentage)
                                    print(f"Extracted packet loss: {packet_loss_percentage}%")
                                    if 'uplink' in filename:
                                        uplink_packet_loss_percentages[bit_rate_value] = percentages
                                    elif 'downlink' in filename:
                                        downlink_packet_loss_percentages[bit_rate_value] = percentages

        return uplink_packet_loss_percentages, downlink_packet_loss_percentages
        

    def plot_packet_loss_data(self, uplink_data, downlink_data):
        plt.figure(figsize=(10, 5))

        # Uplink
        plt.subplot(1, 2, 1)
        for bit_rate, percentages in uplink_data.items():
            for percentage in percentages:
                plt.plot(bit_rate, percentage, marker='o', linestyle='None', color='b')
        #uplink_keys = list(uplink_data.keys())
        #uplink_values = list(uplink_data.values())
        #plt.plot(list(uplink_data.keys()), list(uplink_data.values()), marker='o', linestyle='None', color='b')
        plt.title('Uplink Packet Loss')
        plt.xlabel('Bit Rate (Mbps)')
        plt.ylabel('Packet Loss (%)')
        plt.ylim(-5, 100)
        plt.xlim(0.5, 10.5)
        plt.xticks(list(uplink_data.keys()))
        #plt.xticks([1,2,3,5,10])
        #for i, value in enumerate(uplink_values):
        #   plt.text(uplink_keys[i], max(value, 1), f'{value}%', ha='center', va='bottom')  # Ajusta el 1 para cambiar la altura mínima


        # Downlink
        plt.subplot(1, 2, 2)
        for bit_rate, percentages in downlink_data.items():
            for percentage in percentages:
                plt.plot(bit_rate, percentage, marker='o', linestyle='None', color='r')
        #downlink_keys = list(downlink_data.keys())
        #downlink_values = list(downlink_data.values())
        #plt.plot(list(downlink_data.keys()), list(downlink_data.values()), marker='o', linestyle='None', color='r')
        plt.title('Downlink Packet Loss')
        plt.xlabel('Bit Rate (Mbps)')
        plt.ylabel('Packet Loss (%)')
        plt.ylim(-5, 100)
        plt.xlim(0.5, 10.5)
        plt.xticks(list(downlink_data.keys()))
        #plt.xticks([1,2,3,5,10])
        #for i, value in enumerate(downlink_values):
        #   plt.text(downlink_keys[i], max(value, 1), f'{value}%', ha='center', va='bottom')  # Ajusta el 1 para cambiar la altura mínima


        plt.tight_layout()
        plt.show()

    # Uso de la función
    def plot_data(self):
        folder_path = 'iperf3_outputs'
        uplink_packet_loss_percentage, downlink_packet_loss_percentage = self.extract_packet_loss_from_folder(folder_path)
        print(uplink_packet_loss_percentage)
        print(downlink_packet_loss_percentage)
        self.plot_packet_loss_data(uplink_packet_loss_percentage, downlink_packet_loss_percentage)




