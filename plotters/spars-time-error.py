from settings import *

def exp_range(start, stop, step):
    while (start < stop):
        yield start
        start *= step
    return

folder_path = '../output'
output_folder_path = '../plots'

graph_names = ['Journal']

colors = ['teal', 'purple']
alpha= 0.6
width = 1 # size of bars in the plot
lw = 12

for gname in graph_names:
    input_file = folder_path + '/' + gname

    df_clr = pd.read_csv(input_file + '/' + 'clr-7iter.txt', sep=' ',skipinitialspace=True, names=['time', 'prob', 'error'])
    df_edg = pd.read_csv(input_file + '/' + 'edgspars-7iter.txt', sep=' ',skipinitialspace=True, names=['time', 'prob', 'error'])
    
    #df_clr = df_clr[3:]
    
    print(df_clr.head(20), df_edg.head(20))
        
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.plot(df_clr['prob'], df_clr['error'], alpha=alpha, color=colors[0], linewidth=lw, marker='o', markersize = 22, markevery=4, linestyle=':', markerfacecolor='deeppink', markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')
    ax.plot(df_edg['prob'], df_edg['error'], alpha=alpha, color=colors[1], linewidth=lw, marker='o', markersize = 22, markevery=4, linestyle=':', markerfacecolor='deeppink', markeredgecolor='k', solid_capstyle='round', dash_capstyle='round')


    ax.margins(x=0)
    #plt.ylim([0.2, 101])
    ax.set_ylabel(r'Error(\%)')
    ax.set_xlabel('Probability $p$')
    
    
    ax.set_yticks([0.01, 1.0, 10.0, 100.0])
    ax.set_xticks([0.004, 0.016, 0.062, 0.25, 1.0])
    
    plt.yscale('log', basey=10)
    #plt.xscale('log', basex=4)
    
    ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))


    # output_path = output_folder_path + '/' + gname + '/'
    # if not os.path.exists(output_path):
        # os.makedirs(output_path)

    #ax.figure.savefig(output_path + '/' + gname + '-spars-error-time.pdf', format='pdf',
    #                  bbox_inches='tight', dpi=400)
    plt.show()
    time.sleep(1)
    plt.close("all")


