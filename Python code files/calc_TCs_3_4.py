def calc_TCs_3_4(mfa_plastics_ch, mycursor):


    scenario = 'sc0001'


    select_processes_on_LC_stage = ("SELECT id_processes FROM processes WHERE life_cycle_stage_number_processes = (%s)")

    fetch_connected_flows_several_in = ("SELECT "
                                        "id_inflow, "
                                        "value_inflow_sum, "
                                        "id_flows AS 'id_outflow', "
                                        "value_flows AS 'value_outflow', "
                                        "`subsegment_origin_flows`, "  # not needed (= subsegment_inflow)
                                        "`subsegment_inflow`, "
                                        "plastic_type_flows, "  # not needed (= plastic_type_inflow)
                                        "plastic_type_inflow, "
                                        "scenario_flows, "
                                        "concerned_process, "
                                        "origin_flows, "  # not needed (= concerned process)
                                        "destination_flows "
                                        "FROM "
                                        "(SELECT "
                                        "id_flows as 'id_inflow', "
                                        "value_inflow_sum, "
                                        "concerned_process, "
                                        "`subsegment_inflow`, "
                                        "plastic_type_inflow, "
                                        "scenario_inflow "
                                        "FROM "
                                        "(SELECT "
                                        "sum(value_flows) AS 'value_inflow_sum', "  # for sorting, if one subsegment from one plastic type comes to one sorting process from different collection systems (e.g. food bottles from hollow bodies and mixed plastics bag collections to mixed plastics sorting abroad; or flow into Use from import and manufacturing CH)
                                        "destination_flows AS 'concerned_process', "
                                        "`subsegment_destination_flows` AS 'subsegment_inflow', "
                                        "plastic_type_flows AS 'plastic_type_inflow', "
                                        "scenario_flows AS 'scenario_inflow' "
                                        "FROM "
                                        "flows "
                                        "WHERE "
                                        "destination_flows = (%s) "
                                        "GROUP BY `subsegment_inflow`, plastic_type_inflow, concerned_process, scenario_inflow) t1  "
                                        "INNER JOIN "
                                        "flows t2 "  # wenn mehrere Eingangsflüsse, wird jedem einzelnen (jeder id) die Summe aller eingehenden Flüsse (dieses subsegments und plastic types) zugeordnet
                                        "ON t1.concerned_process = t2.destination_flows "
                                        "WHERE "
                                        "`subsegment_origin_flows` = `subsegment_inflow` AND "
                                        "plastic_type_flows = plastic_type_inflow) t3 "
                                        "INNER JOIN "
                                        "flows t4 "
                                        "ON "
                                        "t3.concerned_process = t4.origin_flows "  # connection of each inflow to outflow (works also for several outflows, then several rows created - same inflow in each row with respective outflow)
                                        "WHERE "
                                        "`subsegment_inflow` = `subsegment_origin_flows` AND "
                                        "plastic_type_inflow = plastic_type_flows AND "
                                        "scenario_inflow = scenario_flows AND "
                                        "scenario_flows = (%s)")

    insert_into_TCs = ("INSERT INTO "
                       "TCs "
                       "(inflow, outflow, scenario, TC, source) "
                       "VALUES "
                       "((%s), (%s), (%s), (%s), (%s))")


    for i in range(3, 4 + 1):  # 3 for use, 4 for separate collection

        parameter = (i,)

        mycursor.execute(select_processes_on_LC_stage, parameter)
        processes_on_LC_stage = mycursor.fetchall()
        #print(processes_on_LC_stage)
        for process in processes_on_LC_stage:
            #print((process[0], scenario))
            mycursor.execute(fetch_connected_flows_several_in, (process[0], scenario))
            connected_flows = mycursor.fetchall()
            #print(connected_flows)

            for row in connected_flows:
                if row[1] != 0:  # if inflow different from 0 (value inflow always >0 also if negativ net import into use, because sum of all inflows)
                    TC = row[3] / row[1]
                    inflow_id = row[0]  # same TC for all inflows to process, individual of course for destination processes (i.e. individual TCs for sum(in) to individual destination processes)
                    outflow_id = row[2]
                    scen = row[8]
                    parameters = (inflow_id, outflow_id, scen, TC, 'NULL')
                    mycursor.execute(insert_into_TCs, parameters)
                    mfa_plastics_ch.commit()