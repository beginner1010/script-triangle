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

graph_names = ['yahoo']

linestyles = [':','--','-','-']
markers = ['s', 'o', 'D']
colors = ['tomato','mediumseagreen','dodgerblue', 'red', 'blue','k']

alpha= 0.8
width = 2.0 # size of bars in the plot
lw = 19

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
            file_name_Res = 'res=[75,600].txt'
            file_name_Ada = 'res=[75,600],gamma=[0.5,0.9].txt'

            Batch_df = pd.read_csv(folder_path + '/' + gname + '/' + 'batch' + '/' + gname + '.txt', sep=',', skipinitialspace=True)
            Res_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Res' + '/' + file_name_Res, sep=',', skipinitialspace=True)
            IRes_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IRes' + '/' + file_name_Res, sep=',', skipinitialspace=True)
            Ada_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Ada' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
            oldAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'oldAda' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
            IAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IAda' + '/' + file_name_Ada, sep=',', skipinitialspace=True)
            Mar_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Mar' + '/' + file_name_Res, sep=',', skipinitialspace=True)

            Ada_df = narrow_down_with_gamma(Ada_df, gamma)
            oldAda_df = narrow_down_with_gamma(oldAda_df, gamma)
            IAda_df = narrow_down_with_gamma(IAda_df, gamma)

            print(Mar_df.head())

            processed_edges = Res_df['batch'].max()
            reservoirs = sorted(Res_df['res-sz'].unique())
            iterations = sorted(Res_df['iteration'].unique())
            batches = sorted(Res_df['batch'].unique())
            exact_bfly = Batch_df['bfly'].max()

            new_batches = batches #[b for b in batches if (b > reservoir)]

            Res_error = get_median_error(new_batches, Res_df, reservoir, Batch_df)
            IRes_error = get_median_error(new_batches, IRes_df, reservoir, Batch_df)
            Ada_error = get_median_error(new_batches, Ada_df, reservoir, Batch_df)
            oldAda_error = get_median_error(new_batches, oldAda_df, reservoir, Batch_df)
            IAda_error = get_median_error(new_batches, IAda_df, reservoir, Batch_df)
            Mar_error = get_median_error(new_batches, Mar_df, reservoir, Batch_df)

            fig, ax = plt.subplots(figsize=(8, 5))  # plt.figure()

            #interval_size = inter # only 6 points are printed

            mx = max(Res_error)
            mx = max(mx, max(IRes_error))
            mx = max(mx, max(Ada_error))
            mx = max(mx, max(oldAda_error))
            mx = max(mx, max(IAda_error))
            #mx = max(mx, max(Mar_error))

            algorithms = [r'\textsc{Fleet1}', r'\textsc{Fleet2}', r'\textsc{Fleet3}']

            #ax.plot(new_batches, scipy.signal.savgol_filter(Res_error, 9, 3), alpha=alpha, color=colors[0], linewidth=lw, linestyle=linestyles[0], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
            #ax.plot(new_batches, scipy.signal.savgol_filter(IRes_error, 9, 3), alpha=alpha, color=colors[1], linewidth=lw, linestyle=linestyles[0], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
            ax.plot(new_batches, scipy.signal.savgol_filter(oldAda_error, 9, 3), alpha=alpha, color=colors[0], linewidth=lw, linestyle=linestyles[0], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
            ax.plot(new_batches, scipy.signal.savgol_filter(Ada_error, 9, 3), alpha=alpha, color=colors[1], linewidth=lw, linestyle=linestyles[1], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
            ax.plot(new_batches, scipy.signal.savgol_filter(IAda_error, 9, 3), alpha=alpha, color=colors[2], linewidth=lw, linestyle=linestyles[2], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
            #ax.plot(new_batches, scipy.signal.savgol_filter(Mar_error, 9, 3), alpha=alpha, color=colors[5], linewidth=lw, linestyle=linestyles[0], markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')

            ax.margins(x=0)
            plt.ylim((0, mx))
            ax.set_ylabel('Error(\%)')
            ax.set_xlabel('\# Edges')

            ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
            #ax.tick_params(axis='x', which='major', pad=13)
            #ax.tick_params(axis='y', which='major', pad=5)
            #ax.xaxis.set_major_locator(ticker.MultipleLocator(1000))
            #ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
            #ax.xaxis.set_major_formatter(plt.MaxNLocator(3))


            ax.legend(algorithms, fancybox=True, framealpha=1.0, ncol=5, bbox_to_anchor=(-1, -1.05),
                   shadow=True, borderpad=0.2, borderaxespad=0.2, handletextpad=0.3, handlelength=3, labelspacing=0.3,
                      columnspacing = 2.0, frameon=True)


            output_path = output_folder_path + '/' + gname + '/'
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            #ax.figure.savefig(output_path + '/error-stream-linear-' + gname + '-gamma=' + str(gamma) + '-res-sz=' + str(reservoir) + '.pdf', format='pdf', bbox_inches='tight', dpi=300)
            ax.figure.savefig(output_folder_path + '/legends/' + 'error-stream' + '.pdf', format='pdf', bbox_inches='tight', dpi=300)

            plt.show(block=False)
            time.sleep(0.5)
            plt.close("all")

            exit(0)


