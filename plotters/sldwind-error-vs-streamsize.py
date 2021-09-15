import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
import time
import os

rc('text', usetex=True)
rc('font', family='serif')

# plot configuration
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['lines.linewidth'] = 5
mpl.rcParams['lines.markersize'] = 14
mpl.rcParams['font.size'] = 42
mpl.rcParams['xtick.labelsize'] = 38
mpl.rcParams['ytick.labelsize'] = 38
mpl.rcParams['legend.fontsize'] = 38
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['legend.framealpha'] = 0.5
mpl.rcParams['figure.figsize'] = [5.2, 3.76]
sz = 38

def error_rate(exact, est):
    n = len(exact)
    for i in range(n):
        est[i] = abs(exact[i] - est[i]) / exact[i] * 100
    return est


folder_path = './sld_data'
output_folder_path = './plots'

graph_names = ['lkml', 'en-wiki', 'digg', 'movie-lens']
stream_sizes = [599858, 5573038, 3010898, 10000054]
num_quries = 30
window_size = 500000
sample_window_ratio = [0.05, 0.10, 0.20]
intervals = [1 / 6, 1 / 2, 1 / 4, 1 / 8]

linestyles = ['-', '-', '-']
markers = ['s', 'o', 'D']
colors = ['palevioletred', 'lightseagreen', 'sandybrown']
alpha = 1.0
width = 1.0  # size of bars in the plot
lw = 4
reservoir = 100 * 1000

for i in range(4):
    graph_name = graph_names[i]
    input_file = folder_path + '/' + graph_name
    exact_data = np.genfromtxt(input_file + '/batch.' + graph_name, delimiter=',')[:, 2]
    five_data = np.genfromtxt(input_file + '/5.' + graph_name, delimiter=',')[:, 2]
    ten_data = np.genfromtxt(input_file + '/10.' + graph_name, delimiter=',')[:, 2]
    twenty_data = np.genfromtxt(input_file + '/20.' + graph_name, delimiter=',')[:, 2]
    five_err = [0]
    for x in error_rate(exact_data, five_data):
        five_err.append(x)
    ten_err = [0]
    for x in error_rate(exact_data, ten_data):
        ten_err.append(x)
    twenty_err = [0]
    for x in error_rate(exact_data, twenty_data):
        twenty_err.append(x)

    fig, ax = plt.subplots(figsize=(8, 5))  # plt.figure()
    stream_size = stream_sizes[i]
    x_axis = [i for i in range(0, stream_size, (stream_size // num_quries))]
    ax.plot(x_axis, five_err, alpha=alpha, color=colors[0], linewidth=lw, linestyle=linestyles[0],
            solid_capstyle='round', dash_capstyle='round')
    ax.plot(x_axis, ten_err, alpha=alpha, color=colors[1], linewidth=lw, linestyle=linestyles[1],
            solid_capstyle='round', dash_capstyle='round')
    ax.plot(x_axis, twenty_err, alpha=alpha, color=colors[2], linewidth=lw, linestyle=linestyles[2],
            solid_capstyle='round', dash_capstyle='round')

    ax.margins(x=0)
    ax.set_ylabel('Error(\%)')
    ax.set_xlabel('\# Edges')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
    # ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

    ax.legend(['5\% sample rate', '10\% sample rate', '20\% sample rate'], fancybox=True, framealpha=1,
              shadow=True, borderpad=0.25, borderaxespad=0.20, handletextpad=0.2, handlelength=1.5, labelspacing=0.2)

    output_path = output_folder_path + '/' + graph_name + '/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ax.figure.savefig(output_path + '/error-window-' + graph_name + '.pdf', format='pdf', bbox_inches='tight', dpi=300)
    time.sleep(1)
    plt.close("all")
