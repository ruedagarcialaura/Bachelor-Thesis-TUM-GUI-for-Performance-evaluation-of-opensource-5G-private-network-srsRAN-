import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Generate dummy data
data1= [
    649.6714153011233, 586.1735698828816, 664.7688538100692, 752.3029856408025,
    # ... rest of the data
]

data2 = [
    # Add your second set of data here
    649.6714153011233, 586.1735698828816, 664.7688538100692, 752.3029856408025,
    
]

data3 = [
    # Add your second set of data here
    649.6714153011233, 586.1735698828816, 664.7688538100692, 752.3029856408025,
    
]

class Results_view(tk.Frame):
    def __init__(self, root):
        #super()._init_(root)
        self.root = root
        
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.results_view_label = tk.Label(self.frame, text="Welcome to the Results view")
        self.results_view_label.grid()

        self.inner_frame = tk.Frame(self.frame)
        self.inner_frame.grid()

        # Create additional frames
        frame1 = tk.Frame(self.inner_frame)
        frame1.grid(row=0, column=0)
        frame1.configure(bg="red")

        frame2 = tk.Frame(self.inner_frame)
        frame2.grid(row=0, column=1)
        frame2.configure(bg="green")

        frame3 = tk.Frame(self.inner_frame)
        frame3.grid(row=1, column=0)
        frame3.configure(bg="blue")

        frame4 = tk.Frame(self.inner_frame)
        frame4.grid(row=1, column=1)
        frame4.configure(bg="yellow")

        # Create a Matplotlib figure and axes
        fig = Figure(figsize=(3.5, 2.5), dpi=100)     #LAURA: I changed the size of the figure
        ax = fig.add_subplot(111)
        ax.boxplot([data1, data2, data3])

        # Create a Matplotlib figure and axes
        fig2 = Figure(figsize=(3.5, 2.5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.boxplot([data1, data2, data3])

        fig3 = Figure(figsize=(3.5, 2.5), dpi=100)
        ax3 = fig3.add_subplot(111)
        ax3.boxplot([data1, data2, data3])

        fig4 = Figure(figsize=(3.5, 2.5), dpi=100) 
        ax4 = fig4.add_subplot(111)
        ax4.boxplot([data1, data2, data3])

        ax.set_title('Latency', fontsize=7)  # Set fontsize to 7 or any desired size
        ax2.set_title('Packet Loss', fontsize=7)
        ax3.set_title('Throughput', fontsize=7)
        ax4.set_title('Inter Sending Time', fontsize=7)



            # Add labels and title
            # Custom labels for the x-axis
        labels = ['1 Mbps', '5 Mbps', '10 Mbps']

            # Set the position of the ticks first
        ax.set_xticks([1, 2, 3])

            # Then set the custom labels
        ax.set_xticklabels(labels, fontsize=7)
        ax2.set_xticklabels(labels, fontsize=7)
        ax3.set_xticklabels(labels, fontsize=7)
        ax4.set_xticklabels(labels, fontsize=7)

        ax.tick_params(axis='y', labelsize=7)
        ax2.tick_params(axis='y', labelsize=7)
        ax3.tick_params(axis='y', labelsize=7)
        ax4.tick_params(axis='y', labelsize=7)

        # Embed the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.inner_frame)  # Use the inner_frame as the master
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        canvas2 = FigureCanvasTkAgg(fig2, master=self.inner_frame)  # Use the inner_frame as the master
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, sticky="nsew")

        canvas3 = FigureCanvasTkAgg(fig3, master=self.inner_frame)  # Use the inner_frame as the master
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        canvas4 = FigureCanvasTkAgg(fig4, master=self.inner_frame)  # Use the inner_frame as the master 
        canvas4.draw()
        canvas4.get_tk_widget().grid(row=1, column=1, sticky="nsew")


                # Configure the grid to expand equally
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_rowconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=1)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_forget()