import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
import time
import os
import matplotlib.ticker as ticker

rc('text', usetex = True)
rc('font', family='serif')

rc('text', usetex = True)
rc('font', family='serif')

# plot configuration
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['lines.linewidth'] = 5
mpl.rcParams['lines.markersize'] = 14
mpl.rcParams['font.size'] = 48
mpl.rcParams['xtick.labelsize'] = 46
mpl.rcParams['ytick.labelsize'] = 46
mpl.rcParams['legend.fontsize'] = 46
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['legend.framealpha'] = 0.5
mpl.rcParams['figure.figsize'] = [5.2, 3.76]
sz = 46


def exp_range(start, stop, step):
    while (start < stop):
        yield start
        start *= step
    return

folder_path = '../output'
output_folder_path = '../plots'

graph_names = ['yahoo','edit-frwiki','edit-enwiki','bag','movie-lens']

colors = ['olive']
alpha= 0.6
width = 1 # size of bars in the plot
lw = 9

for gname in graph_names:
    input_file = folder_path + '/' + gname

    Batch_df = pd.read_csv(folder_path + '/' + gname + '/' + 'batch' + '/' + gname + '.txt', sep=',',skipinitialspace=True)

    print(Batch_df.columns)

    print(Batch_df.head())

    batches = Batch_df['batch']
    bfly = Batch_df['bfly']


    fig, ax = plt.subplots(figsize=(8, 5))  # plt.figure()

    ax.plot(batches, bfly, alpha=alpha, color=colors[0], linewidth=lw, marker='o', markersize = 22, markevery=12, linestyle=':', markerfacecolor='deeppink', markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')

    #plt.yscale('log')
    ax.margins(x=0)
    ax.set_ylabel('\# Butterflies')
    ax.set_xlabel('\# Edge')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2g'))


    output_path = output_folder_path + '/' + gname + '/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ax.figure.savefig(output_path + '/bfly-' + gname + '.pdf', format='pdf',
                      bbox_inches='tight', dpi=400)
    plt.show(block=False)
    time.sleep(1)
    plt.close("all")


