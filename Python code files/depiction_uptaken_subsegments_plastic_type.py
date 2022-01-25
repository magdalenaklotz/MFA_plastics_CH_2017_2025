def depic_uptaken_subsegments_plastic_type(plastic_type, mycursor):


    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib


    # set height of bars, and labels

    select_allocated_sec_mat =  ("SELECT * "
                                 "FROM "
                                 "      uptaken_secondary_material_subsegments_plastic_types "
                                 "WHERE "
                                     "  plastic_type = (%s) AND "
                                     "  `subsegment` NOT IN ('variable') AND "
                                     "  scenario = (%s)")
    demand = [[], [], [], []]
    allocated = [[], [], [], []]

    for i in range(0, 3):
        scenario = 'sc' + str(2).zfill(3) + str(i+2)
        #print(scenario)

        mycursor.execute(select_allocated_sec_mat, (plastic_type, scenario))
        results = mycursor.fetchall()
        #print(results)

        labels = []

        for j in range(0, len(results)):
            labels.append(results[j][2])  # subsegments
            demand[i].append(results[j][4])  # maximum secondary material utilizable
            allocated[i].append(results[j][3])  # uptaken secondary material in scenario

    #print(labels)
    #print(demand)
    #print(allocated)


    # font

    font = {'family': 'Times New Roman',
            'weight': 'normal',
            'size': 6.2}

    matplotlib.rc('font', **font)

    fontsize_selected = 6.2


    # setup the plot

    lim_x = 50000

    figur, (ax2, ax3, ax4) = plt.subplots(1, 3, sharex=True, sharey=True)
    plt.xlim(0, lim_x)

    figur.subplots_adjust(bottom=0.1)
    figur.subplots_adjust(left=0.2)

    y_pos = np.arange(len(labels))

    ax2.barh(np.arange(len(labels)), allocated[0], color=(0, 122 / 255, 150 / 255), label='uptaken secondary material', align='center', zorder=2)
    ax2.barh(np.arange(len(labels)), demand[0], align='center', color=(127.5/255, 188.5/255, 202.5/255), label='maximum applicable secondary material', zorder=1)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels, fontsize=fontsize_selected)
    ax2.invert_yaxis()  # labels read top-to-bottom
    ax2.set_xlabel('secondary material amounts [t]', fontsize=fontsize_selected, fontweight='bold')
    ax2.set_title("high applicability sub-scenario", fontsize=fontsize_selected+1.5)
    ax2.yaxis.grid(color='gainsboro')
    ax2.set_axisbelow(True)
    ax2.tick_params(axis='y', direction='in', length=300, color='gainsboro', zorder=10)

    ax3.barh(np.arange(len(labels)), demand[1], align='center', color=(127.5/255, 188.5/255, 202.5/255), zorder=2)
    ax3.barh(np.arange(len(labels)), allocated[1], align='center', color=(0, 122/255, 150/255), zorder=2)
    ax3.invert_yaxis()  # labels read top-to-bottom
    ax3.set_xlabel('secondary material amounts [t]', fontsize=fontsize_selected)
    ax3.set_title("moderate applicability sub-scenario", fontsize=fontsize_selected+1.5)
    ax3.yaxis.grid(color='gainsboro')
    ax3.tick_params(axis='y', direction='in', length=0, color='gainsboro', zorder=10)

    ax4.barh(np.arange(len(labels)), demand[2], align='center', color=(127.5/255, 188.5/255, 202.5/255), zorder=2)
    ax4.barh(np.arange(len(labels)), allocated[2], align='center',color=(0, 122/255, 150/255), zorder=2)
    ax4.invert_yaxis()  # labels read top-to-bottom
    ax4.set_xlabel('secondary material amounts [t]', fontsize=fontsize_selected)
    ax4.set_title("low applicability sub-scenario", fontsize=fontsize_selected+1.5)
    ax4.yaxis.grid(color='gainsboro')
    ax4.tick_params(axis='y', direction='in', length=0, color='gainsboro', zorder=10)

    handles, labels = ax2.get_legend_handles_labels()
    figur.legend(handles, labels, loc='lower right', bbox_to_anchor=(0.285, 0.016), fontsize=fontsize_selected, frameon=False)
    plt.gca().set_xticklabels(['{:,.0f}'.format(x)  for x in plt.gca().get_xticks()])


    # saving figure in project folder and showing figure

    plt.savefig("figure_uptaken_subseg_" + plastic_type + ".svg", bbox_inches = "tight")
    plt.savefig("figure_uptaken_subseg_" + plastic_type + ".png", bbox_inches="tight", dpi=5000)

    plt.show()


    # manually add overall share uptaken secondary material for each sub-scenario