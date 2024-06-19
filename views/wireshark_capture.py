import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from utils.ssh_connections import SSHConnections
import os

class Wireshark_capture(tk.Frame):

    def __init__(self, root):
        self.root = root

        self.frame = tk.Frame(self.root)
        self.frame.grid()

        # Interfaz de red
        self.entry_label_interface_ue = tk.Label(self.frame, text="UE Interface:") #enp1s0 or tun_srsue
        self.entry_label_interface_ue.grid(row=0, column=0)

        self.entry_interface_ue = tk.Entry(self.frame)
        self.entry_interface_ue.grid(row=0, column=1)

        self.entry_label_interface_core = tk.Label(self.frame, text="Core Interface:") #enp0s31f6 or ogstun
        self.entry_label_interface_core.grid(row=1, column=0)

        self.entry_interface_core = tk.Entry(self.frame)
        self.entry_interface_core.grid(row=1, column=1)


        # Duración de la captura
        self.entry_label_duration = tk.Label(self.frame, text="Duration (seconds):")
        self.entry_label_duration.grid(row=2, column=0)

        self.entry_duration = tk.Entry(self.frame)
        self.entry_duration.grid(row=2, column=1)

        # Botón para iniciar la captura
        self.capture_button = tk.Button(self.frame, text="Begin to capture", command=self.start_capture)
        self.capture_button.grid(row=3, columnspan=2)


    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()
    #UE
    @staticmethod
    def capture_traffic_remote_ue(ssh, interface, capture_file, duration):
        """Captura el tráfico de red usando tshark en el dispositivo remoto."""
        command = f"tshark -i {interface} -w {capture_file} -a duration:{duration}"
        SSHConnections.ssh_ue.execute_command(command)
    
    @staticmethod
    def extract_timestamps_remote_ue(ssh, capture_file, timestamp_file):
        """Extrae los timestamps de los paquetes usando tshark en el dispositivo remoto."""
        command = f"tshark -r {capture_file} -T fields -e frame.time_epoch > {timestamp_file}"
        SSHConnections.ssh_ue.execute_command(command)

    @staticmethod
    def download_file_ue(ssh, remote_path, local_path):
        """Descarga un archivo desde el dispositivo remoto."""
        SSHConnections.ssh_ue.download_file(remote_path, local_path)

    #CORE
    @staticmethod
    def capture_traffic_remote_core(ssh, interface, capture_file, duration):
        """Captura el tráfico de red usando tshark en el dispositivo remoto."""
        command = f"tshark -i {interface} -w {capture_file} -a duration:{duration}"
        SSHConnections.ssh_core.execute_command(command)

    
    @staticmethod
    def extract_timestamps_remote_core(ssh, capture_file, timestamp_file):
        """Extrae los timestamps de los paquetes usando tshark en el dispositivo remoto."""
        command = f"tshark -r {capture_file} -T fields -e frame.time_epoch > {timestamp_file}"
        SSHConnections.ssh_core.execute_command(command)

    @staticmethod
    def download_file_core(ssh, remote_path, local_path):
        """Descarga un archivo desde el dispositivo remoto."""
        SSHConnections.ssh_core.download_file(remote_path, local_path)
    
    @staticmethod
    def calculate_latency(ue_timestamps_file, core_timestamps_file, latency_file):
        """Calcula la latencia a partir de los archivos de timestamps."""
        ue_timestamps = pd.read_csv(ue_timestamps_file, header=None, names=["Timestamp"])
        core_timestamps = pd.read_csv(core_timestamps_file, header=None, names=["Timestamp"])
        latency = core_timestamps["Timestamp"] - ue_timestamps["Timestamp"]
        latency.to_csv(latency_file, index=False, header=["Latency"])
        return latency

    @staticmethod
    def analyze_and_plot(latency):
        print("Latency statistics:")
        print(latency.describe())

        plt.figure(figsize=(10, 5))
        plt.plot(latency, label="Latency")
        plt.xlabel("Number of packets")
        plt.ylabel("Latency (seconds)")
        plt.title("Latency over time")
        plt.legend()
        plt.show()

    def start_capture(self):
        interface_ue = self.entry_interface_ue.get()
        interface_core = self.entry_interface_core.get()
        duration = int(self.entry_duration.get())

        folder_name = "Timestamps"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    
        try:
            # Captura y extracción en UE
            #self.capture_traffic_remote(SSHConnections.ssh_ue, interface_ue, "ue.pcap", duration)
            self.capture_traffic_remote_ue(SSHConnections.ssh_ue, "tun_srsue", "ue.pcap", duration)
            self.extract_timestamps_remote_ue(SSHConnections.ssh_ue, "ue.pcap", "ue_timestamps.txt")
            self.download_file_ue(SSHConnections.ssh_ue, "ue_timestamps.txt", os.path.join(folder_name, "local_ue_timestamps.txt"))

        
            #self.download_file_ue(SSHConnections.ssh_ue, "ue.pcap", "local_ue.pcap")
    
            # Captura y extracción en Core
            #self.capture_traffic_remote(SSHConnections.ssh_core, interface_core, "core.pcap", duration)
            self.capture_traffic_remote_core(SSHConnections.ssh_core, "ogstun", "core.pcap", duration)
            self.extract_timestamps_remote_core(SSHConnections.ssh_core, "core.pcap", "core_timestamps.txt")
            self.download_file_core(SSHConnections.ssh_core, "core_timestamps.txt", os.path.join(folder_name, "local_core_timestamps.txt"))

        
            #self.download_file_core(SSHConnections.ssh_core, "core.pcap", "local_core.pcap")
            
            # Calcular latencia
            latency = self.calculate_latency("local_ue_timestamps.txt", "local_core_timestamps.txt", "latency.txt")
            self.analyze_and_plot(latency)
        
            messagebox.showinfo("Éxito", "Captura y análisis completados")
        except Exception as e:
            messagebox.showerror("Error", str(e))


