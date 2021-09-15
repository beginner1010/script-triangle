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
sz = 55


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

def get_MAPE(batches, df, gamma, Batch_df):
    errors = []
    for batch in batches:
        cur_bfly = df['bfly'].loc[(df ['batch'] == batch) & (df ['gamma'] == gamma)]
        exact_bfly = float(Batch_df['bfly'].loc[(Batch_df ['batch'] == batch)])
        cur_errors = abs(cur_bfly - exact_bfly) / exact_bfly * 100.0
        errors.append(cur_errors.median())

    mape = np.mean(errors)
    return mape

def narrow_down_with_reservoir(df, reservoir):
    return df.loc[df['res-sz'] == reservoir]


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

            Ada_err = get_MAPE(batches, Ada_df, gamma, Batch_df)
            oldAda_err = get_MAPE(batches, oldAda_df, gamma, Batch_df)
            IAda_err = get_MAPE(batches, IAda_df, gamma, Batch_df)

            xs.append(x_location)

            ax.bar(x_location - width, oldAda_err, width, alpha=alpha, hatch=hatches[0], color=colors[0], linewidth=2, edgecolor='k')
            ax.bar(x_location, Ada_err, width, alpha=alpha, hatch=hatches[1], color = colors [1], linewidth=2, edgecolor='k')
            ax.bar(x_location + width, IAda_err, width, alpha=alpha, hatch=hatches[2], color=colors[2], linewidth=2, edgecolor='k')

            x_location += 5
            plt.gca().set_prop_cycle(None)

            mx = max(mx, float(Ada_err))
            mx = max(mx, float(oldAda_err))
            mx = max(mx, float(IAda_err))

        ax.margins(x=0.9)
        plt.ylim((0, mx + 1))
        #plt.yscale('log')
        ax.set_ylabel('MAPE')
        ax.set_xlabel(r'${\large \gamma}$', fontsize= 80)
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))

        str_gammas = ['{:.1f}'.format(i) for i in gammas]

        plt.xticks(xs, str_gammas)

        plt.xlim([-width, max(xs) + width + 1])

        output_path = output_folder_path + '/' + gname + '/'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ax.figure.savefig(output_path + '/gamma-error-' + gname + '-reservoir=' + str(reservoir) + '.pdf', format='pdf', bbox_inches='tight', dpi=400)
        plt.show(block=False)
        time.sleep(0)
        plt.close("all")
