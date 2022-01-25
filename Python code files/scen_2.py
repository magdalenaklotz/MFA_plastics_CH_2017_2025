def scen_2(mfa_plastics_ch, mycursor):


    # create scenario

    mycursor.execute("DELETE FROM "
                     "  scenarios "
                     "WHERE "
                     "  id_scenarios = 'sc0002'")

    scen_description = '80%_collection_2025'
    scenario = 'sc0002'
    year = 2025     # year based on next EU target of 50% plastics packaging recycling rate (before extruder losses) in 2025 (Packaging Directive)

    insert_into_scenarios = ("INSERT INTO scenarios (id_scenarios, name_scenarios) VALUES ((%s), (%s))")
    mycursor.execute(insert_into_scenarios, (scenario, scen_description))
    mfa_plastics_ch.commit()


    # create flows

    from create_flows import create_all_flows_scenario
    create_all_flows_scenario(scenario, year, mfa_plastics_ch, mycursor)


    # retrieving total use amounts for each subsegment from each plastic type for sc0001

    get_total_use_amount_subsegment_plastic = ("SELECT "
                                                "   scenario_flows, "
                                                "   `subsegment_origin_flows`, "
                                                "   plastic_type_flows, "
                                                "   sum(value_flows) "
                                                "FROM "
                                                "   flows "
                                               "WHERE "
                                               "    scenario_flows = 'sc0001' AND "
                                               "    destination_flows = 'pr0008' AND "
                                               "    `subsegment_origin_flows` = (%s) AND "
                                               "    plastic_type_flows = (%s)")


    # write same use amounts into db for sc0002 as for sc0001, (optionally) with scaling factor

    # scaling_factor_use = 1  # if should be same as in 2017
    scaling_factor_use = 9058337/8419550      # scaling with population possible for constant per-capita consumption, calculation: estimated population CH in 2025 / population CH in 2017 (from BFS, "ständige Wohnbevölkerung")

    select_flow_value_origin = ("SELECT "
                                "   origin_flows, value_flows "
                                "FROM "
                                "   flows "
                                "WHERE "
                                "  scenario_flows = (%s) AND "
                                "  `subsegment_origin_flows` = (%s) AND "
                                "  plastic_type_flows = (%s) AND "
                                "  destination_flows = (%s)")

    insert_flow_value = ("UPDATE "
                         "  flows "
                         "SET "
                         "  value_flows = (%s) "
                         "WHERE "
                         "  scenario_flows = (%s) AND "
                         "  `subsegment_origin_flows` = (%s) AND "
                         "  plastic_type_flows = (%s) AND "
                         "  destination_flows = (%s) AND "
                         "  origin_flows = (%s)")

    for i in range(1, (54+1)):
        for j in range(1, (11+1)):
            subsegment = 'su' + str(i).zfill(4)
            plastic_type = 'pl' + str(j).zfill(4)
            parameters = ('sc0001', subsegment, plastic_type, 'pr0008')
            mycursor.execute(select_flow_value_origin, parameters)
            flows = mycursor.fetchall()
            #print(flows)
            for row in flows:   # 2 rows, one from Import, one from Manufacturing CH
                parameters_scenario = (row[1]*scaling_factor_use, scenario, subsegment, plastic_type, 'pr0008', row[0])
                mycursor.execute(insert_flow_value, parameters_scenario)

    mfa_plastics_ch.commit()


    # calculate TCs for Use so that shares to single Collection processes same as for sc0001 and total collection rate = as defined here

    # get all current (for sc0001) TCs from Use to Collection (not Incineration or Export or Unknown destiny); flows to bulky goods collection not selected, because assumed all recycled waste from this collection collected via alternative specific collection systems

    get_TCs_scen_1_use_col = (  "SELECT "                                        
                                    "   origin_flows AS 'origin_inflow', "
                                    "   concerned_process, "
                                    "   `subsegment_destination_flows`, "
                                    "   plastic_type_flows, "
                                    "   destination_outflow, "
                                    "   inflow, "
                                    "   outflow, "
                                    "   TC "
                                    "FROM "
                                    "   (SELECT "
                                    "       origin_flows as 'concerned_process', "
                                    "       destination_flows as 'destination_outflow', "
                                    "       inflow, "
                                    "       outflow, "
                                    "       TC, "
                                    "       scenario "
                                    "     FROM "
                                    "       TCs "
                                    "       INNER JOIN "
                                    "       flows "
                                    "       ON TCs.outflow = flows.id_flows) as t1 "
                                    "   INNER JOIN flows "
                                    "   on t1.inflow = flows.id_flows "
                                    "WHERE TC >0 and scenario = 'sc0001' and concerned_process = 'pr0008' and destination_outflow not in ('pr0029', 'pr0002', 'pr0003', 'pr0034') " # only flows to collection processes, not to energy recovery or export or unknown destiny or bulky goods
                                    "ORDER BY concerned_process, origin_inflow, `subsegment_destination_flows`, plastic_type_flows, destination_outflow")

    mycursor.execute(get_TCs_scen_1_use_col)
    TCs_use = mycursor.fetchall()
    #print(TCs_use)

    insert_into_TCs = ( "INSERT INTO "
                            "TCs "
                            "(inflow, outflow, scenario, TC, source) "
                        "VALUES "
                            "((%s), (%s), (%s), (%s), (%s))")

    select_flow_id = ("SELECT "
                     "  id_flows "
                     "FROM "
                     "  flows "
                     "WHERE "
                     "  `subsegment_origin_flows` = (%s) AND "
                     "  plastic_type_flows = (%s) AND "
                     "  origin_flows = (%s) AND "
                     "  destination_flows = (%s) AND "
                     "  scenario_flows = (%s)")

    select_waste = ("SELECT "                               # all waste incl. incineration and export and unknown destiny (and bulky goods)
                        "   scenario_flows, "
                        "   `subsegment_origin_flows`, "
                        "   plastic_type_flows, "
                        "   sum(value_flows) "
                        "FROM "
                        "   flows "
                        "WHERE "
                        "   scenario_flows = 'sc0001' AND "
                        "   origin_flows = 'pr0008' AND "
                        "   `subsegment_origin_flows` = (%s) AND "
                        "   plastic_type_flows = (%s)")
    waste_scen2 = []

    for i in range(1, (54+1)):
        for j in range(1, (11+1)):
            subsegment = 'su' + str(i).zfill(4)
            plastic_type = 'pl' + str(j).zfill(4)

            collection_rate_target = 0.80
            collection_rate = collection_rate_target
            # collection rate = input("collection rate?")

    # of most subsegments, a small share, but representative regarding composition for whole waste from this segment collected (same composition as total waste)
    # for some subsegments, which are heterogeneous, today only a specific share of the total waste is collected, which is specifically suitable for recycling; this was considered by only assuming 80% collection of this specific share of total waste (which is suitable for recycling and to which TCs in model apply)

            if subsegment == 'su0012' or subsegment == 'su0014' or subsegment == 'su0017' or subsegment == 'su0018':      # NC packaging rigids assumed heterogeneous, and thus TCs only valid for part of this waste - assumed only for 50% and that 80% of respective share of waste to which TCs apply are collected (rest: possibly multi-material etc.)
                collection_rate = 0.5 * collection_rate_target

            if subsegment == 'su0023':      # result in scaling factor > 1, because bulky goods collection not included as separate collection for share total collection
                if plastic_type == 'pl0001':
                    collection_rate = 0.36 * collection_rate_target  # 36% of all waste from HDPE pipes (su0023) are HDPE cable conduits, 80% or these collected; collection of respective pipes increased, since TCs refer to those (others are e.g. from multi-material or contaminated or not collected for other reasons)
                elif plastic_type == 'pl0004':
                    collection_rate = 0.26 * collection_rate_target   # 26% of all PP pipes waste are PP cable conduits, TCs refer to those
                else:
                    collection_rate = 0     # if LDPE mixed with HDPE in cable conduits, it is also collected, this was neglected

            if subsegment == 'su0029':
                if plastic_type == 'pl0004':
                    collection_rate = (1-0.53) * 0.10/0.289 * collection_rate_target / 0.019     # exported waste modelled to still be exported; 10% (assumption based on Patil et al. (2017)) of all plastic waste from automotive (su0029) is PP bumpers and 28.9% of all plastic waste from automotive is PP, thus, about 1/3 (10% / 28.9%) of all PP waste from automotive is PP bumper waste which is collected (80% of it); already 100% of vehicles not exported are collected today, and losses arise at sorting (efficiency = 0.019), thus, colletion amount artficially scaled up (divided by 0.019, in order to reach a share of 0.1/0.289 * 0.8 (corresponding to dismantled bumpers of 80% of all ELVs not exported) of collected vehicles going to recycling, so resulting in an (artificial) collection rate of >100%); actually TC for sorting to recycling for automotive changes, and newly (overall) amounts to 0.1*0.8=0.08, but for the sake of convenience, the described calculation method, delivering the same amount of secondary material, was applied;
                else:
                    collection_rate = 0

            # get use and waste amounts for 2025

            mycursor.execute(get_total_use_amount_subsegment_plastic, (subsegment, plastic_type))
            use = mycursor.fetchall()
            if use[0][3] is not None and use[0][3] != 0:
                #print(use[0][3], "sc factor:", scaling_factor_use)
                use_scaled = use[0][3] * scaling_factor_use
                #print(use[0][3], use_scaled, subsegment, plastic_type)

                mycursor.execute(select_waste, (subsegment, plastic_type))      # includes all waste (going to collection, incineration and export)
                waste = mycursor.fetchall()
                if waste[0][3] is not None and waste[0][3] != 0:
                    if subsegment == 'su0023' or subsegment == 'su0024' or subsegment == 'su0025' or subsegment == 'su0026' or subsegment == 'su0027' or subsegment == 'su0028':
                        av_lifetime = 33
                        waste_scaling_factor = (use[0][3] * (1- ((2017-(year-av_lifetime))/(2017-1950)))) / waste[0][3]     # average lifetime for B&C used (alternatively, individual lifetimes for B&C subsegments could be used), assuming waste in 2025 corresponds to Use amounts of (2025-33), i.e.1992; assuming linear increase of use amounts from 0 in 2050 to the amount of 2017 in 2017
                    elif subsegment == 'su0029':
                        av_lifetime = 12
                        waste_scaling_factor = (use[0][3] * (1 - ((2017 - (year - av_lifetime)) / (2017 - 1950)))) / waste[0][3]
                    elif subsegment == 'su0030' or subsegment == 'su0031' or subsegment == 'su0032' or subsegment == 'su0033' or subsegment == 'su0034':
                        av_lifetime = 8
                        waste_scaling_factor = use[0][3] * (1 + (scaling_factor_use - 1) * (1 - av_lifetime / (year - 2017))) / waste[0][3]     # average lifetime for EEE used (alternatively, individual lifetimes for B&C subsegments could be used), assuming waste in 2025 corresponds to Use amounts of (2025-8), i.e.2017; assuming linear increase of use amounts from amount in 2017 to the amount of 2025
                    elif subsegment == 'su0035' or subsegment == 'su0036' or subsegment == 'su0037' or subsegment == 'su0038' or subsegment == 'su0039' or subsegment == 'su0040':
                        av_lifetime = 4
                        waste_scaling_factor = use[0][3] * (1 + (scaling_factor_use - 1) * (1 - av_lifetime / (year - 2017))) / waste[0][3]     # average lifetime for agriculture used (alternatively, individual lifetimes for B&C subsegments could be used), assuming waste in 2025 corresponds to Use amounts of (2025-4), i.e.2021; assuming linear increase of use amounts from amount in 2017 to the amount of 2025
                    elif subsegment == 'su0041' or subsegment == 'su0042' or subsegment == 'su0043' \
                            or subsegment == 'su0044' or subsegment == 'su0045' or subsegment == 'su0046' \
                            or subsegment == 'su0047' or subsegment == 'su0048' or subsegment == 'su0049' \
                            or subsegment == 'su0050' or subsegment == 'su0051' or subsegment == 'su0052' \
                            or subsegment == 'su0053' or subsegment == 'su0054':
                        av_lifetime = 5
                        waste_scaling_factor = use[0][3] * (1 + (scaling_factor_use - 1) * (1 - av_lifetime/(year-2017))) / waste[0][3]     # average lifetime for Other and Textiles used (alternatively, individual lifetimes for B&C subsegments could be used), assuming waste in 2025 corresponds to Use amounts of (2025-5), i.e.2020; assuming linear increase of use amounts from amount in 2017 to the amount of 2025
                    else:
                        waste_scaling_factor = scaling_factor_use
                    waste_scaled = waste[0][3] * waste_scaling_factor       # increase of waste amounts estimated via lifetime-based calculation and estimation of past consumption amounts
                    #print(subsegment, 'waste scaling factor:', waste_scaling_factor, 'scaled waste:', waste_scaled, 'waste:', waste[0][3], 'use:', use[0][3])
                    waste_scen2.append((subsegment, plastic_type, waste_scaled))
                    #print('waste scen2 \n', waste_scen2)
                    #print(waste[0][3], subsegment, plastic_type)

                # collect all TCs for one subsegment from one plastic type in one list (come from Import and Manufacturing CH and go to different Collection processes)

                paths = []
                for row in TCs_use:
                    if row[2] == subsegment and row[3] == plastic_type:
                        paths.append(row)
                #print(paths)

                share_total_collection = 0
                for row in paths:
                    if row[0] == 'pr0007':      # TC refers to sum of flows from pr0006 (import) and pr0007 (manufacturing CH), thus, same TC in list for both flows, but only once needed (could also be pr0006 instead of pr0007)
                        share_total_collection = share_total_collection + row[7]
                #print(subsegment, plastic_type, share_total_collection * use[0][3]/waste[0][3], "use scaled:", use_scaled, "waste scaled:", waste_scaled)

                if share_total_collection > 0:
                    scaling_factor = collection_rate / (share_total_collection * use[0][3]/waste[0][3])
                    #print(subsegment, plastic_type, share_total_collection, "use scaled:", use_scaled, "waste scaled:", waste_scaled)
                    if scaling_factor > 1:
                        scaling_factor_used = scaling_factor
                    else:       #for all EEE subsegments and PET in food and hospitality bottles collection rate already above 80% and thus scaling factor <1 results;
                        #print(subsegment, scaling_factor)
                        scaling_factor_used = 1

                    for row in paths:

                        TC_scen_2 = (row[7] * use[0][3]/waste[0][3]) * scaling_factor_used * (waste_scaled / use_scaled)       # collection amounts calculated based on use, not waste amount, while collection rate refers to waste amounts; for bulky goods collection, no TCs specified in this way for scenario 2 (this collection not included in TC table from above, thus, no flows go there and no secondary material results), recycled waste from bulky goods collection only collected via specific collection systems for this waste
                        #print(subsegment, plastic_type, "row[7]:", row[7], "TC_scen_2:", TC_scen_2, "use[0][3]:", use[0][3], "waste[0][3]:", waste[0][3])
                        #print("scaling_factor_used:",  scaling_factor_used, "waste_scaled:", waste_scaled, "use_scaled:", use_scaled)
                        origin_inflow = row[0]
                        concerned_process = row[1]
                        destination = row[4]
                        #print((subsegment, plastic_type, origin_inflow, concerned_process, scenario))
                        mycursor.execute(select_flow_id,
                                         (subsegment, plastic_type, origin_inflow, concerned_process, scenario))
                        inflow_id = mycursor.fetchall()

                        mycursor.execute(select_flow_id,
                                         (subsegment, plastic_type, concerned_process, destination, scenario))
                        outflow_id = mycursor.fetchall()
                        mycursor.execute(insert_into_TCs, (inflow_id[0][0], outflow_id[0][0], scenario, TC_scen_2, 'NULL'))

    mfa_plastics_ch.commit()

    for row in waste_scen2:
        #print(row)
        mycursor.execute("INSERT INTO waste_scen2 "
                         "VALUES "
                         "((%s), (%s), (%s))", row)
        mfa_plastics_ch.commit()


    # set TCs for Collection and Sorting same as for sc0001

    select_processes_on_LC_stage = ("SELECT "
                                    "   id_processes "
                                    "FROM "
                                    "   processes "
                                    "WHERE "
                                    "   life_cycle_stage_number_processes = (%s)")

    get_TCs_scen_1 = (  "SELECT "
                        "   origin_flows AS 'origin_inflow', "
                        "   concerned_process, "
                        "   `subsegment_destination_flows`, "
                        "   plastic_type_flows, "
                        "   destination_outflow, "
                        "   inflow, "
                        "   outflow, "
                        "   TC "
                        "FROM "
                        "(SELECT "
                        "   origin_flows as 'concerned_process', "
                        "   destination_flows as 'destination_outflow', "
                        "   inflow, "
                        "   outflow, "
                        "   TC, "
                        "   scenario "
                        "FROM "
                        "   TCs "
                        "   INNER JOIN flows "
                        "   on TCs.outflow = flows.id_flows) as t1 "
                        "INNER JOIN flows "
                        "on t1.inflow = flows.id_flows "
                        "where TC >0 and scenario = 'sc0001' and concerned_process = (%s) "
                        "order by concerned_process, origin_inflow, `subsegment_destination_flows`, plastic_type_flows, destination_outflow")

    for i in range(4, (5+1)):
        mycursor.execute(select_processes_on_LC_stage, (i, ))
        processes = mycursor.fetchall()
        #print(processes)
        for process in processes:
            mycursor.execute(get_TCs_scen_1, process)
            TCs = mycursor.fetchall()
            #print(TCs)

            for i in range(1, (54+1)):
                for j in range(1, (11+1)):
                    subsegment = 'su' + str(i).zfill(4)
                    plastic_type = 'pl' + str(j).zfill(4)
                    for row in TCs:
                        if row[2] == subsegment and row[3] == plastic_type:
                            TC_scen_2 = row[7]
                            origin_inflow = row[0]
                            concerned_process = row[1]
                            destination = row[4]
                            mycursor.execute(select_flow_id, (subsegment, plastic_type, origin_inflow, concerned_process, scenario))
                            inflow_id = mycursor.fetchall()
                            mycursor.execute(select_flow_id, (subsegment, plastic_type, concerned_process, destination, scenario))
                            outflow_id = mycursor.fetchall()
                            #if inflow_id != [] and outflow_id != []:
                            if outflow_id != []: # then also inflow must exist
                                mycursor.execute(insert_into_TCs, (inflow_id[0][0], outflow_id[0][0], scenario, TC_scen_2, 'NULL'))

    mfa_plastics_ch.commit()


    # calculate amounts from use until into recycling

    from calc_flows import calc_flows
    calc_flows(3, 6, scenario, mfa_plastics_ch, mycursor)


    # calculate amounts secondary material

    from calc_sec_mat import calc_mat_out_from_rec_subsegments
    from functions import write_sec_mat_subseg_into_db
    write_sec_mat_subseg_into_db(calc_mat_out_from_rec_subsegments(scenario, mycursor), mfa_plastics_ch, mycursor)

    mfa_plastics_ch.commit()



