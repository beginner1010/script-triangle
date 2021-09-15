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
output_folder_path = '../tables'


total_bfly = [1197019065804, 601291038864, 2036443879822, 101483757332276, 40817318286263]
graph_names = ['movie-lens','edit-frwiki','edit-enwiki','yahoo','bag']

alpha= 0.8
width = 2.0 # size of bars in the plot
lw = 6

def get_MAPE(batches, df, reservoir, Batch_df):
    errors = []
    for batch in batches:
        cur_bfly = df['bfly'].loc[(df ['batch'] == batch) & (df ['res-sz'] == reservoir)]
        #print(df.loc[(df ['batch'] == batch) & (df ['res-sz'] == reservoir)])
        exact_bfly = float(Batch_df['bfly'].loc[(Batch_df ['batch'] == batch)])
        cur_errors = abs(cur_bfly - exact_bfly) / exact_bfly * 100.0
        errors.append(cur_errors.median())

    mape = np.mean(errors)
    mape_str = '{:.2f}'.format(np.mean(errors))
    return mape_str

def get_Chakra_MAPE(df, reservoir, total_bfly):
    errors = []
    cur_bfly = df['bfly'].loc[(df ['res-sz'] == reservoir)]
    print(cur_bfly)
    abs_error = abs(cur_bfly - total_bfly) / total_bfly * 100.0
    print(abs_error)
    mape_str = '{:.2f}'.format(abs_error.median())
    return mape_str


def narrow_down_with_gamma(df, gamma):
    return df.loc[df['gamma'] == gamma]


for reservoir in exp_range(75000, 600 * 1000 + 1, 2):
    for gamma in [0.5, 0.6, 0.7, 0.8, 0.9]:
        algorithms = ['Graph','Res', 'IRes', 'oldAda', 'Ada', 'IAda', 'Mar', 'Chakra']
        MAPE = pd.DataFrame([], columns=algorithms)
        for graph_idx, gname in enumerate (graph_names):
            file_name_Res = 'res=[75,600].txt'
            file_name_Ada = 'res=[75,600],gamma=[0.5,0.9].txt'

            Batch_df = pd.read_csv(folder_path + '/' + gname + '/' + 'batch' + '/' + gname + '.txt', sep=',',
                                   skipinitialspace=True)
            Res_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Res' + '/' + file_name_Res, sep=',',
                                 skipinitialspace=True)
            IRes_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IRes' + '/' + file_name_Res, sep=',',
                                  skipinitialspace=True)
            Ada_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Ada' + '/' + file_name_Ada, sep=',',
                                 skipinitialspace=True)
            oldAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'oldAda' + '/' + file_name_Ada, sep=',',
                                    skipinitialspace=True)
            IAda_df = pd.read_csv(folder_path + '/' + gname + '/' + 'IAda' + '/' + file_name_Ada, sep=',',
                                  skipinitialspace=True)
            Chakra_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Chakra' + '/' + file_name_Res, sep=',',
                                  skipinitialspace=True)
            Mar_df = pd.read_csv(folder_path + '/' + gname + '/' + 'Mar' + '/' + file_name_Res, sep=',', skipinitialspace=True)

            Chakra_df ['res-sz'] = Chakra_df ['res-sz'] * 2
            print(Chakra_df['res-sz'].unique())

            Ada_df = narrow_down_with_gamma(Ada_df, gamma)
            oldAda_df = narrow_down_with_gamma(oldAda_df, gamma)
            IAda_df = narrow_down_with_gamma(IAda_df, gamma)

            # print(Mar_df.head())


            processed_edges = Res_df['batch'].max()
            reservoirs = sorted(Res_df['res-sz'].unique())
            iterations = sorted(Res_df['iteration'].unique())
            batches = sorted(Res_df['batch'].unique())
            exact_bfly = Batch_df['bfly'].max()

            new_batches = batches  # [b for b in batches if (b > reservoir)]

            Res_error = get_MAPE(new_batches, Res_df, reservoir, Batch_df)
            IRes_error = get_MAPE(new_batches, IRes_df, reservoir, Batch_df)
            Ada_error = get_MAPE(new_batches, Ada_df, reservoir, Batch_df)
            oldAda_error = get_MAPE(new_batches, oldAda_df, reservoir, Batch_df)
            IAda_error = get_MAPE(new_batches, IAda_df, reservoir, Batch_df)
            Mar_error = get_MAPE(new_batches, Mar_df, reservoir, Batch_df)

            Chakra_error = get_Chakra_MAPE(df=Chakra_df, reservoir=reservoir, total_bfly=total_bfly[graph_idx])

            #algorithms = ['Graph', 'Res', 'IRes', 'oldAda', 'Ada', 'IAda', 'Mar', 'Chakra']
            MAPE.loc[graph_idx] = [gname, Res_error, IRes_error, oldAda_error, Ada_error, IAda_error, Mar_error, Chakra_error]
            # Mar_error = get_median_error(new_batches, Mar_df, reservoir, Batch_df)

        output_path = output_folder_path + '/' + 'MAPE'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        MAPE.to_csv(output_path + '/' + 'gamma=' + str(gamma) + '-res-sz=' + str(reservoir) + '.csv', sep=',')
