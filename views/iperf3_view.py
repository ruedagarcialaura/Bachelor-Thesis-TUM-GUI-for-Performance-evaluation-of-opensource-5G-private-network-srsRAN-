import tkinter as tk
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
        
        '''#Output monitoring for when UE gets disconnected
        self.last_output_time = None
        self.monitor_thread = threading.Thread(target=self.monitor_output_activity)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()'''

        #Title of the view
        self.iperf3_view_label = tk.Label(self.frame, text= "Here you can generate traffic on the network using iperf3. \nPlease enter the IP address of the server and the client to start the test. \nYou can also select the sending bit rate in Mbps. \nPlease note that the server must be started first. \nStop the server by clicking the button below when you finish generating traffic. \n")
        self.iperf3_view_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=6)
        
        #SERVER SIDE

        #Server IP address
        self.entry_label_iperf_server = tk.Label(self.frame, text="Enter the IP address of the server for iperf3:")
        self.entry_label_iperf_server.grid(row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)
        self.entry_ip_server = tk.Entry(self.frame)
        self.entry_ip_server.grid(row=2, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)    
        
        #start server
        self.iperf_server_button = tk.Button(self.frame, text="Start Server", command=self.iperf3_server_ssh, width=20)
        self.iperf_server_button.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
       
        #stop server
        self.iperf_server_button = tk.Button(self.frame, text="Stop Server", command=self.stop_iperf3_server, width=20)
        self.iperf_server_button.grid(row=3, column=1, padx=20, pady=20, sticky="ew")


        #output monitoring for server
        self.iperf_server_output = tk.Text(self.frame, height=15, width=70)
        self.iperf_server_output.grid(row=4, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)





        #Vertical separator
        separator = ttk.Separator(self.frame, orient='vertical')
        separator.grid(row=1, column=2, sticky='ns', rowspan=10, padx=5)  # rowspan ajustable según la altura deseada


        #CLIENT SIDE  

        #Client IP address
        self.entry_label_iperf_client = tk.Label(self.frame, text="Enter the IP address of the client for iperf3:")
        self.entry_label_iperf_client.grid(row=1, column=3, padx=20, pady=20, sticky="nsew")
        self.entry_ip_client = tk.Entry(self.frame)
        self.entry_ip_client.grid(row=1, column=4, padx=20, pady=20, sticky="nsew")

        #Bitrate options
        self.entry_label_bitrate_client = tk.Label(self.frame, text="Enter the sending bit rate in Mbps:")
        self.entry_label_bitrate_client.grid(row=2, column=3, padx=20, pady=20, sticky="nsew")
        bitrate_options = ["1", "2", "3", "5", "10"]
        self.entry_bitrate_client = ttk.Combobox(self.frame, values=bitrate_options)
        self.entry_bitrate_client.grid(row=2, column=4, padx=20, pady=20, sticky="nsew")
        self.entry_bitrate_client.set("10")
 
        #Downlink/Uplink traffic options
        self.reverse_mode_var = tk.IntVar()
        self.reverse_mode_checkbox = tk.Checkbutton(self.frame, text="Downlink Traffic", variable=self.reverse_mode_var, onvalue=1, offvalue=0, width=20)
        self.reverse_mode_checkbox.grid(row=3, column=5, padx=10, pady=20, sticky="ew")

        #Start iperf3 client
        self.iperf_client_button = tk.Button(self.frame, text="Generate iperf3 traffic", command=self.iperf3_client_ssh, width=20)
        self.iperf_client_button.grid(row=3, column=3, padx=10, pady=20, sticky="ew")

        #Stop iperf3 client
        self.iperf_client_button = tk.Button(self.frame, text="Stop traffic", command=self.stop_iperf3_client, width=20)
        self.iperf_client_button.grid(row=3, column=4, padx=10, pady=20, sticky="ew")

        

        #Output monitoring for the client
        self.iperf_client_output = tk.Text(self.frame, height=15, width=70)
        self.iperf_client_output.grid(row=4, column=3, padx=20, pady=20, sticky="nsew", columnspan=3)

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
                   #output = SSHConnections.ssh_core.execute_command(iperf_server_command)
                   #output_str = output.decode('utf-8')
                   #Insertar el resultado en el widget de texto
                   #self.iperf_server_output.insert(tk.END, "Server listening on port lalala")
                   #self.iperf_server_output.insert(tk.END, output_str + "\n")
                   #self.iperf_server_output.see(tk.END)
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

            folder_name = "iperf3_outputs"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            
            # Solo guardar el output para uplink desde el lado del cliente
            if direction == "uplink":
                filename = os.path.join(folder_name, f"{direction}_{bit_rate}Mbps.txt")

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

    '''def monitor_output_activity(self):
       while True:
            time.sleep(5)  # Verificar la actividad cada 5 segundos
            if self.last_output_time and (time.time() - self.last_output_time > 10):  # 10 segundos de inactividad
                self.stop_iperf_processes()
                self.show_error_message("UE disconnected from RAN Network.")
                break

    def stop_iperf_processes(self):
        self.stop_iperf3_client()
        self.stop_iperf3_server()

    def show_error_message(self, message):
        tk.messagebox.showerror("Error", message)'''        

    def execute_iperf3_client_async(self):
        ip_address_server = '10.45.0.1'
        #ip_address_server = self.entry_ip_server.get() 
        ip_address = self.entry_ip_client.get()
        bit_rate = self.entry_bitrate_client.get()
        #bit_rate = '10'
        downlink_traffic = "-R" if self.reverse_mode_var.get() == 1 else ""
        if ip_address and ip_address_server:
            iperf_client_command = f"iperf3 -c {ip_address_server} -B {ip_address} -i 1 -t 20 -u -b {bit_rate}M {downlink_traffic}"
            try:
                if SSHConnections.ssh_core is not None:
                   SSHConnections.ssh_ue.execute_command_async(iperf_client_command, output_callback = self.handle_output_client)
                   #output_str = output.decode('utf-8')
                   # Insertar el resultado en el widget de texto
                   #self.iperf_client_output.insert(tk.END, output_str + "\n")
                   #self.iperf_client_output.see(tk.END)
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


  
