def depic_RR(mfa_plastics_ch, mycursor):


    import numpy as np
    import matplotlib.pyplot as plt


    # set width of bars

    barWidth = 0.3


    # set height of bars, and labels

    mycursor.execute("SELECT * "
                     "FROM "
                     "res_opt_scen_only")
    results = mycursor.fetchall()

    labels = []
    RR_total = []
    RR_sc0022 = []
    RR_sc0023 = []
    RR_sc0024 = []

    for i in range(0, len(results)):
        labels.append(results[i][0])  # all plastic types
        RR_total.append(results[i][10])  # recycling rate for all plastic types
        RR_sc0022.append(results[i][13])  # true recycling rate for all plastic types in scenario sc0022
        RR_sc0023.append(results[i][14])  # true recycling rate for all plastic types in scenario sc0023
        RR_sc0024.append(results[i][15])  # true recycling rate for all plastic types in scenario sc0024


    # font size

    fontsize_selected = 12


    # Set position of bar on X axis

    br1 = np.arange(len(labels))
    br2 = [x+barWidth/3 for x in br1]
    br3 = [x+barWidth/3 for x in br2]
    br4 = [x+barWidth/3 for x in br3]


    # Make the plot

    plt.bar(br1, RR_total, color=(149 / 255, 96 / 255, 19 / 255), width=barWidth,
            label='RR')
    plt.bar(br2, RR_sc0022, color=(102 / 255, 175 / 255, 192 / 255), width=barWidth,
            label='TRR - high applicability sub-scenario')
    plt.bar(br3, RR_sc0023, color=(153 / 255, 202 / 255, 213 / 255), width=barWidth,
            label='TRR - moderate applicability sub-scenario')
    plt.bar(br4, RR_sc0024, color=(204 / 255, 228 / 255, 234 / 255), width=barWidth,
            label='TRR - low applicability sub-scenario')


    # Adding Xlabel, Ylabel

    plt.xlabel('Plastic Type', fontweight='bold', fontsize=fontsize_selected)
    plt.ylabel('(True) Recycling Rate ((T)RR) [-]', fontweight='bold', fontsize=fontsize_selected)


    # Adding Xticks, Yticks

    plt.xticks([r+barWidth/2 for r in range(len(labels))],
               labels, fontsize=fontsize_selected)
    plt.yticks(fontsize=fontsize_selected)
    # print([r + barWidth/2 for r in range(len(labels))])


    # Formatting Yaxis

    plt.ylim(0, 0.5)
    plt.gca().set_yticklabels(['{:.0f}%'.format(x * 100) for x in plt.gca().get_yticks()])


    # Formatting figure frame

    for pos in ['right', 'top']:
        plt.gca().spines[pos].set_visible(False)


    # Adding legend

    plt.legend(
        fontsize=fontsize_selected - 2, frameon=False)


    # Saving figure in project folder and showing figure

    plt.savefig("figure_RR.svg")
    plt.savefig("figure_RR.png", dpi=2000, bbox_inches = "tight")

    plt.show()