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

        # Botón para iniciar la captura
        self.capture_button = tk.Button(self.frame, text="Begin to capture", command=self.start_capture)
        self.capture_button.grid(row=3, columnspan=2)

        # Botón para parar la captura
        self.stop_button = tk.Button(self.frame, text="Stop capture", command=self.stop_capture)
        self.stop_button.grid(row=4, columnspan=2)


    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

    
    #First we need the necessary permission to capture traffic:
    #sudo apt install tshark
    #sudo dpkg-reconfigure wireshark-common  (select "<YES>")
    #sudo usermod -a -G wireshark laura

    pid_ue = None
    pid_core = None

    
    def capture_traffic_remote_ue(self, ssh, interface, remote_capture_file):
        """Captures the traffic using tshark in the remote ue device."""
        command = f"nohup tshark -i {interface} -w {remote_capture_file} > /dev/null 2>&1 & echo $!"
        stdout = SSHConnections.ssh_ue.execute_command(command)
        pid_ue = stdout.decode('utf-8').strip()
        print(f"tshark on UE started with PID {pid_ue}")
        self.pid_ue = pid_ue
        
            


    def capture_traffic_remote_core(self, ssh, interface, remote_capture_file):
        """Captures the traffic using tshark in the remote core device."""
        command = f"nohup tshark -i {interface} -w {remote_capture_file} > /dev/null 2>&1 & echo $!"
        stdout = SSHConnections.ssh_core.execute_command(command)
        pid_core = stdout.decode('utf-8').strip()
        print(f"tshark on core started with PID {pid_core}")
        self.pid_core = pid_core
        
            

    def start_capture(self):
        interface_ue = self.entry_interface_ue.get()
        interface_core = self.entry_interface_core.get()   
        #interface_gnb = self.entry_interface_gnb.get()   
        try:         
           self.capture_traffic_remote_ue(SSHConnections.ssh_ue, "enp1s0", "ue.pcap")
           self.capture_traffic_remote_core(SSHConnections.ssh_core, "enp0s31f6", "core.pcap")
           #self.capture_traffic_remote_gnb(SSHConnections.ssh_gnb, "??????", "gnb.pcap")
           messagebox.showinfo("Success", "Capture started")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    
    def stop_capture_remote(self,ssh, pid):
        """Stops the traffic capture in the remote device."""
        if pid is None:
            print("No PID found")
            return
        if ssh is SSHConnections.ssh_core:
            command_core = f"kill -9 {pid}"
            SSHConnections.ssh_core.execute_command(command_core)
            print(f"tshark on core with PID {pid} stopped")
        elif ssh is SSHConnections.ssh_ue:
            command_ue = f"kill -9 {pid}"
            SSHConnections.ssh_ue.execute_command(command_ue)
            print(f"tshark on UE with PID {pid} stopped")

    def stop_capture(self):
        try: 
            self.stop_capture_remote(SSHConnections.ssh_ue, self.pid_ue)
            self.stop_capture_remote(SSHConnections.ssh_core, self.pid_core)
            messagebox.showinfo("Success", "Capture stopped")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
           


    @staticmethod
    def download_file_ue(ssh, remote_path, local_path):
        """Descarga un archivo desde el dispositivo remoto."""
        SSHConnections.ssh_ue.download_file(remote_path, local_path)

    @staticmethod
    def download_file_core(ssh, remote_path, local_path):
        """Descarga un archivo desde el dispositivo remoto."""
        SSHConnections.ssh_core.download_file(remote_path, local_path)
    

    def start_capture1(self):
        interface_ue = self.entry_interface_ue.get()
        interface_core = self.entry_interface_core.get()      
    
        #try:
            # Captura y extracción en UE
        self.capture_traffic_remote_ue(SSHConnections.ssh_ue, "enp1s0", "ue.pcap")
        print("Captura de tráfico en UE completada")
        os.chdir(os.path.expanduser("~"))
        if self.check_file_exists_remote_ue(SSHConnections.ssh_ue, "ue.pcap"):
             self.download_file_ue(SSHConnections.ssh_ue, "ue.pcap","local_ue.pcap")
        else:
            print("El archivo ue.pcap no existe en el dispositivo remoto.")
            
        # Captura y extracción en Core
        self.capture_traffic_remote_core(SSHConnections.ssh_core, "enp0s31f6", "core.pcap")
        print("Captura de tráfico en Core completada")
        os.chdir(os.path.expanduser("~"))
        if self.check_file_exists_remote_ue(SSHConnections.ssh_core, "core.pcap"):
             self.download_file_core(SSHConnections.ssh_core, "core.pcap","local_core.pcap")
        else:
            print("El archivo core.pcap no existe en el dispositivo remoto.")
            
            #messagebox.showinfo("Éxito", "Captura y análisis completados")
        #except Exception as e:
         #   messagebox.showerror("Error", str(e))

    
    def check_file_exists_remote_ue(self, ssh, remote_path):
        """Verifica si un archivo existe en el dispositivo remoto."""
        try:
            sftp = SSHConnections.ssh_ue.open_sftp()
            sftp.stat(remote_path)
            sftp.close()
            return True
        except FileNotFoundError:
            return False
        
    def check_file_exists_remote_core(self, ssh, remote_path):
        """Verifica si un archivo existe en el dispositivo remoto."""
        try:
            sftp = SSHConnections.ssh_core.open_sftp()
            sftp.stat(remote_path)
            return True
        except FileNotFoundError:
            return False

