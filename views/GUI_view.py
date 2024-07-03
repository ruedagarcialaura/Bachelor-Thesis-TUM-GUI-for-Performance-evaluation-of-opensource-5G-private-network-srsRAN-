import tkinter as tk

class GUI_view(tk.Frame):
    def __init__(self, root):
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.throughput_view_label = tk.Label(self.frame, text= "Performance Evaluation of srsRAN")
        self.throughput_view_label.grid()

        '''self.uplink_button = tk.Button(self.frame, text="Plot uplink data", command=self.plot_uplink_data)
        self.uplink_button.grid()

        self.downlink_button = tk.Button(self.frame, text="Plot downlink data", command=self.plot_downlink_data)
        self.downlink_button.grid()'''

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()

    '''def extract_throughput_from_files(self, folder_path):
        throughput_pattern = re.compile(r'(\d+\.\d+|\d+)\s*(K|M|G)bits/sec')
        throughput_data = {'uplink': {1: [], 2: [], 3: [], 5: [], 10: []},
                           'downlink': {1: [], 2: [], 3: [], 5: [], 10: []}}
        for filename in os.listdir(folder_path):
            print(f"Checking file: {filename}")
            if 'uplink' in filename or 'downlink' in filename:
                direction = 'uplink' if 'uplink' in filename else 'downlink'
                match_file_name = re.search(r'(\d+)Mbps', filename)
                if match_file_name:
                    bitrate = int(match_file_name.group(1))
                with open(os.path.join(folder_path, filename), 'r') as file:
                    for line in file:
                        if 'receiver' in line:
                            print(f"Found receiver line: {line.strip()}")
                            match = throughput_pattern.search(line)
                            if match:
                               # Extraer el valor y la unidad
                               value, unit = match.groups()
                               value = float(value)
                            
                               # Convertir el valor a Mbits/sec
                               if unit == 'K':
                                 value /= 1000  # Convertir de Kbits/sec a Mbits/sec
                               elif unit == 'G':
                                 value *= 1000  # Convertir de Gbits/sec a Mbits/sec
                            
                               # Agregar el valor convertido a la estructura de datos
                               throughput_data[direction][bitrate].append(value)
                               print(f"Extracted throughput: {value} Mbits/sec")
        return throughput_data'''
                            
    '''def plot_uplink_throughput_data(self):
        folder_path = 'iperf3_outputs'
        data = self.extract_throughput_from_files(folder_path)
        num_plots = sum(len(bitrates) for bitrates in data.values())
        num_columns = 2  # Número de columnas de subplots
        num_rows = num_plots // num_columns + (num_plots % num_columns > 0)

        plt.figure(figsize=(10, 4 * num_rows))  # Ajustar el tamaño de la figura

        plot_index = 1  # Índice para el subplot actual
        for direction, bitrates in data.items():
            if direction == 'uplink':
                for bitrate, values in bitrates.items():
                    ax = plt.subplot(num_rows, num_columns, plot_index)
                    ax.plot(values, label=f"{direction} {bitrate}Mbps")
                    ax.set_title(f"{direction} {bitrate}Mbps")
                    ax.legend()
                    plot_index += 1

        plt.tight_layout()  # Ajustar los subplots para evitar superposiciones
        plt.show()'''

    '''def plot_downlink_throughput_data(self):
        folder_path = 'iperf3_outputs'
        data = self.extract_throughput_from_files(folder_path)
        num_plots = sum(len(bitrates) for bitrates in data.values())
        num_columns = 2  # Número de columnas de subplots
        num_rows = num_plots // num_columns + (num_plots % num_columns > 0)

        plt.figure(figsize=(10, 4 * num_rows))  # Ajustar el tamaño de la figura

        plot_index = 1  # Índice para el subplot actual
        for direction, bitrates in data.items():
            if direction == 'downlink':
                for bitrate, values in bitrates.items():
                    ax = plt.subplot(num_rows, num_columns, plot_index)
                    ax.plot(values, label=f"{direction} {bitrate}Mbps")
                    ax.set_title(f"{direction} {bitrate}Mbps")
                    ax.legend()
                    plot_index += 1

        plt.tight_layout()  # Ajustar los subplots para evitar superposiciones
        plt.show()'''

    '''def plot_uplink_data(self):
        self.plot_uplink_throughput_data()
        #print(self.extract_throughput_from_files('iperf3_outputs'))

    def plot_downlink_data(self):
        self.plot_downlink_throughput_data()
        #print(self.extract_throughput_from_files('iperf3_outputs'))'''
