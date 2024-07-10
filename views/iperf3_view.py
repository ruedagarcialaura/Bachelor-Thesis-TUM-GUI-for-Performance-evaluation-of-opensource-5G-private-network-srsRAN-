import tkinter as tk
from tkinter import messagebox
import os
from utils.ssh_connections import SSHConnections
from tkinter import ttk
import  threading
import datetime

class Iperf3_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        #Acumulator to save the outputs of iperf3
        self.iperf_output_accumulator = ""

        #CATURE TRAFFIC WITH WIRESHARK
        self.capture_traffic_title = tk.Label(self.frame, text="Capture traffic with Wireshark", font=("Helvetica", 16, "bold"), fg="blue")
        self.capture_traffic_title.grid(row=0, column=0, columnspan=10, sticky="ew")
        #Interfaces
        self.entry_label_interface_ue = tk.Label(self.frame, text="UE Interface:")  # enp1s0 or tun_srsue
        self.entry_label_interface_ue.grid(row=1, column=0)
        self.entry_interface_ue = tk.Entry(self.frame)
        self.entry_interface_ue.grid(row=1, column=1)
        self.entry_label_interface_core = tk.Label(self.frame, text="Core Interface:")  # enp0s31f6 or ogstun
        self.entry_label_interface_core.grid(row=1, column=2)
        self.entry_interface_core = tk.Entry(self.frame)
        self.entry_interface_core.grid(row=1, column=4)
        # Start capture button
        self.capture_button = tk.Button(self.frame, text="Begin to capture", command=self.start_capture)
        self.capture_button.grid(row=1, column=5)
        # Stop capture button
        self.stop_button = tk.Button(self.frame, text="Stop capture", command=self.stop_capture_async)
        self.stop_button.grid(row=1, column=6)

        # Horizontal Separator
        self.separator_horizontal = ttk.Separator(self.frame, orient='horizontal')
        self.separator_horizontal.grid(row=3, column=0, columnspan=10, sticky='ew', pady=10)
 

        #IPERF3 TRAFFIC GENERATION
        self.generate_traffic_title = tk.Label(self.frame, text="Generate traffic with iperf3", font=("Helvetica", 16, "bold"), fg="blue")
        self.generate_traffic_title.grid(row=4, column=0, columnspan=10, sticky="ew")
        #Bitrate 
        self.entry_label_bitrate_client = tk.Label(self.frame, text="Sending bit rate in Mbps:")
        self.entry_label_bitrate_client.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")
        bitrate_options = ["3", "4", "5", "10"]
        self.entry_bitrate_client = ttk.Combobox(self.frame, values=bitrate_options)
        self.entry_bitrate_client.grid(row=5, column=1, padx=20, pady=20, sticky="nsew")
        self.entry_bitrate_client.set("10")
        #Iteration
        iterations = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.entry_iteration = ttk.Combobox(self.frame, values=iterations)
        self.entry_iteration.grid(row=5, column=6, padx=20, pady=20, sticky="nsew")
        self.entry_iteration.set("1")
        #Packet size
        self.packet_size_label = tk.Label(self.frame, text="Packet size in bytes:")
        self.packet_size_label.grid(row=5, column=2, padx=20, pady=20, sticky="nsew")
        packet_size_options = ["1300"]
        self.entry_packet_size = ttk.Combobox(self.frame, values=packet_size_options)
        self.entry_packet_size.grid(row=5, column=4, padx=20, pady=20, sticky="nsew")
        self.entry_packet_size.set("1300") 
        #Downlink/Uplink traffic options
        self.reverse_mode_var = tk.IntVar()
        self.reverse_mode_checkbox = tk.Checkbutton(self.frame, text="Downlink Traffic", variable=self.reverse_mode_var, onvalue=1, offvalue=0, width=20)
        self.reverse_mode_checkbox.grid(row=5, column=5, padx=10, pady=20, sticky="ew")

        #2nd Horizontal Separator
        self.separator_horizontal = ttk.Separator(self.frame, orient='horizontal')
        self.separator_horizontal.grid(row=6, column=0, columnspan=10, sticky='ew', pady=10)

        #SERVER SIDE

        #Server IP address
        self.entry_label_iperf_server = tk.Label(self.frame, text="IP address of the server for iperf3:")
        self.entry_label_iperf_server.grid(row=7, column=0, padx=20, pady=20, sticky="nsew", columnspan=1)
        self.entry_ip_server = tk.Entry(self.frame)
        self.entry_ip_server.grid(row=7, column=1, padx=20, pady=20, sticky="nsew", columnspan=2)    
        #start server
        self.iperf_server_button = tk.Button(self.frame, text="Start Server", command=self.iperf3_server_ssh, width=20)
        self.iperf_server_button.grid(row=8, column=0, padx=20, pady=20, sticky="ew")
        #stop server
        self.iperf_server_button = tk.Button(self.frame, text="Stop Server", command=self.stop_iperf3_server, width=20)
        self.iperf_server_button.grid(row=8, column=1, padx=20, pady=20, sticky="ew", columnspan=2)
        #output monitoring for server
        self.iperf_server_output = tk.Text(self.frame, height=13, width=70)
        self.iperf_server_output.grid(row=9, column=0, padx=20, pady=20, sticky="nsew", columnspan=3)

        #Vertical separator
        separator = ttk.Separator(self.frame, orient='vertical')
        separator.grid(row=7, column=3, sticky='ns', rowspan=9, padx=5)  # rowspan ajustable según la altura deseada


        #CLIENT SIDE  

        #Client IP address
        self.entry_label_iperf_client = tk.Label(self.frame, text="IP address of the client:")
        self.entry_label_iperf_client.grid(row=7, column=4, padx=20, pady=20, sticky="nsew")
        self.entry_ip_client = tk.Entry(self.frame)
        self.entry_ip_client.grid(row=7, column=5, padx=20, pady=20, sticky="nsew", columnspan=2)
        #Start iperf3 client
        self.iperf_client_button = tk.Button(self.frame, text="Generate iperf3 traffic", command=self.iperf3_client_ssh, width=20)
        self.iperf_client_button.grid(row=8, column=4, padx=10, pady=20, sticky="ew", columnspan=2)
        #Stop iperf3 client
        self.iperf_stop_client_button = tk.Button(self.frame, text="Stop traffic", command=self.stop_iperf3_client, width=20)
        self.iperf_stop_client_button.grid(row=8, column=6, padx=10, pady=20, sticky="ew")
        #Output monitoring for the client
        self.iperf_client_output = tk.Text(self.frame, height=13, width=70)
        self.iperf_client_output.grid(row=9, column=4, padx=20, pady=20, sticky="nsew", columnspan=3)


        

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()
  

    def handle_output_server(self, line):

        self.iperf_server_output.insert(tk.END, line)
        self.iperf_server_output.see(tk.END)

    def execute_iperf3_server_async(self):
        #ip_address = self.entry_ip_server.get() 
        ip_address = '10.45.0.1'
        if ip_address:
            iperf_server_command = f"iperf3 -s -B {ip_address}"
            try: 
                if SSHConnections.ssh_core is not None:
                   SSHConnections.ssh_core.execute_command_async(iperf_server_command, output_callback=self.handle_output_server)
                else:
                   self.iperf_server_output.insert(tk.END, "SSH core connection is not established.\n")
                   self.iperf_server_output.see(tk.END)
            except Exception as e:
                self.iperf_server_output.insert(tk.END, f"Error: {e}\n")
                self.iperf_server_output.see(tk.END)
        else:
            # Mensaje de error si no se ha introducido ninguna dirección IP
            self.iperf_server_output.insert(tk.END, "Please enter an IP address.\n")

    def iperf3_server_ssh(self):
        # Ejecutar en un hilo separado para evitar bloquear la GUI
        threading.Thread(target=self.execute_iperf3_server_async).start()

    def stop_iperf3_server(self):
        stop_command = "pkill iperf3"  # Este comando detiene todos los procesos de iperf3
        try:
            if SSHConnections.ssh_core is not None:
               SSHConnections.ssh_core.execute_command_async(stop_command)
               self.iperf_server_output.insert(tk.END, "iperf3 server stopped.\n")
            else:
               self.iperf_server_output.insert(tk.END, "SSH Core connection is not established.\n")
        except Exception as e:
           self.iperf_server_output.insert(tk.END, f"Error stopping iperf3 server: {e}\n")

    def handle_output_client(self, line): 
        self.iperf_output_accumulator += line + "\n"
        self.iperf_client_output.insert(tk.END, line)
        self.iperf_client_output.see(tk.END)   
        #self.last_output_time = time.time()
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           

        if "sender" in line or "receiver" in line:
            bit_rate = self.entry_bitrate_client.get()
            direction = "downlink" if self.reverse_mode_var.get() == 1 else "uplink"
            iteration = self.entry_iteration.get()
            packet_size = self.entry_packet_size.get()

            folder_name = "iperf3_outputs"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            
            # Solo guardar el output para uplink desde el lado del cliente
            if direction == "uplink":
                filename = os.path.join(folder_name, f"{direction}_{packet_size}bytes_{bit_rate}Mbps_{iteration}.txt")

                with open(filename, "a") as file:
                    file.write(f"\n{current_datetime}\n")
                    file.write(self.iperf_output_accumulator)
            elif direction == "downlink":
                filename = os.path.join(folder_name, f"{direction}_{bit_rate}Mbps.txt")
                with open(filename, "a") as file:
                    file.write(f"\n{current_datetime}\n")
                    file.write(self.iperf_output_accumulator)
            
            # Reiniciar el acumulador para el próximo test
            self.iperf_output_accumulator = ""
     
    def execute_iperf3_client_async(self):
        ip_address_server = '10.45.0.1'
        #ip_address_server = self.entry_ip_server.get() 
        ip_address = self.entry_ip_client.get()
        bit_rate = self.entry_bitrate_client.get()
        packet_size = self.entry_packet_size.get()
        number_bytes = packet_size * 10000
        number_blocks = 500
        print(f"Packet size: {packet_size}")
        
        downlink_traffic = "-R" if self.reverse_mode_var.get() == 1 else ""
        if ip_address and ip_address_server:
            #iperf_client_command = f"iperf3 -c {ip_address_server} -B {ip_address} -i 1 -M -u -b {bit_rate}M {downlink_traffic}"
            iperf_client_command = f"iperf3 -c {ip_address_server} -B {ip_address} -i 1 -l {packet_size} -k {number_blocks} -u -b {bit_rate}M {downlink_traffic}"
            #iperf_client_command = f"iperf3 -c {ip_address_server} -B {ip_address} -i 1 -l {packet_size} -n {number_bytes} -u -b {bit_rate}M {downlink_traffic}"
            try:
                if SSHConnections.ssh_core is not None:
                   SSHConnections.ssh_ue.execute_command_async(iperf_client_command, output_callback = self.handle_output_client)
                else:
                   self.iperf_client_output.insert(tk.END, "SSH UE connection is not established.\n")
                   self.iperf_client_output.see(tk.END)
            except Exception as e:
                self.iperf_client_output.insert(tk.END, f"Error: {e}\n")
                self.iperf_client_output.see(tk.END)
        else:
            # Mensaje de error si no se ha introducido ninguna dirección IP
            self.iperf_client_output.insert(tk.END, "Please enter an IP address.\n")
            #bit_rate = 10

    def iperf3_client_ssh(self):
        # Ejecutar en un hilo separado para evitar bloquear la GUI
        threading.Thread(target=self.execute_iperf3_client_async).start()

    def stop_iperf3_client(self):
        stop_command = "pkill iperf3"  # Este comando detiene todos los procesos de iperf3
        try:
            if SSHConnections.ssh_ue is not None:
               SSHConnections.ssh_ue.execute_command_async(stop_command)
               self.iperf_client_output.insert(tk.END, "iperf3 client stopped.\n")
            else:
               self.iperf_client_output.insert(tk.END, "SSH UE connection is not established.\n")
        except Exception as e:
           self.iperf_client_output.insert(tk.END, f"Error stopping iperf3 client: {e}\n")

    pid_ue = None
    pid_core = None

    def capture_traffic_remote_ue(self, ssh, interface, remote_capture_file):
        """Captures the traffic using tshark in the remote ue device."""
        interface = "tun_srsue"
        command = f"nohup tshark -i {interface} -w {remote_capture_file} > /dev/null 2>&1 & echo $!"
        stdout = SSHConnections.ssh_ue.execute_command(command)
        pid_ue = stdout.decode('utf-8').strip()
        print(f"tshark on UE started with PID {pid_ue}")
        self.pid_ue = pid_ue
        
            


    def capture_traffic_remote_core(self, ssh, interface, remote_capture_file):
        """Captures the traffic using tshark in the remote core device."""
        interface = "ogstun"
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
           self.capture_traffic_remote_ue(SSHConnections.ssh_ue, interface_ue, "ue.pcap") #"enp1s0"
           self.capture_traffic_remote_core(SSHConnections.ssh_core, interface_core, "core.pcap") #"enp0s31f6"
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
            command_core = f"kill -2 {pid}"
            SSHConnections.ssh_core.execute_command(command_core)
            print(f"tshark on core with PID {pid} stopped")
        elif ssh is SSHConnections.ssh_ue:
            command_ue = f"kill -2 {pid}"
            SSHConnections.ssh_ue.execute_command(command_ue)
            print(f"tshark on UE with PID {pid} stopped")

    def stop_capture(self):
        bit_rate = self.entry_bitrate_client.get()
        direction = "downlink" if self.reverse_mode_var.get() == 1 else "uplink"
        packet_size = self.entry_packet_size.get()
        iteration = self.entry_iteration.get()
        folder_name = "pcaps"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        try: 
            self.stop_capture_remote(SSHConnections.ssh_ue, self.pid_ue)
            self.stop_capture_remote(SSHConnections.ssh_core, self.pid_core)
            messagebox.showinfo("Success", "Capture stopped")

            self.download_file_core(SSHConnections.ssh_core, "core.pcap", os.path.join(folder_name, f"core_{direction}_{bit_rate}Mbps_{packet_size}bytes_{iteration}.pcap"))
            self.download_file_ue(  SSHConnections.ssh_ue,   "ue.pcap",   os.path.join(folder_name, f"ue_{direction}_{bit_rate}Mbps_{packet_size}bytes_{iteration}.pcap"))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_capture_async(self):
        thread = threading.Thread(target=self.stop_capture)
        thread.daemon = True
        thread.start()

    
    def download_file_ue(self, ssh, remote_path, local_path):
        """Descarga un archivo desde el dispositivo remoto."""
        SSHConnections.ssh_ue.download_file(remote_path, local_path)

    
    def download_file_core(self, ssh, remote_path, local_path):
        """Descarga un archivo desde el dispositivo remoto."""
        SSHConnections.ssh_core.download_file(remote_path, local_path)
        
           
