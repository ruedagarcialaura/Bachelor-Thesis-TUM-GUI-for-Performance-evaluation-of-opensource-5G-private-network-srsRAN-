import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import subprocess
#import os
import paramiko

# Create the main window
window = ThemedTk(theme="aqua")
window.title("GUI de laura")
window.geometry("500x500")

# Create a function to run the ping command
def ping():
    ip_address = entry.get()  # Get the IP address from the entry widget
    #response = os.system("ping -n 1 " + ip_address)  # Execute the ping command
    response = subprocess.run(["ping", "-n", "4", ip_address], capture_output=True, text=True)
    #print(response)
    if response.returncode == 0:
        result_label.config(text=f"{ip_address} is reachable")
        result_label2.config(text=response.stdout)
    else:
        result_label.config(text=f"{ip_address} is unreachable")
   
# Create an entry widget for the IP address for ping
entry_label = ttk.Label(window, text="Enter the IP address for ping:")
entry_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
entry = ttk.Entry(window)
entry.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

# Create a button to trigger the iperf function
button = ttk.Button(window, text="ping", command=ping)
button.grid(row=1, column=1, padx=20, pady=20)

#Create a label to display the result
result_label = ttk.Label(window, text="")
result_label.grid(row=3, column=0, padx=20, pady=20)
result_label2 = ttk.Label(window, text="")
result_label2.grid(row=3, column=1, padx=20, pady=20)




# Create a function to run the iperf3 command with UDP
def iperf3():
    ip_address = entry2.get()  # Get the IP address from the entry widget
    response = os.system("iperf3 -c " + ip_address + " -u")  # Execute the iperf3 command with UDP option
    if response == 0:
        print("iperf3 UDP connection to", ip_address, "successful")
    else:
        print("iperf3 UDP connection to", ip_address, "failed")


# Create an entry widget for the IP address for iperf3
entry_label2 = ttk.Label(window, text="Enter the IP address for iperf3:")
entry_label2.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
entry2 = ttk.Entry(window)
entry2.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")
#entry2.config(borderwidth=2, relief="groove")
# Create a button to trigger the iperf function
button4 = ttk.Button(window, text="iperf", command=iperf3)
button4.grid(row=5, column=1, padx=20, pady=20)

# Start the main event loop
window.mainloop()