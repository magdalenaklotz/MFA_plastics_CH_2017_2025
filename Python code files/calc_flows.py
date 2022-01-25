def calc_flows(from_LC_stage, to_LC_stage, scenario, mfa_plastics_ch, mycursor):    # calculating flows via TCs


    import numpy as np
    import pandas as pd


    select_processes_on_LC_stage = ("SELECT "
                                    "   id_processes "
                                    "FROM "
                                    "   processes "
                                    "WHERE "
                                    "   life_cycle_stage_number_processes = (%s)")

    select_inflows_calc = ("SELECT "
                           "    id_flows, "
                           "    value_flows "
                           "FROM "
                           "    flows "
                           "WHERE "
                           "    destination_flows = (%s) AND "
                           "    scenario_flows = (%s) AND "
                           "    (value_flows > 0 or value_flows < 0)")

    select_TC_calc = ("SELECT "
                      "     TC, "
                      "     outflow "
                      "FROM "
                      "     TCs "
                      "WHERE "
                      "     inflow = (%s) AND "
                      "     scenario = (%s)")

    write_outflow_into_db = ("UPDATE flows "
                             "SET"
                             "  value_flows = (%s) "
                             "WHERE"
                             "  id_flows = (%s) AND "
                             "  scenario_flows = (%s)")


    for i in range(from_LC_stage, to_LC_stage):
        LC_stage = (i, )
        outflows = []
        flows_one_stage = []

        mycursor.execute(select_processes_on_LC_stage, LC_stage)
        processes_on_LC_stage = mycursor.fetchall()
        for process in processes_on_LC_stage:
                mycursor.execute(select_inflows_calc, (process[0], scenario))
                flows_one_stage.extend(mycursor.fetchall()) # gives one list for each destination process (i.e. one of the processes on the concerned LC stage), these lists are collected in one list (result is one single list, not several lists in one list); result is one list with all ingoing flows to processes on concerned LC stage (stored in flows_one_stage)
        for flow in flows_one_stage:
            inflow_id = flow[0]
            mycursor.execute(select_TC_calc, (inflow_id, scenario)) # searching all outflows into which inflow is going, for each inflow stored in flows_one_stage
            TC_outflow = mycursor.fetchall()
            for row_TC_outflow in TC_outflow:
                    outflow_value = row_TC_outflow[0] * flow[1]   # TC * inflow_value
                    outflow_id = row_TC_outflow[1]
                    outflows.append((outflow_value, outflow_id, scenario))  # after having calculated all outflow values, storing them with outflow ids in one list
        df = pd.DataFrame(outflows, columns=['outflow_value', 'outflow_id', 'scenario'])
        df_grouped = pd.pivot_table(df, index=['outflow_id'], aggfunc={'outflow_value': np.sum})    # some outflows have several inflows as input (e.g. food bottles from both hollow bodies and mixed plastics bags collection go into sorting mixed plastics abroad and from there to recycling rigids abroad) -> they are summed up to the final value of the respective outflow (result is each row one outflow with respective final value)
        for index, row in df_grouped.iterrows():
            outflow_id = index
            outflow_value = float(row['outflow_value'])
            parameters = (outflow_value, outflow_id, scenario)
            #print(parameters)
            mycursor.execute(write_outflow_into_db, parameters)
            mfa_plastics_ch.commit()