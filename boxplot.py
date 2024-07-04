import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt

# Generate dummy data
data1 = [
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

# Create the main window
window = tk.Tk()


# Add your GUI elements here


# Create box plots for both data sets


# Create a canvas to display the plot

# Create three more figures and axes
# Create a figure and axis
fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()

# Create box plots for the additional data sets
ax.boxplot([data1, data2, data3])
ax2.boxplot([data1, data2, data3])
ax3.boxplot([data1, data2, data3])
ax4.boxplot([data1, data2,  data3])



ax.set_title('Latency')
ax2.set_title('Packet Loss')
ax3.set_title('Throughput')
ax4.set_title('Inter Sending Time')

ax.set_ylabel('(ms)')
ax2.set_ylabel('(%)')
ax3.set_ylabel('(Mbps)')
ax4.set_ylabel('(ms)')

# Add labels and title
# Custom labels for the x-axis
labels = ['1 Mbps', '5 Mbps', '10 Mbps']

# Set the position of the ticks first
ax.set_xticks([1, 2, 3])

# Then set the custom labels
ax.set_xticklabels(labels)
ax2.set_xticklabels(labels)
ax3.set_xticklabels(labels)
ax4.set_xticklabels(labels)



canvas1 = FigureCanvasTkAgg(fig, master=window)  # Assuming canvas1 and fig1 are defined somewhere above
canvas1.draw()
canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew")

canvas2 = FigureCanvasTkAgg(fig2, master=window)
canvas2.draw()
canvas2.get_tk_widget().grid(row=0, column=1, sticky="nsew")

canvas3 = FigureCanvasTkAgg(fig3, master=window)
canvas3.draw()
canvas3.get_tk_widget().grid(row=1, column=0, sticky="nsew")

canvas4 = FigureCanvasTkAgg(fig4, master=window)
canvas4.draw()
canvas4.get_tk_widget().grid(row=1, column=1, sticky="nsew")

# Configure the grid to expand equally
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# Start the main event loop
window.mainloop()

'''data1 = [
    22.215604782104492,
    151.0751247406006,
    212.07904815673828,
    210.12496948242188,
    284.9116325378418,
    283.95748138427734,
    282.98234939575195,
    282.0107936859131,
    281.0404300689697,
    280.06529808044434,
    279.09088134765625,
    278.11670303344727,
    277.14061737060547,
    276.1657238006592,
    275.1915454864502,
    274.2171287536621,
    273.2434272766113,
    272.27115631103516,
    271.2976932525635,
    270.32470703125,
    269.34814453125,
    268.37658882141113,
    267.40241050720215,
    266.42704010009766,
    265.45166969299316,
    264.4767761230469,
    263.5030746459961,
    262.5293731689453,
    261.5547180175781,
    260.58053970336914,
    259.60516929626465,
    258.63122940063477,
    257.6558589935303,
    255.68127632141113,
    254.70614433288574,
    253.73101234436035,
    252.75707244873047,
    251.78170204162598,
    250.8077621459961,
    249.8319149017334,
    248.85892868041992,
    247.88403511047363,
    246.90866470336914,
    245.93424797058105,
    244.95959281921387,
    243.98517608642578,
    243.011474609375,
    242.03896522521973,
    241.06287956237793,
    240.09156227111816,
    239.1185760498047,
    238.13486099243164,
    237.166166305542,
    236.18721961975098,
    235.21685600280762,
    234.24005508422852,
    233.26849937438965,
    232.29050636291504,
    231.31799697875977,
    230.34071922302246,
    229.3686866760254,
    228.38878631591797,
    227.41460800170898,
    226.4397144317627,
    225.4641056060791,
    224.47609901428223,
    223.55079650878906,
    222.54180908203125,
    221.57025337219238,
    220.59226036071777,
    219.6216583251953,
    218.62411499023438,
    217.66352653503418,
    215.69395065307617,
    214.7054672241211,
    213.7439250946045,
    212.75639533996582,
    211.82823181152344,
    210.81924438476562,
    209.82956886291504,
    208.87041091918945,
    207.89694786071777,
    206.9225311279297,
    205.9471607208252,
    204.9860954284668,
    203.99904251098633,
    203.01318168640137,
    202.07881927490234
]'''

