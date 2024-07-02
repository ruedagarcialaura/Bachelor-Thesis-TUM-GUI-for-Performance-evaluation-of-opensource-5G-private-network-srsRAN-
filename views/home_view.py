import tkinter as tk
import json
import paramiko
from utils.ssh import SSHClient
from utils.ssh_connections import SSHConnections
import json

class Home_view(tk.Frame):
    def __init__(self, root):
        self.root = root

        self.frame = tk.Frame(self.root)
        self.frame.grid()

        #self.load_data()

        self.home_view_label = tk.Label(self.frame, text= "Connect to your 5G RAN network via SSH",font=("Helvetica", 16, "bold"), fg="blue")
        self.home_view_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=3)

        #username ubuntu
        self.label_user = tk.Label(self.frame, text="Username:")
        self.label_user.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        self.entry_user = tk.Entry(self.frame)
        self.entry_user.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")  

        #labels
        self.label_ipv4 = tk.Label(self.frame, text="Computer's private IPv4 address:")
        self.label_ipv4.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

        self.label_password = tk.Label(self.frame, text="User password:")
        self.label_password.grid(row=2, column=2, padx=20, pady=20, sticky="nsew")


        
        #UE
        self.label_ue = tk.Label(self.frame, text="User Equipment:")
        self.label_ue.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        
        self.entry_ue_ipv4 = tk.Entry(self.frame)
        self.entry_ue_ipv4.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")  
        
        self.entry_ue_password = tk.Entry(self.frame, show="*")
        self.entry_ue_password.grid(row=3, column=2, padx=20, pady=20, sticky="nsew")  
        
        #gNB
        self.label_gnb = tk.Label(self.frame, text="gNodeB:")
        self.label_gnb.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
        
        self.entry_gnb_ipv4 = tk.Entry(self.frame)
        self.entry_gnb_ipv4.grid(row=4, column=1, padx=20, pady=20, sticky="nsew")  
        
        self.entry_gnb_password = tk.Entry(self.frame, show="*")
        self.entry_gnb_password.grid(row=4, column=2, padx=20, pady=20, sticky="nsew")  
        
        #CORE
        self.label_core = tk.Label(self.frame, text="Core Network:")
        self.label_core.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")
        
        self.entry_core_ipv4 = tk.Entry(self.frame)
        self.entry_core_ipv4.grid(row=5, column=1, padx=20, pady=20, sticky="nsew")  
        
        self.entry_core_password = tk.Entry(self.frame, show="*")
        self.entry_core_password.grid(row=5, column=2, padx=20, pady=20, sticky="nsew")  
        
        #Connect button
        self.button_connect = tk.Button(self.frame, text="Connect", command=self.on_connect)
        self.button_connect.grid(row=6, column=1, padx=20, pady=20, sticky="nsew")

        #Output Message
        self.message_label_ue = tk.Label(self.frame, text="")
        self.message_label_ue.grid(row=7, column=0, columnspan=3)  

        self.message_label_gnb = tk.Label(self.frame, text="")
        self.message_label_gnb.grid(row=8, column=0, columnspan=3)

        self.message_label_core = tk.Label(self.frame, text="")
        self.message_label_core.grid(row=9, column=0, columnspan=3)

        self.message_label_all = tk.Label(self.frame, text="")
        self.message_label_all.grid(row=10, column=0, columnspan=3)


    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

    #ssh methods
    def initialize_ssh_connection_ue(self, hostname, username, password):
        #self.ssh_ue = SSHClient(hostname, 22, username, password)
        self.ssh_ue = SSHClient("10.162.149.122", 22, "laura", "chaparral")
        self.ssh_ue.connect()
        SSHConnections.ssh_ue = self.ssh_ue

    def initialize_ssh_connection_gnb(self, hostname, username, password):
        #self.ssh_gnb = SSHClient(hostname, 22, username, password)
        self.ssh_gnb = SSHClient("10.162.149.121", 22, "laura", "chaparral")
        self.ssh_gnb.connect()
        SSHConnections.ssh_gnb = self.ssh_gnb

    def initialize_ssh_connection_core(self, hostname, username, password):
        #self.ssh_core = SSHClient(hostname, 22, username, password)
        self.ssh_core = SSHClient("10.162.149.143", 22, "laura", "chaparral")
        self.ssh_core.connect()
        SSHConnections.ssh_core = self.ssh_core


    def on_connect(self):
        #Get the values from the entries
        user = self.entry_user.get()
        ue_ip = self.entry_ue_ipv4.get()
        ue_password = self.entry_ue_password.get()  
        gnb_ip = self.entry_gnb_ipv4.get()
        gnb_password = self.entry_gnb_password.get()  
        core_ip = self.entry_core_ipv4.get()
        core_password = self.entry_core_password.get()
        #self.save_data()

        
        # Initialize SSH connections
        try:
            self.initialize_ssh_connection_ue(ue_ip, user, ue_password)
            self.message_label_ue.config(text=f"SSH Connection with {ue_ip} successfully stablished.")
        except Exception as e:
            self.message_label_ue.config(text=f"Error connecting to UE on {ue_ip}: {e}")
            return

        try:
            self.initialize_ssh_connection_gnb(gnb_ip, user, gnb_password)
            self.message_label_gnb.config(text=f"SSH Connection with {gnb_ip} successfully stablished.")
        except Exception as e:
            self.message_label_gnb.config(text=f"Error connecting to gNB on {gnb_ip}: {e}")
            return

        try:
            self.initialize_ssh_connection_core(core_ip, user, core_password)
            self.message_label_core.config(text=f"SSH Connection with {core_ip} successfully stablished.")
        except Exception as e:
            self.message_label_core.config(text=f"Error connecting to core on {core_ip}: {e}")
            return

        self.message_label_all.config(text="All connections successfully established.")


    def connect_ssh(self,remote_host, port, username, password, command):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Acepta automáticamente la llave del host
        try:
            client.connect(remote_host, port=port, username=username, password=password)
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read().decode())  # Muestra la salida del comando
        except Exception as e:
            print(f"Error al conectar o ejecutar el comando: {e}")
        finally:
            client.close()

    
    