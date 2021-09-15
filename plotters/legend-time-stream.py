import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
import time
import os

rc('text', usetex = True)
rc('font', family='serif')

# plot configuration
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['lines.linewidth'] = 5
mpl.rcParams['lines.markersize'] = 14
mpl.rcParams['font.size'] = 48
mpl.rcParams['xtick.labelsize'] = 44
mpl.rcParams['ytick.labelsize'] = 44
mpl.rcParams['legend.fontsize'] = 44
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['legend.framealpha'] = 0.5
mpl.rcParams['figure.figsize'] = [5.2, 3.76]
sz = 44


def exp_range(start, stop, step):
    while (start < stop):
        yield start
        start *= step
    return

folder_path = '../output'
output_folder_path = '../plots'

graph_names = ['yahoo']
markers = ['s', 'o', 'D', '*','^']
linestyles = ['-',':','-.','--','..']
hatches = ['', '\\', '/','\\','+']
colors = ['tomato','mediumseagreen','dodgerblue', 'red', 'blue','k']

alpha= 0.8
width = 2.0 # size of bars in the plot
lw = 6
sz_marker=22

def get_median_runtime(batches, df, reservoir):
    runtimes = []
    for batch in batches:
        cur_time = df['time'].loc[(df ['batch'] == batch) & (df ['res-sz'] == reservoir)]
        #print(df.loc[(df ['batch'] == batch) & (df ['res-sz'] == reservoir)])
        runtimes.append(cur_time.median())
    return runtimes

def narrow_down_with_gamma(df, gamma):
    return df.loc[df['gamma'] == gamma]


for gname in graph_names:
    for reservoir in exp_range(75000, 600 * 1000 + 1, 2):
        for gamma in [0.5, 0.6, 0.7, 0.8, 0.9]:
            file_name_Res = 'res=[75,600].txt'
            file_name_Ada = 'res=[75,600],gamma=[0.5,0.9].txt'

            Batch_df = pd.read_csv(folder_path + '/' + gname + '/' + 'batch' + '/' + gname + '.txt', sep=',', skipinitialspace=True)
            Res_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Res' + '/' + file_name_Res, sep=',', skipinitialspace=True)
            IRes_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IRes' + '/' + file_name_Res, sep=',', skipinitialspace=True)
            Ada_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Ada' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
            oldAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'oldAda' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
            IAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IAda' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
            Mar_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Mar' + '/' + file_name_Res, sep=',', skipinitialspace=True)

            print(Res_df.columns)

            Ada_df = narrow_down_with_gamma(Ada_df, gamma)
            oldAda_df = narrow_down_with_gamma(oldAda_df, gamma)
            IAda_df = narrow_down_with_gamma(IAda_df, gamma)

            processed_edges = Res_df['batch'].max()
            reservoirs = sorted(Res_df['res-sz'].unique())
            iterations = sorted(Res_df['iteration'].unique())
            batches = sorted(Res_df['batch'].unique())
            exact_bfly = Batch_df['bfly'].max()

            Res_time = get_median_runtime(batches, Res_df, reservoir)
            IRes_time = get_median_runtime(batches, IRes_df, reservoir)
            Ada_time = get_median_runtime(batches, Ada_df, reservoir)
            oldAda_time = get_median_runtime(batches, oldAda_df, reservoir)
            IAda_time = get_median_runtime(batches, IAda_df, reservoir)

            fig, ax = plt.subplots(figsize=(8, 5))  # plt.figure()

            algorithms = ['Ada1', 'Ada2', 'Ada3']

            #ax.plot(batches, Res_time, alpha=alpha, color=colors[0], linewidth=lw, marker=markers[0], markevery=15, markersize = sz_marker, linestyle=linestyles[0], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
            #ax.plot(batches, IRes_time, alpha=alpha, color=colors[1], linewidth=lw, marker=markers[1], markevery=15, markersize = sz_marker, linestyle=linestyles[1], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
            ax.plot(batches, oldAda_time, alpha=alpha, color=colors[0], linewidth=lw, marker=markers[0], markevery=15, markersize = sz_marker, linestyle=linestyles[3], dashes=(4,2,3,2), markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
            ax.plot(batches, Ada_time, alpha=alpha, color=colors[1], linewidth=lw, marker=markers[1], markevery=15, markersize = sz_marker, linestyle=linestyles[2], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
            ax.plot(batches, IAda_time, alpha=alpha, color=colors[2], linewidth=lw, marker=markers[2], markevery=15, markersize = sz_marker, linestyle=linestyles[3], dashes=(5,2), markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')

            ax.margins(x=0)
            ax.set_ylabel('Time(sec)')
            ax.set_xlabel('\# Edges')
            ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
            ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

            ax.legend(algorithms, fancybox=True, framealpha=1.0, ncol=5, bbox_to_anchor=(-1, -1.05),
                   shadow=True, borderpad=0.2, borderaxespad=0.2, handletextpad=0.3, handlelength=1.5, labelspacing=0.3,
                      columnspacing = 0.5, frameon=True)

            output_path = output_folder_path + '/' + gname + '/'
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            ax.figure.savefig(output_folder_path + '/legends/' + 'time-stream' + '.pdf', format='pdf', bbox_inches='tight', dpi=300)
            plt.show(block=False)
            time.sleep(1)
            plt.close("all")
            exit(0)


