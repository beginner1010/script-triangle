import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
import time
import os
import scipy.signal

rc('text', usetex = True)
rc('font', family='serif')

# plot configuration
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['lines.markersize'] = 14
mpl.rcParams['font.size'] = 42
mpl.rcParams['xtick.labelsize'] = 38
mpl.rcParams['ytick.labelsize'] = 38
mpl.rcParams['legend.fontsize'] = 38
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['legend.framealpha'] = 0.5
mpl.rcParams['figure.figsize'] = [5.2, 3.76]
sz = 38


def exp_range(start, stop, step):
    while (start < stop):
        yield start
        start *= step
    return

folder_path = '../output'
output_folder_path = '../plots'

graph_names = ['edit-frwiki']
batch_sizes = [10000, 10000, 100000, 100000]
algorithms = ['Res','IRes','Ada']
intervals = [1/6, 1/2, 1/4, 1/8]

linestyles = ['-','-','-']
markers = ['s', 'o', 'D']
colors = ['palevioletred', 'lightseagreen','sandybrown']
alpha= 1.0
width = 1.0 # size of bars in the plot
lw = 4
reservoir = 400 * 1000

def get_median_error(batches, df, reservoir, Batch_df):
    errors = []
    for batch in batches:
        cur_bfly = df['bfly'].loc[(df ['batch'] == batch) & (df ['res-sz'] == reservoir)]
        #print(df.loc[(df ['batch'] == batch) & (df ['res-sz'] == reservoir)])
        exact_bfly = float(Batch_df['bfly'].loc[(Batch_df ['batch'] == batch)])
        cur_errors = abs(cur_bfly - exact_bfly) / exact_bfly * 100.0
        errors.append(cur_errors.median())
    return errors


for gname, batch, interval_size in zip(graph_names, batch_sizes, intervals):
    input_file = folder_path + '/' + gname

    Batch_df = pd.read_csv(folder_path + '/' + gname + '/' + 'batch' + '/' + gname + '.txt', sep=',', skipinitialspace=True)
    Res_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Res' + '/res=[50,400].txt', sep=',', skipinitialspace=True)
    IRes_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IRes' + '/res=[50,400].txt', sep=',', skipinitialspace=True)
    Ada_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Ada' + '/res=[50,400].txt', sep=',', skipinitialspace=True)

    print(Res_df.columns)

    processed_edges = Res_df['batch'].max()
    reservoirs = sorted(Res_df['res-sz'].unique())
    iterations = sorted(Res_df['iteration'].unique())
    batches = sorted(Res_df['batch'].unique())
    exact_bfly = Batch_df['bfly'].max()

    reservoirs = [i for i in reservoirs if i <= 200 * 1000]

    new_batches = [b for b in batches if (b > reservoir)]

    Res_error = get_median_error(new_batches, Res_df, reservoir, Batch_df)
    IRes_error = get_median_error(new_batches, IRes_df, reservoir, Batch_df)
    Ada_error = get_median_error(new_batches, Ada_df, reservoir, Batch_df)

    fig, ax = plt.subplots(figsize=(8, 5))  # plt.figure()

    #interval_size = inter # only 6 points are printed

    ax.plot(new_batches, scipy.signal.savgol_filter(Res_error, 51, 3), alpha=alpha, color=colors[0], linewidth=lw, linestyle=linestyles[0], markevery=interval_size, markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
    ax.plot(new_batches, scipy.signal.savgol_filter(IRes_error, 51, 3), alpha=alpha, color=colors[1], linewidth=lw, linestyle=linestyles[1], markevery=interval_size, markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
    ax.plot(new_batches, scipy.signal.savgol_filter(Ada_error, 51, 3), alpha=alpha, color=colors[2], linewidth=lw, linestyle=linestyles[2], markevery=interval_size, markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')

    ax.margins(x=0)
    plt.yscale('log', basey=10)
    plt.ylim((10**-2, 10**2))
    ax.set_ylabel('Error(\%)')
    ax.set_xlabel('\# Edges')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
    #ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

    ax.legend(algorithms, fancybox=True, framealpha=0.5,
           shadow=False, borderpad=0.25, borderaxespad=0.20, handletextpad=0.2, handlelength=1.5, labelspacing=0.2)

    output_path = output_folder_path + '/' + gname + '/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ax.figure.savefig(output_path + '/error-stream-' + gname + '.pdf', format='pdf', bbox_inches='tight', dpi=300)
    plt.show(block=False)
    time.sleep(1)
    plt.close("all")


