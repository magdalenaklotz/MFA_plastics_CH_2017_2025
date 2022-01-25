def calc_mat_out_from_rec_subsegments(scenario, mycursor):


    import pandas as pd
    import numpy as np


    calc_mat_into_rec_plastic_type_subsegment_process = ("SELECT"
                                             "  scenario_flows, "
                                             " `subsegment_origin_flows`, "
                                             "  plastic_type_flows, "
                                             "  sum(value_flows) "                                             
                                             "FROM "
                                             "  flows "
                                             "WHERE "
                                             "  destination_flows = (%s) and scenario_flows = (%s) "
                                             "GROUP BY"
                                             "  scenario_flows, `subsegment_origin_flows`, plastic_type_flows")

    select_TC = ("SELECT "
                  "     TC "
                  "FROM "
                   "     TCs_definition "
                  "WHERE "
                   "     outflow_destination_LC_stage = '2' and process_concerned = (%s) and (plastic_type = (%s) or plastic_type = 'any') and (inflow_subsegment = (%s) or inflow_subsegment = 'any')")       #and scenario = (%s)


    sec_mat_total = []
    sec_mat_total_pivot = []


    LC_stage = (6, )
    select_processes_on_LC_stage = ("SELECT id_processes FROM processes WHERE life_cycle_stage_number_processes = (%s)")    # select all processes on LC stage recycling
    mycursor.execute(select_processes_on_LC_stage, LC_stage)
    recycling_processes = mycursor.fetchall()
    #print(recycling_processes)

    for process in recycling_processes:
        mycursor.execute(calc_mat_into_rec_plastic_type_subsegment_process, (process[0], scenario))     #calculate total material into single recycling processes for each subsegment from each plastic type
        mat_into_rec_plastic_type_subsegment_process = mycursor.fetchall()
        #print(mat_into_rec_plastic_type_subsegment_process)
        for row in mat_into_rec_plastic_type_subsegment_process:    # for each process (first loop), calculate secondary material for all ingoing flows (this loop, each calculated secondary material flow directly append to final list)
            if (row[3] != None and row[3] != 0):
                parameters = (process[0], row[2], row[1])
                mycursor.execute(select_TC, parameters)     # select TC for respective plastic type in respective process
                TC = mycursor.fetchall()
                if TC != []:    # certain plastic types go into a recycling process, but are then conveyed to energy recovery (e.g. EPS in window profiles), and are thus not specified (only TCs to secondary material specified)
                    amount_sec_mat = row[3] * TC[0][0]
                    sec_mat = (scenario, row[1], row[2], amount_sec_mat)
                    sec_mat_total.append(sec_mat)       # all secondary material flows from all processes stored in one list
    #print(sec_mat_total)

    df = pd.DataFrame(sec_mat_total, columns=['scenario', 'subsegment', 'plastic_type', 'amount_secondary_material'])
    df_grouped = pd.pivot_table(df, index=['scenario', 'subsegment', 'plastic_type'], aggfunc={'amount_secondary_material': np.sum})       # secondary material of one plastic type of one subsegment can come from different recycling processes, here total amount calculated
    #print(df)
    #print(df_grouped)
    for index, row in df_grouped.iterrows():
        scenario = index[0]
        subsegment = index[1]
        plastic_type = index[2]
        amount_secondary_material = float(row['amount_secondary_material'])
        parameters = (scenario, subsegment, plastic_type, amount_secondary_material)
        #print(parameters)
        sec_mat_total_pivot.append(parameters)

    return(sec_mat_total_pivot)