import tkinter as tk
import pyshark
import os
import re
from tkinter import ttk

class Calculations_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.latency_view_label = tk.Label(self.frame, text= "Welcome to the Calculations view")
        self.latency_view_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)      

        self.calculate_button = tk.Button(self.frame, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

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
    
    def packet_size_is_1328(self, packet):
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
       
            
    def calculate_latency_and_packet_loss(self, sender_pcap_path, receiver_pcap_path):

        filtered_receiver_cap = self.filter_receiver_pcap_corrupt_packets(receiver_pcap_path)
        filtered_sender_cap = self.filter_sender_pcap_corrupt_packets(sender_pcap_path)


        sender_index = 0
        receiver_index = 0
        lost_packets = 0
        latencies = []

        sender_iter = iter(filtered_sender_cap)
        print(f"Sender iter guardado: {sender_iter}")
        receiver_iter = iter(filtered_receiver_cap)
        print(f"Receiver iter guardado: {receiver_iter}")

        try:
            print("Trying to get the first packets")
            sender_pkt = next(sender_iter)
            print(f"Sender packet guardado: {sender_pkt}")
            print(f"Sender packet length: {sender_pkt.length}")
            receiver_pkt = next(receiver_iter)
            print(f"Receiver packet guardado: {receiver_pkt}")
            print(f"Receiver packet length: {receiver_pkt.length}")
        except StopIteration:
            print("There are no packets to process")
            return 0, 0
        


        while True:
            try:
                print("Trying to get the next packets")
                if sender_index <= 10015:
                    if self.packet_size_is_1328(sender_pkt) and self.packet_size_is_1328(receiver_pkt):
                        print(f"Packets have the correct size: {sender_pkt.length}, {receiver_pkt.length}")
                        #print(f"Sender packet guardado: {sender_pkt}")
                        #print(f"Receiver packet guardado: {receiver_pkt}")
                        sender_port = int(sender_pkt[sender_pkt.transport_layer].dstport)
                        receiver_port = int(receiver_pkt[receiver_pkt.transport_layer].dstport)
                        # Verifica si alguno de los paquetes usa el puerto 5201
                        if (sender_port == 5201 or receiver_port == 5201):
                            print("Packets are using iperf3 port")
                        # Aquí asumimos que quieres usar el timestamp y secuencia de UDP, ajusta según sea necesario
                        if 'UDP' in sender_pkt and 'UDP' in receiver_pkt:
                            print("Packets are using UDP")
                            
                            #sender_seq = sender_pkt.udp.seq
                            #print(f"Sender sequence: {sender_seq}")
                            # Asumiendo que tienes un objeto de paquete llamado 'pkt' que representa el paquete IPERF3
                            sender_seq = sender_pkt['IPERF3'].get_field_by_showname('iPerf3 sequence')
                            print(f"iPerf3 sequence number: {sender_seq}")
                            receiver_seq = receiver_pkt['IPERF3'].get_field_by_showname('iPerf3 sequence')
                            print(f"Receiver sequence: {receiver_seq}")

                            if sender_seq == receiver_seq:
                                print(f"Packets {sender_index} and {receiver_index} match")
                                latency = (float(receiver_pkt.sniff_timestamp) - float(sender_pkt.sniff_timestamp)) * 1000
                                latencies.append(latency)
                                sender_pkt = next(sender_iter)
                                receiver_pkt = next(receiver_iter)
                                sender_index += 1
                                receiver_index += 1
                            else:
                                lost_packets += 1
                                sender_pkt = next(sender_iter)
                                sender_index += 1
                    else:
                        print("Packets don't have the correct size")
                        print(f"Sender packet length: {sender_pkt.length}, Receiver packet length: {receiver_pkt.length}")
                        if not self.packet_size_is_1328(sender_pkt):
                            sender_pkt = next(sender_iter)
                            sender_index += 1
                        if not self.packet_size_is_1328(receiver_pkt):
                            receiver_pkt = next(receiver_iter)
                            receiver_index += 1
                else:
                    print("10000 packets have been processed")
                    break

            except StopIteration:
                print("There are no more packets to process")
                print(f"Number of packets sent: {sender_index}, and received: {receiver_index}")
                break  # Salir del bucle cuando se alcanza el final de cualquiera de las capturas
        #if sender_index != receiver_index:
         #   lost_packets += abs(sender_index - receiver_index)
    


        average_latency = sum(latencies) / len(latencies) if latencies else 0
        packet_loss_percentage = (lost_packets / sender_index) * 100 if sender_index else 0
        print(f"Average Latency: {average_latency} miliseconds, Lost Packets: {lost_packets}, Packet Loss Percentage: {packet_loss_percentage}%")

 
        file_name = os.path.basename(sender_pcap_path)
        if file_name.startswith("ue_") or file_name.startswith("core_"):
            file_name = file_name.split("_", 1)[1]
        base_file_name = re.sub(r'_\d+\.pcap$', '', file_name)
        latency_file_name = f"{base_file_name}_latencies.txt"

        folder_name = "latencies"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        latency_file_path = os.path.join(folder_name, latency_file_name)

        with open(latency_file_path, 'a') as latency_file:
            latency_file.write(f"Latencies for {file_name}\n")
            latency_file.write('\n'.join(str(latency) for latency in latencies))
            latency_file.write('\n')
            latency_file.write('\n')
            latency_file.write(f"The average latency is: {average_latency} milliseconds\n")



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
            packet_loss_file.write(f"The number of lost packets is: {lost_packets}\n")
            packet_loss_file.write(f"The packet loss percentage is: {packet_loss_percentage}%\n")

        return average_latency, lost_packets
        
    def calculate(self):
        try:
            print("Calculating...")
            average_latency, lost_packets = self.calculate_latency_and_packet_loss('pcaps/core_downlink_10Mbps_1300bytes_2.pcap', 'pcaps/ue_downlink_10Mbps_1300bytes_2.pcap')
            print("Calculations done!")
            if average_latency == 0:
                print("The metrics couldn't be calculated. Please try again.")
            else:
                print("Success!")
        except Exception as e:
            print(f"Error: {e}")