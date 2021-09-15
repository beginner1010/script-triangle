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
mpl.rcParams['font.size'] = 52
mpl.rcParams['xtick.labelsize'] = 52
mpl.rcParams['ytick.labelsize'] = 52
mpl.rcParams['legend.fontsize'] = 52
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

graph_names = ['edit-enwiki'] #['movie-lens','edit-frwiki','edit-enwiki','yahoo','bag']
hatches = ['', '\\', '/','\\','+']

colors = ['tomato','mediumseagreen','dodgerblue', 'red', 'blue','k']
alpha= 1.0
width = 1.3 # size of bars in the plot
lw = 6

def get_median_throughput(reservoirs, processed_edges, df):
    runtimes = []
    for rs in reservoirs:
        total_runtimes = df['time'].loc[(df['batch'] == processed_edges) & (df ['res-sz'] == rs)]
        runtimes.append(total_runtimes.median())
    return processed_edges / runtimes


def narrow_down_with_gamma(df, gamma):
    return df.loc[df['gamma'] == gamma]

for gname in graph_names:
    for gamma in [0.6]: #[0.5, 0.6, 0.7, 0.8, 0.9]
        file_name_Res = 'res=[75,600].txt'
        file_name_Ada = 'res=[75,600],gamma=[0.5,0.9].txt'

        Batch_df = pd.read_csv(folder_path + '/' + gname + '/' + 'batch' + '/' + gname + '.txt', sep=',', skipinitialspace=True)
        Res_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Res' + '/' + file_name_Res, sep=',', skipinitialspace=True)
        IRes_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IRes' + '/' + file_name_Res, sep=',', skipinitialspace=True)
        Ada_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Ada' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
        oldAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'oldAda' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
        IAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IAda' + '/' + file_name_Ada, sep=',',skipinitialspace=True)
        #Mar_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Mar' + '/' + file_name_Res, sep=',', skipinitialspace=True)

        Ada_df = narrow_down_with_gamma(Ada_df, gamma)
        oldAda_df = narrow_down_with_gamma(oldAda_df, gamma)
        IAda_df = narrow_down_with_gamma(IAda_df, gamma)

        processed_edges = Res_df['batch'].max()
        reservoirs = sorted(Res_df['res-sz'].unique())
        iterations = sorted(Res_df['iteration'].unique())
        batches = sorted(Res_df['batch'].unique())

        Res_time = get_median_throughput(reservoirs, processed_edges, Res_df)
        IRes_time = get_median_throughput(reservoirs, processed_edges, IRes_df)
        Ada_time = get_median_throughput(reservoirs, processed_edges, Ada_df)
        oldAda_time = get_median_throughput(reservoirs, processed_edges, oldAda_df)
        IAda_time = get_median_throughput(reservoirs, processed_edges, IAda_df)

        algorithms = ['Ada1', 'Ada2', 'Ada3']

        x_location = 1
        fig, ax = plt.subplots(figsize=(13, 5))  # plt.figure()

        mx = 0
        mx = max(mx, max(oldAda_time))
        mx = max(mx, max(Ada_time))
        mx = max(mx, max(IAda_time))

        xs = []

        #print('Reservoir', 'fleet1', 'fleet2', 'fleet3')
        for i in range (0, len(Res_time)):
            xs.append(x_location)
            #ax.bar(x_location - 2 * width, Res_err[i], width, alpha=alpha, hatch=hatches[0], color = colors [0], linewidth=2, edgecolor='k')
            #ax.bar(x_location - width, IRes_err[i], width, alpha=alpha, hatch=hatches[1], color = colors [1], linewidth=2, edgecolor='k')
            ax.bar(x_location - width, oldAda_time[i], width, alpha=alpha, hatch=hatches[0], color=colors[0], linewidth=2, edgecolor='k')
            ax.bar(x_location, Ada_time[i], width, alpha=alpha, hatch=hatches[1], color = colors [1], linewidth=2, edgecolor='k')
            ax.bar(x_location + width, IAda_time[i], width, alpha=alpha, hatch=hatches[2], color=colors[2], linewidth=2, edgecolor='k')

            #print(reservoirs[i], oldAda_time[i], Ada_time[i], IAda_time[i])



            x_location += 5
            plt.gca().set_prop_cycle(None)

        #ax.margins(x=0)
        #plt.ylim(0.1, 100 * 1000 * 1000)
        plt.xlim([-1, max(xs) + width + 0.5])
        #plt.yscale('log')
        ax.set_ylabel('Throughput')
        ax.set_xlabel('Reservoir Size')
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2g'))

        new_reservoirs = ['{:.2g}'.format(i) for i in reservoirs]
        plt.xticks(xs, new_reservoirs)
        #ax.legend(algorithms, fancybox=True, framealpha=1,
        #       shadow=True, borderpad=0.25, borderaxespad=0.20, handletextpad=0.2, handlelength=1.5, labelspacing=0.2)

        output_path = output_folder_path + '/' + gname + '/'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ax.figure.savefig(output_path + '/throughput-reservoir-' + gname + '-gamma=' + str(gamma) + '.pdf', format='pdf', bbox_inches='tight', dpi=400)
        plt.show(block=False)
        time.sleep(0.5)
        plt.close("all")


