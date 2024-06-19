import tkinter as tk
#import subprocess
#from utils.ssh import SSHClient
#from views.home_view import Home_view
from utils.ssh_connections import SSHConnections

class Latency_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        #self.ssh_ue = None

        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.latency_view_label = tk.Label(self.frame, text= "Welcome to the Latency view")
        self.latency_view_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.entry_label_ping = tk.Label(self.frame, text="Enter the IP address for ping:")
        self.entry_label_ping.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        self.entry_ping = tk.Entry(self.frame)
        self.entry_ping.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")    
        
        self.ping_button = tk.Button(self.frame, text="Ping", command=self.ping_ssh)
        self.ping_button.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")


        self.ping_output = tk.Text(self.frame, height=10, width=50)
        self.ping_output.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")


            
        self.ls_button = tk.Button(self.frame, text="ls", command=self.ls_ssh)
        self.ls_button.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")


        self.ls_output = tk.Text(self.frame, height=10, width=50)
        self.ls_output.grid(row=4, column=1, padx=20, pady=20, sticky="nsew")





    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

    def ping_ssh(self):
        ip_address = self.entry_ping.get() 
        if ip_address:
            ping_command = f"ping -c 4 {ip_address}"
           
            if SSHConnections.ssh_ue is not None:
                output = SSHConnections.ssh_ue.execute_command(ping_command)
                output_str = output.decode('utf-8')
                # Insertar el resultado en el widget de texto
                self.ping_output.insert(tk.END, output_str + "\n")
                self.ping_output.see(tk.END)
            else:
                self.ping_output.insert(tk.END, "SSH UE connection is not established.\n")
                self.ping_output.see(tk.END)
        else:
            # Mensaje de error si no se ha introducido ninguna dirección IP
            self.ping_output.insert(tk.END, "Please enter an IP address.\n")

    def ls_ssh(self):
        if SSHConnections.ssh_ue is not None:
           # Comando de ping para sistemas Unix/Linux. Cambia según el sistema operativo del servidor remoto.
           ls_command = "ls"
           # Ejecutar el comando de ping a través de SSH
           output = SSHConnections.ssh_ue.execute_command(ls_command)
           output_str = output.decode('utf-8')
           # Insertar el resultado en el widget de texto
           self.ls_output.insert(tk.END, output_str + "\n")
           self.ls_output.see(tk.END)
        else:
              self.ls_output.insert(tk.END, "SSH UE connection is not established.\n")
              self.ls_output.see(tk.END)