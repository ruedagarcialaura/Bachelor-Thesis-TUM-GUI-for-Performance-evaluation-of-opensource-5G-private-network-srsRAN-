import tkinter as tk
import pyshark
import os
import re
from tkinter import ttk
from tkinter import messagebox

class Calculations_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.latency_view_label = tk.Label(self.frame, text= "Obtain Latency, Throughput, Packet Loss and Inter Arrival Time average values of your captured traffic", font=("Helvetica", 16, "bold"), fg="blue")
        self.latency_view_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=6)      

        #Bitrate options
        self.entry_label_bitrate_client = tk.Label(self.frame, text="Enter the bit rate in Mbps:")
        self.entry_label_bitrate_client.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        bitrate_options = ["3", "4", "5", "10"]
        self.entry_bitrate_client = ttk.Combobox(self.frame, values=bitrate_options)
        self.entry_bitrate_client.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.entry_bitrate_client.set("10")

        #Direction options
        self.entry_label_direction = tk.Label(self.frame, text="Enter the direction of the traffic:")
        self.entry_label_direction.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        direction_options = ["uplink", "downlink"]  
        self.entry_direction = ttk.Combobox(self.frame, values=direction_options)
        self.entry_direction.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
        self.entry_direction.set("uplink")

        #packet size options
        self.entry_label_packet_size = tk.Label(self.frame, text="Enter the packet size in bytes:")
        self.entry_label_packet_size.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        packet_size_values = ["256","1000","1300"]
        self.entry_packet_size = ttk.Combobox(self.frame, values= packet_size_values)
        self.entry_packet_size.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")
        self.entry_packet_size.set("1300")
         
        #Iteration options
        self.entry_label_iteration = tk.Label(self.frame, text="Enter the iteration number: ")
        self.entry_label_iteration.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
        iterations = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.entry_iteration = ttk.Combobox(self.frame, values=iterations)
        self.entry_iteration.grid(row=4, column=1, padx=20, pady=20, sticky="nsew")
        self.entry_iteration.set("1")

        self.calculate_button = tk.Button(self.frame, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=5, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        #Vertical separator
        self.separator = ttk.Separator(self.frame, orient="vertical")
        self.separator.grid(row=1, column=2, rowspan=6, sticky="ns", padx=20, pady=20)


        #Latency, packet loss, throughput and inter arrival time Results
        self.text_label_latency = tk.Label(self.frame, text="Latency (ms) ")
        self.text_label_latency.grid(row=1, column=3, padx=20, pady=20, sticky="nsew")

        self.input_latency = tk.Text(self.frame, height=1, width=10)
        self.input_latency.grid(row=1, column=4, padx=20, pady=20, sticky="nsew")

        self.text_label_packet_loss = tk.Label(self.frame, text="Packet Loss (%) ")
        self.text_label_packet_loss.grid(row=2, column=3, padx=20, pady=20, sticky="nsew")

        self.input_packet_loss = tk.Text(self.frame, height=1, width=10)
        self.input_packet_loss.grid(row=2, column=4, padx=20, pady=20, sticky="nsew")

        self.text_label_throughput = tk.Label(self.frame, text="Throughput (Mbps) ")
        self.text_label_throughput.grid(row=3, column=3, padx=20, pady=20, sticky="nsew")

        self.input_throughput = tk.Text(self.frame, height=1, width=10)
        self.input_throughput.grid(row=3, column=4, padx=20, pady=20, sticky="nsew")

        self.text_label_inter_arrival_time = tk.Label(self.frame, text="Inter Arrival Time (ms) ")
        self.text_label_inter_arrival_time.grid(row=4, column=3, padx=20, pady=20, sticky="nsew")

        self.input_inter_arrival_time = tk.Text(self.frame, height=1, width=10)    
        self.input_inter_arrival_time.grid(row=4, column=4, padx=20, pady=20, sticky="nsew")

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()


    def extract_iperf_sequence(packet):
        try:
            udp_payload = bytes.fromhex(packet.udp.payload.replace(':', ''))
            if len(udp_payload) >= 24:
                return int.from_bytes(udp_payload[16:24], byteorder='big')
        except AttributeError:
            pass
        return None
    
    def packet_size_matches(self, packet):
        packet_size = self.entry_packet_size.get()
        if packet_size == "256":
            #The packets sent have a payload of 256 bytes, but the total length is 284 bytes
            return int(packet.length) == 284
        elif packet_size == "1000":
            #The packets sent have a payload of 1000 bytes, but the total length is 1028 bytes
            return int(packet.length) == 1028
        elif packet_size == "1300":
            #The packets sent have a payload of 1300 bytes, but the total length is 1328 bytes
            return int(packet.length) == 1328
    
    def filter_sender_pcap_corrupt_packets(self, sender_pcap_path):
         
        dir_name, file_name = os.path.split(sender_pcap_path)
        parent_dir = os.path.dirname(dir_name)
        filtered_dir_path = os.path.join(parent_dir, "pcaps_filtered")
        os.makedirs(filtered_dir_path, exist_ok=True)
        sender_pcap_path_filtered = os.path.join(filtered_dir_path, file_name)
        tshark_command_sender = f'tshark -r {sender_pcap_path} -Y "frame.len >= 60" -w {sender_pcap_path_filtered}'
        os.system(tshark_command_sender)
        sender_cap_filtered = pyshark.FileCapture(sender_pcap_path_filtered)
        return sender_cap_filtered
    
    def filter_receiver_pcap_corrupt_packets(self, receiver_pcap_path):

        dir_name, file_name = os.path.split(receiver_pcap_path)
        parent_dir = os.path.dirname(dir_name)
        filtered_dir_path = os.path.join(parent_dir, "pcaps_filtered")
        os.makedirs(filtered_dir_path, exist_ok=True)
        receiver_pcap_path_filtered = os.path.join(filtered_dir_path, file_name)
        tshark_command_receiver = f'tshark -r {receiver_pcap_path} -Y "frame.len >= 60" -w {receiver_pcap_path_filtered}'
        os.system(tshark_command_receiver)
        filtered_receiver_cap = pyshark.FileCapture(receiver_pcap_path_filtered)
        return filtered_receiver_cap
                

    def get_metric_values(self, sender_pcap_path, receiver_pcap_path):

        filtered_receiver_cap = self.filter_receiver_pcap_corrupt_packets(receiver_pcap_path)
        filtered_sender_cap = self.filter_sender_pcap_corrupt_packets(sender_pcap_path)


        sender_index = 0
        receiver_index = 0
        lost_packets = 0
        latencies = []
        arrival_times= []
        inter_arrival_times = []
        time_slot_tx_start = None
        bytes_sent = 0
        remaining_bytes = 0
        throughput_tx_per_second = []
        
        

        sender_iter = iter(filtered_sender_cap)
        #print(f"Sender iter saved: {sender_iter}")
        receiver_iter = iter(filtered_receiver_cap)
        #print(f"Receiver iter saved: {receiver_iter}")

        try:
            print("Trying to get the first packets")
            sender_pkt = next(sender_iter)
            print(f"Sender packet saved: {sender_pkt}")
            print(f"Sender packet length: {sender_pkt.length}")
            receiver_pkt = next(receiver_iter)
            print(f"Receiver packet saved: {receiver_pkt}")
            print(f"Receiver packet length: {receiver_pkt.length}")
        except StopIteration:
            print("There are no packets to process")
            return 0, 0
        


        while True:
            try:
                print("Trying to get the next packets")
                #The first 15 packages correspond to the initial TCP connection:  handshake
                if sender_index <= 10015:
                    if self.packet_size_matches(sender_pkt) and self.packet_size_matches(receiver_pkt):
                        print(f"Packets have the correct size: {sender_pkt.length}, {receiver_pkt.length}")
                        sender_port = int(sender_pkt[sender_pkt.transport_layer].dstport)
                        receiver_port = int(receiver_pkt[receiver_pkt.transport_layer].dstport)
                        if (sender_port == 5201 or receiver_port == 5201):
                            print("Packets are using iperf3 port 5201")
                        if 'UDP' in sender_pkt and 'UDP' in receiver_pkt:
                            print("Packets are using UDP")
                            sender_seq = sender_pkt['IPERF3'].get_field_by_showname('iPerf3 sequence')
                            print(f"Sender sequence: {sender_seq}")
                            receiver_seq = receiver_pkt['IPERF3'].get_field_by_showname('iPerf3 sequence')
                            print(f"Receiver sequence: {receiver_seq}")

                            #sending throughput calculation
                            if not time_slot_tx_start:
                                time_slot_tx_start = float(sender_pkt.sniff_timestamp)
                            time_diff_sec_tx = (float(sender_pkt.sniff_timestamp) - time_slot_tx_start) * 1000 #in milliseconds

                            if (time_diff_sec_tx) >= 10: #miliseconds
                                throughput_tx = ((bytes_sent * 8) / (time_diff_sec_tx / 1000)) / 1000000
                                throughput_tx_per_second.append(throughput_tx)
                                time_slot_tx_start = float(sender_pkt.sniff_timestamp)
                                bytes_sent = 0
                            

                            packet_length = int(sender_pkt.length)
                            if time_diff_sec_tx < 10:
                                if remaining_bytes > 0:
                                    bytes_sent += remaining_bytes
                                    remaining_bytes = 0
                                else:
                                    bytes_sent += packet_length
                            else:
                                remaining_bytes = packet_length - (time_diff_sec_tx - 10) * (packet_length / time_diff_sec_tx)
                                bytes_sent += packet_length - remaining_bytes

                            if sender_seq == receiver_seq:
                                print(f"Packets {sender_index} and {receiver_index} match")

                                #latency calculation
                                latency = (float(receiver_pkt.sniff_timestamp) - float(sender_pkt.sniff_timestamp)) * 1000
                                latencies.append(latency)

                                #inter arrival time calculation
                                arrival_times.append(receiver_pkt.sniff_timestamp)
                                sender_pkt = next(sender_iter)
                                receiver_pkt = next(receiver_iter)
                                sender_index += 1
                                receiver_index += 1
                            else:
                                #lost packets calculation
                                lost_packets += 1
                                sender_pkt = next(sender_iter)
                                sender_index += 1
                    else:
                        print(f"Packets don't have the correct size: {sender_pkt.length}, {receiver_pkt.length}")
                        if not self.packet_size_matches(sender_pkt):
                            sender_pkt = next(sender_iter)
                            sender_index += 1
                        if not self.packet_size_matches(receiver_pkt):
                            receiver_pkt = next(receiver_iter)
                            receiver_index += 1
                else:
                    print("10000 packets have been processed. Done!")
                    break
                    

            except StopIteration:
                print("There are no more packets to process")
                print(f"Number of packets sent: {sender_index}, and received: {receiver_index}")
                break  # Salir del bucle cuando se alcanza el final de cualquiera de las capturas 

        #Latency
        average_latency = round(sum(latencies) / len(latencies), 4) if latencies else None 
        copy_average_latency = average_latency
        if latencies:
            squared_diffs = [(x - copy_average_latency) ** 2 for x in latencies]
            variance = sum(squared_diffs) / len(latencies)
            standard_deviation = round(variance ** 0.5, 4)
        else:
            variance = None
            standard_deviation = None
        print("latency done")
        

        #Packet Loss
        packet_loss_percentage = round((lost_packets / sender_index) * 100, 4) if sender_index else None
        print("packet loss done")


        #Throughput
        average_throughput_tx = round(sum(throughput_tx_per_second) / len(throughput_tx_per_second), 4) if throughput_tx_per_second else None
        if throughput_tx_per_second:
            squared_diffs = [(x - average_throughput_tx) ** 2 for x in throughput_tx_per_second]
            variance_tp = sum(squared_diffs) / len(throughput_tx_per_second)
            standard_deviation_tp = round(variance_tp ** 0.5, 4)
        else:
            variance_tp = None
            standard_deviation_tp = None
        print("throughput done")


        #Inter arrival time
        for t in range(1, len(arrival_times)):
            inter_arrival_time = (float(arrival_times[t]) - float(arrival_times[t-1])) * 1000
            inter_arrival_times.append(inter_arrival_time)
        inter_arrival_time_average = round(sum(inter_arrival_times) / len(inter_arrival_times), 4) if inter_arrival_times else None
        arrival_times = []

        if inter_arrival_times:
            squared_diffs = [(x - inter_arrival_time_average) ** 2 for x in inter_arrival_times]
            variance_iat = sum(squared_diffs) / len(inter_arrival_times)
            standard_deviation_iat = round(variance_iat ** 0.5, 4)
        print("inter arrival time done")

        #Save values in files for future plotting
        self.save_latency_values(sender_pcap_path, latencies, average_latency, standard_deviation)
        print(f"Latencies saved in file")
        self.save_packet_loss_value(sender_pcap_path, lost_packets, packet_loss_percentage, sender_index, receiver_index)
        print(f"Packet loss saved in file")
        self.save_throughput_tx_values(sender_pcap_path, throughput_tx_per_second, average_throughput_tx, standard_deviation_tp)
        print(f"Sending Throughput saved in file")
        self.save_inter_arrival_time_values(sender_pcap_path, inter_arrival_times, inter_arrival_time_average, standard_deviation_iat)
        print(f"Inter arrival times saved in file")

        #Stdout
        print(f"Average Latency: {average_latency} miliseconds, Standard deviation: {standard_deviation}  Lost Packets: {lost_packets}, Packet Loss Percentage: {packet_loss_percentage}%")
        print(f"Average inter arrival time: {inter_arrival_time_average} and its standard deviation: {standard_deviation_iat}, Average Sending Throughput: {average_throughput_tx} Mbps and its standard deviation: {standard_deviation_tp} Mbps")

        return average_latency, packet_loss_percentage, average_throughput_tx, inter_arrival_time_average
                
    def calculate(self):
        entry_bitrate_client = self.entry_bitrate_client.get()
        entry_direction = self.entry_direction.get()
        entry_iteration = self.entry_iteration.get()
        entry_packet_size = self.entry_packet_size.get()

        # Clear the text fields
        self.input_latency.delete('1.0', tk.END)
        self.input_packet_loss.delete('1.0', tk.END)
        self.input_throughput.delete('1.0', tk.END)
        self.input_inter_arrival_time.delete('1.0', tk.END)

        sender_base = "core" if entry_direction == "downlink" else "ue"
        receiver_base = "ue" if entry_direction == "downlink" else "core"
        
        sender_pcap_path = f"pcaps/{sender_base}_{entry_direction}_{entry_bitrate_client}Mbps_{entry_packet_size}bytes_{entry_iteration}.pcap"
        receiver_pcap_path = f"pcaps/{receiver_base}_{entry_direction}_{entry_bitrate_client}Mbps_{entry_packet_size}bytes_{entry_iteration}.pcap"   

        messagebox.showinfo("Calculating", "Results are on the way. Wait.")
    
        try:
            print("Calculating...")
            average_latency, packet_loss_percentage, average_throughput_tx, inter_arrival_time_average = self.get_metric_values(sender_pcap_path, receiver_pcap_path)
            if sender_pcap_path == None or receiver_pcap_path == None:
                messagebox.showerror("Error", "The pcap files couldn't be found. Please try again.")
            elif average_latency == None:
                messagebox.showerror("Error", "The metrics couldn't be calculated. Please try again.")
                self.input_latency.insert(tk.END, 0)
                self.input_latency.see(tk.END)
                self.input_packet_loss.insert(tk.END, 0)
                self.input_packet_loss.see(tk.END)
                self.input_throughput.insert(tk.END, 0)
                self.input_throughput.see(tk.END)
                self.input_inter_arrival_time.insert(tk.END, 0)
                self.input_inter_arrival_time.see(tk.END)
                
            else:
                print("Success!")
                self.input_latency.insert(tk.END, average_latency)
                self.input_latency.see(tk.END)
                self.input_packet_loss.insert(tk.END, packet_loss_percentage)
                self.input_packet_loss.see(tk.END)
                self.input_throughput.insert(tk.END, average_throughput_tx)
                self.input_throughput.see(tk.END)
                self.input_inter_arrival_time.insert(tk.END, inter_arrival_time_average)
                self.input_inter_arrival_time.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")


    def save_latency_values(self, sender_pcap_path, latencies, average_latency, standard_deviation):
        file_name = os.path.basename(sender_pcap_path)
        if file_name.startswith("ue_") or file_name.startswith("core_"):
            file_name = file_name.split("_", 1)[1]
        base_file_name = re.sub(r'\.pcap$', '', file_name)
        latency_file_name = f"{base_file_name}_latencies.txt"

        folder_name = "latencies"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        latency_file_path = os.path.join(folder_name, latency_file_name)

        with open(latency_file_path, 'w') as latency_file:
            latency_file.write(f"Latencies for {file_name}\n")
            latency_file.write('\n'.join(str(latency) for latency in latencies))
            latency_file.write('\n')
            latency_file.write('\n')
            latency_file.write(f"The average latency is: {average_latency} milliseconds\n")
            latency_file.write(f"The standard deviation is: {standard_deviation}miliseconds\n")
            latency_file.write('\n')

    def save_packet_loss_value(self, sender_pcap_path, lost_packets, packet_loss_percentage, sender_index, receiver_index):
        file_name = os.path.basename(sender_pcap_path)
        if file_name.startswith("ue_") or file_name.startswith("core_"):
            file_name = file_name.split("_", 1)[1]
        base_file_name = re.sub(r'_\d+\.pcap$', '', file_name)
        packet_loss_file_name = f"{base_file_name}_packet_loss.txt"

        folder_name = "packet_loss"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        packet_loss_file_path = os.path.join(folder_name, packet_loss_file_name)

        with open(packet_loss_file_path, 'a') as packet_loss_file:
            packet_loss_file.write(f"Packet loss for {file_name}\n")
            packet_loss_file.write(f"The number of packets received out of {sender_index} packets sent is {receiver_index} \n")
            packet_loss_file.write(f"The number of lost packets is: {lost_packets} and this corresponds to {packet_loss_percentage}%\n")
            packet_loss_file.write('\n')

    def save_throughput_tx_values(self, sender_pcap_path, throughput_tx_per_second, average_throughput_tx, standard_deviation_tp):
        
        file_name = os.path.basename(sender_pcap_path)
        if file_name.startswith("ue_") or file_name.startswith("core_"):
            file_name = file_name.split("_", 1)[1]
        base_file_name = re.sub(r'\.pcap$', '', file_name)
        throughput_file_name = f"{base_file_name}_throughput.txt"

        folder_name = "throughput"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        throughput_file_path = os.path.join(folder_name, throughput_file_name)

        with open(throughput_file_path, 'w') as throughput_file:
            throughput_file.write(f"Sending Throughput for {file_name}\n")
            throughput_file.write('\n'.join(str(throughput) for throughput in throughput_tx_per_second))
            throughput_file.write('\n')
            throughput_file.write('\n')
            throughput_file.write(f"The average throughput is: {average_throughput_tx} Mbps\n")
            throughput_file.write(f"The standard deviation is: {standard_deviation_tp} Mbps\n")
            throughput_file.write('\n')

    def save_inter_arrival_time_values(self, sender_pcap_path, inter_arrival_times, inter_arrival_time_average, inter_arrival_time_standard_deviation):
        
        file_name = os.path.basename(sender_pcap_path)
        if file_name.startswith("ue_") or file_name.startswith("core_"):
            file_name = file_name.split("_", 1)[1]
        base_file_name = re.sub(r'\.pcap$', '', file_name)
        inter_arrival_time_file_name = f"{base_file_name}_inter_arrival_times.txt"

        folder_name = "inter_arrival_time"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        inter_arrival_time_file_path = os.path.join(folder_name, inter_arrival_time_file_name)

        with open(inter_arrival_time_file_path, 'w') as inter_arrival_time_file:
            inter_arrival_time_file.write(f"Inter arrival times for {file_name}\n")
            inter_arrival_time_file.write('\n'.join(str(inter_arrival_time) for inter_arrival_time in inter_arrival_times))
            inter_arrival_time_file.write('\n')
            inter_arrival_time_file.write('\n')
            inter_arrival_time_file.write(f"The average inter arrival time is: {inter_arrival_time_average} milliseconds\n")
            inter_arrival_time_file.write(f"The standard deviation is: {inter_arrival_time_standard_deviation} milliseconds\n")
            inter_arrival_time_file.write('\n')

        