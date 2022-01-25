def depic_uptaken_sec_mat_scen(mycursor):


    import numpy as np
    import matplotlib.pyplot as plt


    # set width of bars

    barWidth = 0.15


    # set height of bars, and labels

    mycursor.execute("SELECT * "
                     "FROM "
                     "res_opt_scen_only")
    results = mycursor.fetchall()

    labels = []
    sec_mat = []
    sc0022 = []
    sc0023 = []
    sc0024 = []

    for i in range(0, len(results)):
        labels.append(results[i][0])  # all plastic types
        sec_mat.append(results[i][4])  # total secondary material  for all plastic types
        sc0022.append(results[i][1])  # uptaken secondary material for all plastic types in scenario sc0022
        sc0023.append(results[i][2])  # uptaken secondary material for all plastic types in scenario sc0023
        sc0024.append(results[i][3])  # uptaken secondary material for all plastic types in scenario sc0024


    # font size

    fontsize_selected = 20

    """
    font = {'family' : 'normal',
            #'weight' : 'bold',
            'size'   : fontsize_selected}

    matplotlib.rc('font', **font)
    """

    # Set position of bars on x axis

    br1 = np.arange(len(labels))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    br4 = [x + barWidth for x in br3]
    #print(br1, "\n", br2, "\n", br3, "\n", br4)


    # Make the plot

    plt.bar(br1, sec_mat, color=(149 / 255, 96 / 255, 19 / 255), width=barWidth,
            label='total secondary material available')
    plt.bar(br2, sc0022, color=(0, 122 / 255, 150 / 255, 0.6), width=barWidth,
            label='uptaken secondary material - high applicability sub-scenario')
    plt.bar(br3, sc0023, color=(0, 122 / 255, 150 / 255, 0.4), width=barWidth,
            label='uptaken secondary material - moderate applicability sub-scenario')
    plt.bar(br4, sc0024, color=(0, 122 / 255, 150 / 255, 0.2), width=barWidth,
            label='uptaken secondary material - low applicability sub-scenario')


    # Adding Xlabel, Ylabel

    plt.xlabel('Plastic Type', fontweight='bold', fontsize=fontsize_selected)
    plt.ylabel('Secondary Material Amounts [t]', fontweight='bold', fontsize=fontsize_selected)


    # Adding Xticks, Yticks

    plt.xticks([r + 1.5 * barWidth for r in range(len(labels))],
               labels, fontsize=fontsize_selected)
    plt.yticks(fontsize=fontsize_selected)


    # Formatting Yaxis

    plt.ylim(0, 55000)
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in plt.gca().get_yticks()])


    # Formatting figure frame
    for pos in ['right', 'top']:
        plt.gca().spines[pos].set_visible(False)


    # Adding legend
    plt.legend(fontsize=fontsize_selected-3, frameon=False)


    # Saving figure in project folder and showing figure

    plt.savefig("figure_uptaken_secondary_material.svg")
    plt.savefig("figure_uptaken_secondary_material.png", dpi=2000, bbox_inches="tight")

    plt.show()


    # possibly additionally mention share of uptaken secondary material for each sub-scenario for each plastic type

