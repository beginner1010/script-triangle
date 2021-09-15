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

graph_names = ['yahoo','bag']
hatches = ['', '\\', '/','\\','+']

colors = ['tomato','mediumseagreen','dodgerblue', 'red', 'blue','k']
alpha= 1.0
width = 1.3 # size of bars in the plot
lw = 6

def get_median_error(reservoirs, processed_edges, df, exact_bfly):
    errors = []
    for rs in reservoirs:
        last_bfly = df['bfly'].loc[(df['batch'] == processed_edges) & (df ['res-sz'] == rs)]
        cur_errors = (abs(last_bfly - exact_bfly) * 100.) / exact_bfly
        errors.append(cur_errors.median())
    return errors

def narrow_down_with_gamma(df, gamma):
    return df.loc[df['gamma'] == gamma]

for gname in graph_names:
    for gamma in [0.5, 0.6, 0.7, 0.8, 0.9]:
        file_name_Res = 'res=[75,600].txt'
        file_name_Ada = 'res=[75,600],gamma=[0.5,0.9].txt'

        Batch_df = pd.read_csv(folder_path + '/' + gname + '/' + 'batch' + '/' + gname + '.txt', sep=',', skipinitialspace=True)
        Res_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Res' + '/' + file_name_Res, sep=',', skipinitialspace=True)
        IRes_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IRes' + '/' + file_name_Res, sep=',', skipinitialspace=True)
        Ada_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Ada' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
        oldAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'oldAda' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
        IAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IAda' + '/' + file_name_Ada, sep=',',skipinitialspace=True)
        Mar_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Mar' + '/' + file_name_Res, sep=',', skipinitialspace=True)

        Ada_df = narrow_down_with_gamma(Ada_df, gamma)
        oldAda_df = narrow_down_with_gamma(oldAda_df, gamma)
        IAda_df = narrow_down_with_gamma(IAda_df, gamma)

        processed_edges = IRes_df['batch'].max()
        reservoirs = sorted(IRes_df['res-sz'].unique())
        iterations = sorted(IRes_df['iteration'].unique())
        batches = sorted(IRes_df['batch'].unique())
        exact_bfly = Batch_df['bfly'].max()

        Res_err = get_median_error(reservoirs, processed_edges, Res_df, exact_bfly)
        IRes_err = get_median_error(reservoirs, processed_edges, IRes_df, exact_bfly)
        Ada_err = get_median_error(reservoirs, processed_edges, Ada_df, exact_bfly)
        oldAda_err = get_median_error(reservoirs, processed_edges, oldAda_df, exact_bfly)
        IAda_err = get_median_error(reservoirs, processed_edges, IAda_df, exact_bfly)

        print(reservoirs)

        x_location = 1
        fig, ax = plt.subplots(figsize=(12, 5))  # plt.figure()

        mx = max(Res_err)
        mx = max(mx, max(IRes_err))
        mx = max(mx, max(Ada_err))
        mx = max(mx, max(oldAda_err))
        mx = max(mx, max(IAda_err))

        algorithms = [r'\textsc{Fleet1}', r'\textsc{Fleet2}', r'\textsc{Fleet3}']

        x_location = 1
        xs = []
        for i in range (0, len(Res_err)):
            xs.append(x_location)
            #ax.bar(x_location - 2 * width, Res_err[i], width, alpha=alpha, hatch=hatches[0], color = colors [0], linewidth=2, edgecolor='k')
            #ax.bar(x_location - width, IRes_err[i], width, alpha=alpha, hatch=hatches[1], color = colors [1], linewidth=2, edgecolor='k')
            ax.bar(x_location - width, oldAda_err[i], width, alpha=alpha, hatch=hatches[0], color=colors[0], linewidth=2, edgecolor='k')
            ax.bar(x_location, Ada_err[i], width, alpha=alpha, hatch=hatches[1], color = colors[1], linewidth=2, edgecolor='k')
            ax.bar(x_location + width, IAda_err[i], width, alpha=alpha, hatch=hatches[2], color=colors[2], linewidth=2, edgecolor='k')

            x_location += 8
            plt.gca().set_prop_cycle(None)

        #ax.plot(xs, Res_err, alpha=alpha, color=colors[0], linewidth=lw, marker=markers[0], linestyle=linestyles[0], markeredgecolor='k')
        #ax.plot(xs, IRes_err, alpha=alpha, color=colors[1], linewidth=lw, marker=markers[1], linestyle=linestyles[1], markeredgecolor='k')
        #ax.plot(xs, Ada_err, alpha=alpha, color=colors[2], linewidth=lw, marker=markers[2], linestyle=linestyles[2], markeredgecolor='k')

        ax.margins(x=0.9)
        plt.ylim((1e-2, mx + 3))
        plt.yscale('log')
        ax.set_ylabel('Error(\%)')
        ax.set_xlabel('Reservoir Size')
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
        #ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

        new_reservoirs = ['{:.2g}'.format(i) for i in reservoirs]

        plt.xticks(xs, new_reservoirs)

        sample_rate = [i / processed_edges * 100 for i in reservoirs]
        ax2_ticks = ['{:.2f}'.format(i) for i in sample_rate]
        #plt.twiny().xticks(xs, ax2_ticks)
        #ax2_ticks = ['{}\%']

        ax.legend(algorithms, fancybox=True, framealpha=1.0, ncol=5, bbox_to_anchor=(-1, -1.05),
                  shadow=True, borderpad=0.2, borderaxespad=0.2, handletextpad=0.3, handlelength=1.5, labelspacing=0.3,
                  columnspacing=2.0, frameon=True)

        plt.xlim([-2, max(xs) + 2.75])

        ax2 = plt.twiny()

        plt.xlim([-2, max(xs) + 2.75])

        plt.xticks(xs, ax2_ticks)
        plt.xlabel('Sample Rate(\%)', labelpad=13)

        output_path = output_folder_path + '/' + gname + '/'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ax.figure.savefig(output_folder_path + '/legends/' + 'error-reservoir' + '.pdf', format='pdf', bbox_inches='tight',
                          dpi=300)
        plt.show(block=False)
        time.sleep(0.5)
        plt.close("all")
        exit(0)


