def opt_applicability_scenario(demand_red, demand_red_PET, scen, scen_desc, mfa_plastics_ch, mycursor):


    import pandas as pd
    from scipy.optimize import linprog
    import numpy as np


    select_waste = ("SELECT "                               # all waste (all collections, incineration and export and unknown destiny)
                   "   sum(waste_amount) "
                    "FROM "
                    "   waste_scen2 "
                    "WHERE "
                    "   plastic_type = (%s)")


    # creating a dataframe containing the specification (subsegment, plastic type, origin) and value of all secondary material flows and the uptaking product subsegments from Excel file 'flows_into_rec_suitability_sec_mat'

    df = pd.read_excel(r'C:\\...\\flows_into_rec_suitability_sec_mat.xlsx')
    # print(df)


    # read out share of demand from each subsegment that can be covered by secondary material from Excel file 'demand_reduction'; distinction between PET and all other plastic types

    demand_reduction = pd.read_excel(r'C:\\...\\demand_reduction.xlsx')

    demand_reduction_vector = []
    for i in range(0, len(demand_reduction)):
        demand_reduction_vector.append(
            demand_reduction.iloc[i][demand_red])
    #print(demand_reduction_vector, len(demand_reduction_vector))

    demand_reduction_vector_PET = []
    for i in range(0, len(demand_reduction)):
        demand_reduction_vector_PET.append(
            demand_reduction.iloc[i][demand_red_PET])


    # create scenario

    scenario = scen
    scen_description = scen_desc

    mycursor.execute("DELETE FROM "
                     "  mfa_plastics_ch.uptaken_secondary_material_subsegments_plastic_types "
                     "WHERE "
                     "  scenario = (%s)", (scenario, ))
    mycursor.execute("DELETE FROM "
                     "  mfa_plastics_ch.results_optimization "
                     "WHERE "
                     "  scenario = (%s)", (scenario, ))
    mycursor.execute("DELETE FROM "
                     "  scenarios "
                     "WHERE "
                     "  id_scenarios = (%s)", (scenario, ))
    mfa_plastics_ch.commit()

    insert_into_scenarios = ("INSERT INTO scenarios (id_scenarios, name_scenarios) VALUES ((%s), (%s))")
    mycursor.execute(insert_into_scenarios, (scenario, scen_description))
    mfa_plastics_ch.commit()


    # optimization carried out for each plastic type (subsequently)

    compare = []
    results_opt = []

    for p in range(1, 8 + 1):  # no secondary material from other plastic types (9, 10, 11 = PA, PC, PUR)

        plastic_type = 'pl' + str(p).zfill(4)
        #print(plastic_type)

        mycursor.execute(select_waste, (plastic_type, ))
        total_waste = mycursor.fetchall()

        obj = []
        total_sec_mat = 0

        for i in range(0, len(df)):
            if df.iloc[i]['id plastic'] == plastic_type \
                    and df.iloc[i]['suitable_subsegments_secondary_material'] != 'N/A (sorted out during recycling)':
                    total_sec_mat = total_sec_mat + float(df.iloc[i]['out from recycling'])


        # creation of objective function: for each secondary material flow of concerned plastic type, append value of secondary material flow as many times as uptaking subsegments exist (in objective function, each multiplied with variables specifying shares of secondary material flows allocated to subsegments)

        for i in range(0, len(df)):
            if df.iloc[i]['id plastic'] == plastic_type \
                    and df.iloc[i]['suitable_subsegments_secondary_material'] != 'N/A (sorted out during recycling)':
                a = (df.iloc[i]['suitable_subsegments_secondary_material'])
                for j in range(0, len(a.split(', '))):
                    obj.append(float(df.iloc[i]['out from recycling']) * (-1))


        # creation of constraints (left side): for each subsegment (one now of matrix corresponds to each subsegment), for each secondary material flow, if subsegment can take up secondary material flow, for number of total uptaking subsegments of that secondary material flow, append value of secondary material flow at its position number of all uptaking subsegments of that secondary material flow, for the rest append 0, if subsegment not taking up secondary material flow, append zeros for number of total uptaking subsegments for that secondary material flow

        constraints = []

        for x in range(1, 54 + 1):

            subsegment = 'su' + str(x).zfill(4)
            # print(subsegment)

            uptake = []
            for i in range(0, len(df)):
                if df.iloc[i]['id plastic'] == plastic_type \
                        and df.iloc[i]['suitable_subsegments_secondary_material'] != 'N/A (sorted out during recycling)':
                    a = (df.iloc[i]['suitable_subsegments_secondary_material'])
                    if subsegment in a:
                        for y in range(0, len(a.split(', '))):
                            if a.split(', ')[y] == subsegment:
                                uptake.append(df.iloc[i]['out from recycling'])
                            else:
                                uptake.append(0)
                    else:
                        for j in range(0, len(a.split(', '))):
                            uptake.append(0)
            constraints.append(uptake)

        #print(obj)
        #print(constraints)
        #print('len constraints (should be number of subsegments:', len(constraints))

        # to the list of constraint rows established in previous step (one row for each subsegment), for each secondary material flow of concerned plastic type, append one row, containing constraint that sum of all variables specifying shares of that secondary material flow allocated to individual uptaking subsegments must be smaller or equal to 1 (1s in row for variables relating to concerned secondary material flow, zeros in row for all variables relating to all other secondary material flows)

        con_tot = []
        for i in range(0, len(df)):
            if df.iloc[i]['id plastic'] == plastic_type \
                    and df.iloc[i]['suitable_subsegments_secondary_material'] != 'N/A (sorted out during recycling)':
                con = []
                dig_before = 0
                for l in range(0, i):
                    if df.iloc[l]['id plastic'] == plastic_type \
                            and df.iloc[l][
                        'suitable_subsegments_secondary_material'] != 'N/A (sorted out during recycling)':
                        a = (df.iloc[l]['suitable_subsegments_secondary_material'])
                        # print(a)
                        dig_before = dig_before + len(a.split(', '))
                for m in range(0, dig_before):
                    con.append(0)
                a = (df.iloc[i]['suitable_subsegments_secondary_material'])
                for j in range(0, len(a.split(', '))):
                    con.append(1)
                for k in range(0, len(obj) - dig_before - len(a.split(', '))):
                    con.append(0)
                # print('nr variables = len_con:', len(con))
                con_tot.append(con)

        #print(con_tot)
        #print('nr sec mat flows:', len(con_tot))

        constraints.extend(con_tot)
        #print(constraints)


        # creation of right side of constraints (maximum secondary material amount that can be taken up by each subsegment + as many 1s as secondary material flows exist (maximum sum of all variables specifying shares of that secondary material flow allocated to individual subsegments))

        demand = []

        get_total_use_amount_subsegment_plastic = ("SELECT "
                                                   "   scenario_flows, "
                                                   "   `subsegment_origin_flows`, "
                                                   "   plastic_type_flows, "
                                                   "   sum(value_flows) "
                                                   "FROM "
                                                   "   flows "
                                                   "WHERE "
                                                   "    scenario_flows = (%s) AND "
                                                   "    destination_flows = 'pr0008' AND "
                                                   "    plastic_type_flows = (%s) "
                                                   "GROUP BY "
                                                   "   scenario_flows, "
                                                   "   `subsegment_origin_flows`, "
                                                   "   plastic_type_flows ")

        mycursor.execute(get_total_use_amount_subsegment_plastic, ('sc0002', plastic_type,))
        dem_sub = mycursor.fetchall()

        #print(dem_sub)

        r = 0

        if plastic_type == 'pl0003':
            for row in dem_sub:
                if row[3] is None:
                    demand.append(0)
                    #print(0)
                else:
                    demand.append(row[3]/(1-0.07) * demand_reduction_vector_PET[r])      # share of demand coverable by secondary material multiplied with (consumption amount plus manufacturing losses (7%)); demand reduction vector has same order as use amounts subsegments;
                r += 1
        else:
            for row in dem_sub:
                if row[3] is None:
                    demand.append(0)
                    #print(0)
                else:
                    demand.append(row[3]/(1-0.07) * demand_reduction_vector[r])      # share of demand coverable by secondary material multiplied with (consumption amount plus manufacturing losses (7%)); demand reduction vector has same order as use amounts subsegments;
                    #print(row[3]/(1-0.07), row[3]/(1-0.07) * demand_reduction_vector[r])      # total demand, demand that can be covered by secondary material
                r += 1

        #print(demand)
        #print(len(demand)) # should be number of subsegments

        con_each = []

        for i in range(0, len(df)):
            if df.iloc[i]['id plastic'] == plastic_type \
                    and df.iloc[i]['suitable_subsegments_secondary_material'] != 'N/A (sorted out during recycling)':
                con_each.append(1)

        demand.extend(con_each)

        #print(len(constraints), len(demand))   # shall be the same (number of constraint rows)
        #print(len(obj), len(constraints[0]), len(con_tot[0]))   # shall be the same (number of variables)


        # calculation of optimization

        # boundaries for each variable 0 and +inf are default

        """
        bnd = [(0, float("inf")),  # Bounds of x
               (0, float("inf"))]  # Bounds of y
        Instead of float("inf"), you can use math.inf, numpy.inf, or scipy.inf.
        """

        opt = linprog(c=obj, A_ub=constraints, b_ub=demand, method="revised simplex")
        #print(opt.message) # exit status of algorithm (optimization successful or not)
        #print(len(opt.x))  # values of optimized variables
        results_opt.append((scenario, plastic_type, float(-opt.fun), float(total_sec_mat), float(-opt.fun/total_sec_mat), float(total_sec_mat/total_waste[0][0]), float(-opt.fun/total_waste[0][0])))   # opt.fun = value of optimized function (negative, minimum) = negative amount of total uptaken secondary material of that plastic type


        # calculating the amount of total allocated secondary material for each subsegment (of concerned plastic type), and total allocated share of each secondary material flow

        uptaken = np.dot(constraints, opt.x)
        #print(uptaken)
        #print(len(uptaken))        # number subsegments + number secondary material flows of concerned plastic type


        # for each subsegment, compiling the uptaken amount of secondary material and the demand that can be covered by secondary material; for each secondary material flow, compiling the uptaken share and the maximum allocatable share (1)

        all_uptaking_subsegments = []
        for i in range(0, len(df)):
            if df.iloc[i]['id plastic'] == plastic_type \
                    and df.iloc[i]['suitable_subsegments_secondary_material'] != 'N/A (sorted out during recycling)':
                a = df.iloc[i]['suitable_subsegments_secondary_material']
                all_uptaking_subsegments.extend(a.split(', '))
        #print(all_uptaking_subsegments)

        mycursor.execute("SELECT `name_subsegments` "
                         "FROM "
                         "  `subsegments` "
                         "ORDER BY "
                         "  `id_subsegments`")
        subsegments = mycursor.fetchall()
        #print(subsegments)

        for i in range(0, len(uptaken)):
            if i <= 53:
                subseg = 'su' + str(i + 1).zfill(4)
                #print(subseg)

                if subseg in all_uptaking_subsegments:
                    compare.append((scenario, plastic_type, subsegments[i][0], uptaken[i], demand[i]))
                else:
                    compare.append((scenario, plastic_type, subsegments[i][0], uptaken[i], 0))
            else:
                compare.append((scenario, plastic_type, 'variable', uptaken[i], demand[i]))

        #print(compare)
        #print(len(compare))    # number subsegments + number secondary material flows of concerned plastic type


    # for all plastic types, saving optimization results into database:

        # maximum and uptaken amounts of secondary material for each subsegment

    for row in compare:
        #print('a', (row[0], row[1], row[2], float(row[3]), float(row[4])))
        mycursor.execute("INSERT INTO "
                         "  `uptaken_secondary_material_subsegments_plastic_types` "
                         "VALUES "
                         "  ((%s), (%s), (%s), (%s), (%s))",
                         (row[0], row[1], row[2], float(row[3]), float(row[4])))
        #print((row[0], row[1], row[2], float(row[3]), float(row[4])))
    mfa_plastics_ch.commit()

    #comp_upt_dem_subs = pd.DataFrame(compare, columns=['scenario', 'plastic type', 'subsegment', 'uptaken', 'demand (max)'])
    #print(comp_upt_dem_subs)

        # total and total uptaken amount of secondary material, as well as share of uptaken secondary material, and recycling rate and true recycling rate

    #print ("res: \n", results_opt)
    insert_results_db = ("INSERT INTO "
                         "  results_optimization "
                         "VALUES "
                         "  ((%s), (%s), (%s), (%s), (%s), (%s), (%s))")

    mycursor.executemany(insert_results_db, results_opt)
    mfa_plastics_ch.commit()