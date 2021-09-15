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
mpl.rcParams['font.size'] = 55
mpl.rcParams['xtick.labelsize'] = 55
mpl.rcParams['ytick.labelsize'] = 55
mpl.rcParams['legend.fontsize'] = 55
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['legend.framealpha'] = 0.5
mpl.rcParams['figure.figsize'] = [5.2, 3.76]
sz = 52


def exp_range(start, stop, step):
    while (start < stop):
        yield start
        start *= step
    return

folder_path = '../output'
output_folder_path = '../plots'

graph_names = ['movie-lens','edit-frwiki','edit-enwiki','yahoo','bag']
hatches = ['', '\\', '/','\\','+']
linestyles = [':','--','-','-']
markers = ['o','s','D']

colors = ['tomato','mediumseagreen','dodgerblue', 'k', 'pink','gray']
alpha= 1.0
width = 1.2 # size of bars in the plot
lw = 6

def narrow_down_with_reservoir(df, reservoir):
    return df.loc[df['res-sz'] == reservoir]


def get_median_time(df, gamma, n_edges):
    cur_runtimes = df['time'].loc[(df ['batch'] == n_edges) & (df ['gamma'] == gamma)]
    mean_time = np.median(cur_runtimes)
    return mean_time

for gname in graph_names:
    for reservoir in exp_range(75000, 600 * 1000 + 1, 2):
        file_name_Res = 'res=[75,600].txt'
        file_name_Ada = 'res=[75,600],gamma=[0.5,0.9].txt'

        Batch_df = pd.read_csv(folder_path + '/' + gname + '/' + 'batch' + '/' + gname + '.txt', sep=',', skipinitialspace=True)
        Ada_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Ada' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
        oldAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'oldAda' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
        IAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IAda' + '/' + file_name_Ada, sep=',',skipinitialspace=True)


        processed_edges = Ada_df['batch'].max()
        reservoirs = sorted(Ada_df['res-sz'].unique())
        batches = sorted(Ada_df['batch'].unique())
        exact_bfly = Batch_df['bfly'].max()

        oldAda_df = narrow_down_with_reservoir(oldAda_df, reservoir)
        Ada_df = narrow_down_with_reservoir(Ada_df, reservoir)
        IAda_df = narrow_down_with_reservoir(IAda_df, reservoir)

        print(reservoirs)

        x_location = 1
        fig, ax = plt.subplots(figsize=(13, 5))  # plt.figure()


        algorithms = ['Ada1', 'Ada2', 'Ada3']

        x_location = 1
        xs = []
        mx = 0
        gammas = [0.5,0.6,0.7,0.8,0.9]
        for gamma in gammas:

            Ada_time = get_median_time(Ada_df, gamma, processed_edges)
            oldAda_time = get_median_time(oldAda_df, gamma, processed_edges)
            IAda_time = get_median_time(IAda_df, gamma, processed_edges)

            xs.append(x_location)

            ax.bar(x_location - width, oldAda_time, width, alpha=alpha, hatch=hatches[0], color=colors[0], linewidth=2, edgecolor='k')
            ax.bar(x_location, Ada_time, width, alpha=alpha, hatch=hatches[1], color = colors [1], linewidth=2, edgecolor='k')
            ax.bar(x_location + width, IAda_time, width, alpha=alpha, hatch=hatches[2], color=colors[2], linewidth=2, edgecolor='k')

            x_location += 5
            plt.gca().set_prop_cycle(None)

            mx = max(mx, float(Ada_time))
            mx = max(mx, float(oldAda_time))
            mx = max(mx, float(IAda_time))

        ax.margins(x=0.9)
        #plt.ylim((1e-2, 10**4 + 30000))
        #plt.yscale('log')
        ax.set_ylabel('Time(sec)')
        ax.set_xlabel(r'$\gamma$', fontsize= 80)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2g'))

        str_gammas = ['{:.1f}'.format(i) for i in gammas]

        plt.xticks(xs, str_gammas)

        plt.xlim([-width, max(xs) + width + 1])

        output_path = output_folder_path + '/' + gname + '/'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ax.figure.savefig(output_path + '/gamma-time-' + gname + '-reservoir=' + str(reservoir) + '.pdf', format='pdf', bbox_inches='tight', dpi=400)
        plt.show(block=False)
        time.sleep(0.5)
        plt.close("all")
