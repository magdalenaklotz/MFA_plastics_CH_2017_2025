def calc_rec_losses(mfa_plastics_ch, mycursor):


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

    select_TCs = ("SELECT "
                    "     TC, "
                  "       outflow_destination "
                    "FROM "
                    "     TCs_definition "
                    "WHERE "
                    "     outflow_destination_LC_stage not in ('2') and process_concerned = (%s) and (plastic_type = (%s) or plastic_type = 'any') and (inflow_subsegment = (%s) or inflow_subsegment = 'any')")       #and scenario = (%s)

    add_flow = ("INSERT INTO `flows`"
                "(`id_flows`, `origin_flows`, `subsegment_origin_flows`, `destination_flows`, `subsegment_destination_flows`, `plastic_type_flows`, `year_flows`, `value_flows`, `scenario_flows`)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")


    LC_stage = (6, )
    select_processes_on_LC_stage = ("SELECT id_processes FROM processes WHERE life_cycle_stage_number_processes = (%s)")    # select all processes on LC stage recycling
    mycursor.execute(select_processes_on_LC_stage, LC_stage)
    recycling_processes = mycursor.fetchall()
    #print(recycling_processes)

    for process in recycling_processes:
        mycursor.execute(calc_mat_into_rec_plastic_type_subsegment_process, (process[0], 'sc0001'))     #calculate total material into single recycling processes for each subsegment from each plastic type
        mat_into_rec_plastic_type_subsegment_process = mycursor.fetchall()
        #print(mat_into_rec_plastic_type_subsegment_process)
        for row in mat_into_rec_plastic_type_subsegment_process:
            if (row[3] != None and row[3] != 0):
                parameters = (process[0], row[2], row[1])
                mycursor.execute(select_TCs, parameters)     # select TC to energy recovery processes (can be more than one process) for respective plastic type in respective process
                TCs = mycursor.fetchall()
                if TCs != []:
                    for line in TCs:    # calculate amount of each flow to energy recovery via respective TC and insert flow into db
                        loss_amount = row[3] * line[0]
                        mycursor.execute("SELECT max(id_flows) "
                                         "FROM flows")
                        max_id_flows = mycursor.fetchall()
                        new_max_number = int(max_id_flows[0][0][2:]) + 1
                        id_flows = 'fl' + str(new_max_number).zfill(10)
                        loss = (id_flows, process[0], row[1], line[1], row[1], row[2], 2017, loss_amount, 'sc0001')
                        mycursor.execute(add_flow, loss)
                        mfa_plastics_ch.commit()