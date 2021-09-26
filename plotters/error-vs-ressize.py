import os.path

from script_main import *

for gname in graph_names:


    exact_address = os.path.join(folder_path, gname, 'exact', gname + '_' + 'ins_only_exact.txt')
    if os.path.isfile(exact_address) == False: continue
    exact = pd.read_csv(exact_address)
    exact = polish_exact(exact)

    algo_results = get_data_all_algorithms(gname, 'ins_only_stream')

    random_algo_name = list(algo_results.keys())[0]
    processed_edges = algo_results[random_algo_name]['#processed_edges'].max()
    reservoirs = sorted(algo_results[random_algo_name]['reservoir-size'].unique())
    batches = sorted(algo_results[random_algo_name]['#processed_edges'].unique())
    exact_tri = exact['tri'].max()


    # print(processed_edges)
    # print(reservoirs)
    # print(batches)
    # print(exact_tri)

    reservoir_mapes = []
    for reservoir in reservoirs:
        algo_mape = {}
        for algo in algo_results.keys():
            # print(gname, reservoir, algo)
            algo_mape[algo] = compute_MAPE(algo, batches, algo_results[algo], reservoir, exact)
        reservoir_mapes.append(algo_mape)

    batches = [processed_edges]
    x_location = 1
    fig, ax = plt.subplots(figsize=(13, 5))  # plt.figure()
    x_location = 1
    xs = []
    mx = 0
    for reservoir, mape in zip(reservoirs, reservoir_mapes):
        cur_width = - 1.5 * WIDTH
        for idx, algo in enumerate(algo_results.keys()):
            ax.bar(x_location - cur_width, mape[algo], WIDTH, alpha=ALPHA, hatch=hatches[idx], color=colors[idx], linewidth=2, edgecolor='k')
            cur_width += WIDTH
            mx = max(mx, float(mape[algo]))

        xs.append(x_location)
        x_location += X_JUMP
        plt.gca().set_prop_cycle(None)

    # ax.margins
    ax.margins(x=1.0)
    plt.ylim((1e-2, 120))
    plt.yscale('log')
    ax.set_ylabel('MAEP(\%)')
    ax.set_xlabel('Reservoir Size')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

    new_reservoirs = ['{:.2g}'.format(i) for i in reservoirs]

    plt.xticks(xs, new_reservoirs)

    sample_rate = [i / processed_edges * 100 for i in reservoirs]
    ax2_ticks = ['{:.2f}'.format(i) for i in sample_rate]

    plt.xlim([-1, max(xs) + WIDTH + 0.5])

    ax2 = plt.twiny()

    plt.xlim([-1, max(xs) + WIDTH + 0.5])

    plt.xticks(xs, ax2_ticks)
    plt.xlabel('Sample Rate(\%)', labelpad=13)

    output_path = folder_path + '/' + gname + '/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_address = output_path + f'error-reservoir-{gname}.pdf'
    ax.figure.savefig(file_address, format='pdf', bbox_inches='tight', dpi=400)
    plt.show(block=False)

    print(f'{file_address} generated...')
    # time.sleep(0.5)
    plt.close("all")


