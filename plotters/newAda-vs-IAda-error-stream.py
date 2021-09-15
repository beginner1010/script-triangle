import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import ScalarFormatter
import matplotlib.ticker as ticker
import time
import os
import scipy.signal

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

graph_names = ['movie-lens','edit-frwiki','edit-enwiki','yahoo','bag']

linestyles = [':','--','-','-']
markers = ['s', 'o', 'D']
colors = ['tomato','mediumseagreen','dodgerblue', 'red', 'blue','k']

alpha= 0.8
width = 2.0 # size of bars in the plot
lw = 8

def get_median_error(batches, df, reservoir, Batch_df):
    errors = []
    for batch in batches:
        cur_bfly = df['bfly'].loc[(df ['batch'] == batch) & (df ['res-sz'] == reservoir)]
        #print(df.loc[(df ['batch'] == batch) & (df ['res-sz'] == reservoir)])
        exact_bfly = float(Batch_df['bfly'].loc[(Batch_df ['batch'] == batch)])
        cur_errors = abs(cur_bfly - exact_bfly) / exact_bfly * 100.0
        errors.append(cur_errors.median())
    return errors


def narrow_down_with_gamma(df, gamma):
    return df.loc[df['gamma'] == gamma]


for gname in graph_names:
    for reservoir in exp_range(75000, 600 * 1000 + 1, 2):
        for gamma in [0.5, 0.6, 0.7, 0.8, 0.9]:

            if gamma != 0.9 or reservoir != 75 * 1000 or gname != 'yahoo':
                continue

            file_name_Res = 'res=[75,600].txt'
            file_name_Ada = 'res=[75,600],gamma=[0.5,0.9].txt'

            Batch_df = pd.read_csv(folder_path + '/' + gname + '/' + 'batch' + '/' + gname + '.txt', sep=',', skipinitialspace=True)
            IAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IAda' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
            newAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'newAda' + '/' + file_name_Ada, sep=',', skipinitialspace=True)

            IAda_df = narrow_down_with_gamma(IAda_df, gamma)
            newAda_df = narrow_down_with_gamma(newAda_df, gamma)

            processed_edges = IAda_df['batch'].max()
            reservoirs = sorted(IAda_df['res-sz'].unique())
            batches = sorted(IAda_df['batch'].unique())
            exact_bfly = Batch_df['bfly'].max()

            assert sorted(IAda_df['batch'].unique()) == sorted(newAda_df['batch'].unique())

            print(pd.concat([Batch_df['bfly'], newAda_df['bfly'][newAda_df['res-sz'] == reservoir]], axis=1))

            IAda_error = get_median_error(batches, IAda_df, reservoir, Batch_df)
            newAda_error = get_median_error(batches, newAda_df, reservoir, Batch_df)

            fig, ax = plt.subplots(figsize=(8, 5))  # plt.figure()

            IAda_error = scipy.signal.savgol_filter(IAda_error, 9, 3)
            newAda_error = scipy.signal.savgol_filter(newAda_error, 9, 3)

            mx = 0
            mx = max(mx, max(IAda_error))
            mx = max(mx, max(newAda_error))
            #mx = max(mx, max(Mar_error))

            algorithms = ['IAda', 'newAda']

            ax.plot(batches, IAda_error, alpha=alpha, color=colors[0], linewidth=lw, linestyle=linestyles[0], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round', label=algorithms[0])
            ax.plot(batches, newAda_error, alpha=alpha, color=colors[1], linewidth=lw, linestyle=linestyles[1], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round', label=algorithms[1])

            plt.title(r'Yahoo-song, $\gamma$ = {}, and M = {}'.format(gamma, reservoir), pad=13)

            ax.margins(x=0)
            plt.ylim((0, 105 + 0.2))
            ax.set_ylabel('Error(\%)')
            ax.set_xlabel('\# Edges')

            plt.legend()

            ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))

            output_path = output_folder_path + '/' + gname + '/'
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            ax.figure.savefig(output_path + '/newAda-vs-IAda-' + gname + '-gamma=' + str(gamma) + '-res-sz=' + str(reservoir) + '.pdf', format='pdf', bbox_inches='tight', dpi=300)
            plt.show(block=True)
            time.sleep(0.5)
            plt.close("all")


