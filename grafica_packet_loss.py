import matplotlib.pyplot as plt
import os

def generate_graphs():
    bitrates = ["1", "2", "3", "5", "10"]
    packet_loss_uplink = []
    packet_loss_downlink = []
    
    # Leer los archivos y extraer el porcentaje de pérdida de paquetes
    for bitrate in bitrates:
        for direction in ["uplink", "downlink"]:
            filename = f"{direction}_{bitrate}Mbps.txt"
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    output = file.read()
                    # Aquí necesitas extraer el porcentaje de pérdida de paquetes del output
                    packet_loss = "Extracted packet loss percentage"
                    if direction == "uplink":
                        packet_loss_uplink.append(packet_loss)
                    else:
                        packet_loss_downlink.append(packet_loss)
    
    # Generar la gráfica para uplink
    plt.figure(figsize=(10, 5))
    plt.plot(bitrates, packet_loss_uplink, marker='o', label='Uplink Packet Loss')
    plt.title('Uplink Packet Loss vs Bitrate')
    plt.xlabel('Bitrate (Mbps)')
    plt.ylabel('Packet Loss (%)')
    plt.legend()
    plt.show()
    
    # Generar la gráfica para downlink
    plt.figure(figsize=(10, 5))
    plt.plot(bitrates, packet_loss_downlink, marker='o', label='Downlink Packet Loss')
    plt.title('Downlink Packet Loss vs Bitrate')
    plt.xlabel('Bitrate (Mbps)')
    plt.ylabel('Packet Loss (%)')
    plt.legend()
    plt.show()