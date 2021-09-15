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

graph_names = ['yahoo','bag','edit-enwiki','edit-frwiki','movie-lens']
hatches = ['', '\\', '/','\\','+']

colors = ['tomato','mediumseagreen','dodgerblue', 'red', 'blue','k']
alpha= 1.0
width = 1.3 # size of bars in the plot
lw = 6

def get_MAPE(batches, df, reservoir, Batch_df):
    errors = []
    for batch in batches:
        cur_bfly = df['bfly'].loc[(df ['batch'] == batch) & (df ['res-sz'] == reservoir)]
        exact_bfly = float(Batch_df['bfly'].loc[(Batch_df ['batch'] == batch)])
        cur_errors = abs(cur_bfly - exact_bfly) / exact_bfly * 100.0
        errors.append(cur_errors.median())

    #print(len(errors))
    mape = np.mean(errors)
    return mape

def narrow_down_with_gamma(df, gamma):
    return df.loc[df['gamma'] == gamma]

for gname in graph_names:
    for gamma in [0.5, 0.6, 0.7, 0.8, 0.9]:
        file_name_Res = 'res=[75,600].txt'
        file_name_Ada = 'res=[75,600],gamma=[0.5,0.9].txt'

        Batch_df = pd.read_csv(folder_path + '/' + gname + '/' + 'batch' + '/' + gname + '.txt', sep=',', skipinitialspace=True)
        Ada_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Ada' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
        oldAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'oldAda' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
        IAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IAda' + '/' + file_name_Ada, sep=',',skipinitialspace=True)

        Ada_df = narrow_down_with_gamma(Ada_df, gamma)
        oldAda_df = narrow_down_with_gamma(oldAda_df, gamma)
        IAda_df = narrow_down_with_gamma(IAda_df, gamma)

        processed_edges = Ada_df['batch'].max()
        reservoirs = sorted(Ada_df['res-sz'].unique())
        batches = sorted(Ada_df['batch'].unique())
        exact_bfly = Batch_df['bfly'].max()


        print(reservoirs)

        batches = [processed_edges]

        x_location = 1
        fig, ax = plt.subplots(figsize=(13, 5))  # plt.figure()

        algorithms = ['Ada1', 'Ada2', 'Ada3']

        x_location = 1
        xs = []
        mx = 0
        for reservoir in reservoirs:
            oldAda_err = get_MAPE(batches, oldAda_df, reservoir, Batch_df)
            Ada_err = get_MAPE(batches, Ada_df, reservoir, Batch_df)
            IAda_err = get_MAPE(batches, IAda_df, reservoir, Batch_df)

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
        plt.ylim((1e-2, 101))
        plt.yscale('log')
        ax.set_ylabel('ARE(\%)')
        ax.set_xlabel('Reservoir Size')
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
        #ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

        new_reservoirs = ['{:.2g}'.format(i) for i in reservoirs]

        plt.xticks(xs, new_reservoirs)

        sample_rate = [i / processed_edges * 100 for i in reservoirs]
        ax2_ticks = ['{:.2f}'.format(i) for i in sample_rate]

        plt.xlim([-1, max(xs) + width + 0.5])

        ax2 = plt.twiny()

        plt.xlim([-1, max(xs) + width + 0.5])

        plt.xticks(xs, ax2_ticks)
        plt.xlabel('Sample Rate(\%)', labelpad=13)

        output_path = output_folder_path + '/' + gname + '/'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ax.figure.savefig(output_path + '/error-reservoir-' + gname + '-gamma=' + str(gamma) + '.pdf', format='pdf', bbox_inches='tight', dpi=400)
        plt.show(block=False)
        time.sleep(0.5)
        plt.close("all")


