import tkinter as tk
import pyshark
import os

class Latency_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.latency_view_label = tk.Label(self.frame, text= "Welcome to the Latency view")
        self.latency_view_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.calculate_button = tk.Button(self.frame, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

    '''def find_pcap_pairs(self):
        pairs = []
        files = os.listdir(self.pcaps_dir)
        core_files = [f for f in files if f.startswith('core')]
        ue_files = [f for f in files if f.startswith('ue')]

        for core_file in core_files:
            matching_ue_file = 'ue' + core_file[4:]
            if matching_ue_file in ue_files:
                pairs.append((core_file, matching_ue_file))
        return pairs
        print(pairs)

    #print(find_pcap_pairs('pcaps'))'''


    def extract_iperf_sequence(packet):
        try:
            udp_payload = bytes.fromhex(packet.udp.payload.replace(':', ''))
            if len(udp_payload) >= 24:
                return int.from_bytes(udp_payload[16:24], byteorder='big')
        except AttributeError:
            pass
        return None
    
    def packet_size_is_284(self, packet):
        return int(packet.length) == 284
        '''try:
            # Extraer los bytes 2 y 3 de la cabecera IP y convertirlos a entero
            total_length = int(packet.ip.len)
            return total_length == 284
        except AttributeError:
            return False'''

    def calculate_latency_and_packet_loss(self, sender_pcap_path, receiver_pcap_path):
        sender_cap = pyshark.FileCapture(sender_pcap_path)
        print(f"Sender cap guardada")
        receiver_cap = pyshark.FileCapture(receiver_pcap_path)
        print(f"Receiver cap guardada")

        sender_index = 0
        receiver_index = 0
        lost_packets = 0
        latencies = []

        sender_iter = iter(sender_cap)
        print(f"Sender iter guardado: {sender_iter}")
        receiver_iter = iter(receiver_cap)

        try:
            sender_pkt = next(sender_iter)
            receiver_pkt = next(receiver_iter)
        except StopIteration:
            print("There are no packets to process")
            return 0, 0

        while True:
            try:
                if self.packet_size_is_284(sender_pkt) and self.packet_size_is_284(receiver_pkt):
                    sender_seq = sender_pkt.udp.seq
                    print(f"Sender sequence: {sender_seq}")
                    receiver_seq = receiver_pkt.udp.seq
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
                    if not self.packet_size_is_284(sender_pkt):
                        sender_pkt = next(sender_iter)
                        sender_index += 1
                    if not self.packet_size_is_284(receiver_pkt):
                        receiver_pkt = next(receiver_iter)
                        receiver_index += 1

            except StopIteration:
                print(f"Number of packets sent: {sender_index}, and received: {receiver_index}")
                break  # Salir del bucle cuando se alcanza el final de cualquiera de las capturas

        average_latency = sum(latencies) / len(latencies) if latencies else 0
        packet_loss_percentage = (lost_packets / sender_index) * 100 if sender_index else 0
        print(f"Average Latency: {average_latency} miliseconds, Lost Packets: {lost_packets}, Packet Loss Percentage: {packet_loss_percentage}%")

        with open('latency.txt', 'a') as latency_file:
            latency_file.write('\n'.join(str(latency) for latency in latencies))
            latency_file.write('\n')
            latency_file.write(str(average_latency))

        with open('Packet_loss.txt', 'a') as packet_loss_file:
            packet_loss_file.write(str(lost_packets))

        return average_latency, lost_packets
        
    def calculate(self):
        try:
            print("Calculating...")
            average_latency, lost_packets = self.calculate_latency_and_packet_loss('pcaps/ue_uplink_3Mbps_256bytes_1.pcap', 'pcaps/core_uplink_3Mbps_256bytes_1.pcap')
            print("Calculations done!")
            if average_latency == 0 or lost_packets == 0:
                print("The metrics couldn't be calculated. Please try again.")
            else:
                print("Success!")
        except Exception as e:
            print(f"Error: {e}")


    '''
    def calculate_latency_and_packet_loss(self, sender_pcap_path, receiver_pcap_path):
        sender_cap = pyshark.FileCapture(sender_pcap_path)
        print(f"tamaño de sender cap: {len(sender_cap)}")
        receiver_cap = pyshark.FileCapture(receiver_pcap_path)
        print(f"Receiver cap guardada")

        sender_index = 0
        receiver_index = 0  # Comenzar desde el paquete 1
        lost_packets = 0
        latencies = []

        while sender_index < len(sender_cap) and receiver_index < len(receiver_cap):
                    sender_pkt = sender_cap[sender_index]
                    receiver_pkt = receiver_cap[receiver_index]


                    # Verificar si el paquete cumple con el criterio de tamaño
                    if self.packet_size_is_284(sender_pkt) and self.packet_size_is_284(receiver_pkt):
                        sender_seq = self.extract_iperf_sequence(sender_pkt)
                        receiver_seq = self.extract_iperf_sequence(receiver_pkt)
                        

                        if sender_seq is not None and receiver_seq is not None:
                            if sender_seq == receiver_seq:
                                print(f"Paquete {sender_index} y {receiver_index} coinciden")
                                latency =(float(receiver_pkt.sniff_timestamp) - float(sender_pkt.sniff_timestamp)) * 1000
                                print(f"La latencia del paquete {sender_index} es" + latency)
                                latencies.append(latency)
                                sender_index += 1
                                receiver_index += 1
                            else:
                                lost_packets += 1
                                receiver_index -= 1  # Mantener el índice del receptor para reintentar
                        else:
                            lost_packets += 1
                    
                    # Incrementar los índices solo si el paquete no cumple con el criterio de tamaño
                    if not self.packet_size_is_284(sender_pkt):
                        print(f"El paquete {sender_index} no cumple con el criterio de tamaño")
                        sender_index += 1
                    if not self.packet_size_is_284(receiver_pkt):
                        print(f"El paquete {receiver_index} no cumple con el criterio de tamaño")
                        receiver_index += 1

            
                    print(latencies)
                    average_latency = sum(latencies) / len(latencies) if latencies else 0
                    lost_packet_percentage = (lost_packets / len(latencies)) * 100 if latencies else 0
                    return average_latency, lost_packets
                
            except Exception as e:
                print(f"Error: {e}")
                return 0, 0
            '''
