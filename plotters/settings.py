import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
import time
import os
import matplotlib.ticker as ticker

rc('text', usetex = True)
rc('font', family='serif')

rc('text', usetex = True)
rc('font', family='serif')

# plot configuration
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['lines.linewidth'] = 5
mpl.rcParams['lines.markersize'] = 14
mpl.rcParams['font.size'] = 48
mpl.rcParams['xtick.labelsize'] = 46
mpl.rcParams['ytick.labelsize'] = 46
mpl.rcParams['legend.fontsize'] = 46
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['legend.framealpha'] = 0.5
mpl.rcParams['figure.figsize'] = [5.2, 3.76]
sz = 46



import os

folder_path = '../plots'

input = {
    'batch' : os.path.join(folder_path, 'batch'),
    'Ada' : os.path.join(folder_path, 'Ada'),
    'IAda' : os.path.join(folder_path, 'IAda'),
    'IRes' : os.path.join(folder_path, 'IRes')
}
