def calc_TCs_5_other_than_pack(mfa_plastics_ch, mycursor):


    select_processes_on_LC_stage = ("SELECT id_processes FROM processes WHERE life_cycle_stage_number_processes = (%s)")

    fetch_connected_flows = ("SELECT "
                                 "id_inflow, "
                                 "value_inflow, "
                                 "id_flows AS 'id_outflow', "
                                 "value_flows AS 'value_outflow', "
                                 "`subsegment_origin_flows`, "
                                 "`subsegment_inflow`, "
                                 "plastic_type_flows, "
                                 "plastic_type_inflow, "
                                 "scenario_flows, "
                                 "concerned_process, "
                                 "origin_flows, "
                                 "destination_flows "
                            "FROM "
                                 "(SELECT "
                                    "id_flows AS 'id_inflow', "
                                    "value_flows AS 'value_inflow', "
                                    "destination_flows AS 'concerned_process', "
                                    "`subsegment_destination_flows` AS 'subsegment_inflow', "
                                    "plastic_type_flows AS 'plastic_type_inflow', "
                                    "scenario_flows AS 'scenario_inflow' "
                                 "FROM "
                                    "flows "
                                 "WHERE "
                                    "destination_flows = (%s) AND "
                                    "scenario_flows = 'sc0001') t1 "
                                 "INNER JOIN "
                                 "flows t2 "
                                 "ON "
                                    "t1.concerned_process = t2.origin_flows "
                                 "WHERE "
                                 "`subsegment_inflow` = `subsegment_origin_flows` AND "
                                 "plastic_type_inflow = plastic_type_flows AND "
                                 "scenario_inflow = scenario_flows ")

    insert_into_TCs = ( "INSERT INTO "
                                "TCs "
                                "(inflow, outflow, scenario, TC, source) "
                            "VALUES "
                                "((%s), (%s), (%s), (%s), (%s))")


    parameter = (5,)  # for sorting

    mycursor.execute(select_processes_on_LC_stage, parameter)
    processes_on_LC_stage = mycursor.fetchall()
    #print(processes_on_LC_stage, processes_on_LC_stage[6:12])

    for process in processes_on_LC_stage[6:12]:
        mycursor.execute(fetch_connected_flows, process)
        connected_flows = mycursor.fetchall()
        #print(connected_flows)

        for row in connected_flows:
            if row[1] != 0:
                #print(process)
                #print(row[3], row[1])
                TC = row[3] / row[1]
                inflow_id = row[0]
                outflow_id = row[2]
                scenario = row[8]
                parameters = (inflow_id, outflow_id, scenario, TC, 'NULL')
                #print(parameters)
                mycursor.execute(insert_into_TCs, parameters)
                mfa_plastics_ch.commit()


