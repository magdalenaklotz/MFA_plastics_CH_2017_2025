def excel_read_in(mfa_plastics_ch, mycursor):



    import xlrd



    # connecting to Excel file 'Database'

    excel = xlrd.open_workbook('C:\\...\\Database.xlsx')  # insert storage location of file 'Database'



    # creating objects of the sheet class from the Excel sheets

    segments_sheet = excel.sheet_by_name('db_segments')
    subsegments_sheet = excel.sheet_by_name('db_subsegments')
    plastictypes_sheet = excel.sheet_by_name('db_plastic_types')
    processes_sheet = excel.sheet_by_name('db_processes')
    scenarios_sheet = excel.sheet_by_name('db_scenarios')
    flows_sheet = excel.sheet_by_name('db_flows')
    TCs_sheet = excel.sheet_by_name('db_TCs')
    # print(segments_sheet.cell_value(1, 0))






    # drop any existing tables (not possible to drop table if foreign key refers to it -> delete tables in right sequence in mysql workbench)

    mycursor.execute("DROP TABLE IF EXISTS `waste_scen2`")
    mycursor.execute("DROP TABLE IF EXISTS `results_optimization`")
    mycursor.execute("DROP TABLE IF EXISTS `uptaken_secondary_material_subsegments_plastic_types`")
    mycursor.execute("DROP TABLE IF EXISTS `secondary_material_subsegments_plastic_types`")
    mycursor.execute("DROP TABLE IF EXISTS `TCs`")
    mycursor.execute("DROP TABLE IF EXISTS `TCs_definition`")
    mycursor.execute("DROP TABLE IF EXISTS `flows`")
    mycursor.execute("DROP TABLE IF EXISTS `subsegments`")
    mycursor.execute("DROP TABLE IF EXISTS segments")
    mycursor.execute("DROP TABLE IF EXISTS `plastic_types`")
    mycursor.execute("DROP TABLE IF EXISTS `processes`")
    mycursor.execute("DROP TABLE IF EXISTS `scenarios`")

    mfa_plastics_ch.commit()






    # sheet "db_segments"


    # creating table

    mycursor.execute("CREATE TABLE IF NOT EXISTS segments"
                     "(id_segments VARCHAR(6) PRIMARY KEY,"
                     "name_segments VARCHAR(255) UNIQUE)")


    # inserting data into table

    for i in range(0, segments_sheet.ncols):
        if segments_sheet.cell_value(0, i) == 'id_segments': #enter header of column you want to address
                col_number_id_segments = i

    for i in range(0, segments_sheet.ncols):
        if segments_sheet.cell_value(0, i) == 'name_segments': #enter header of column you want to address
                col_number_name_segments = i

    add_segment = ("INSERT INTO segments"
                   "(id_segments, name_segments)"
                   "VALUES (%s, %s)")

    for r in range(1, segments_sheet.nrows):
        row =   (segments_sheet.cell_value(r, col_number_id_segments),
                segments_sheet.cell_value(r, col_number_name_segments))
        mycursor.execute(add_segment, row)
        mfa_plastics_ch.commit()






    # sheet "db_subsegments"


    # creating table

    mycursor.execute("CREATE TABLE `subsegments`"
                     "(`id_subsegments` VARCHAR(6) PRIMARY KEY,"
                     "`name_subsegments` VARCHAR(255) UNIQUE,"
                     "`segment_subsegments` VARCHAR(6),"
                     "FOREIGN KEY (`segment_subsegments`)" #foreign key ensures that only values inserted in respective column in referenced table can be inserted in respective column of this table
                     "REFERENCES segments (id_segments))")


    # inserting data into table

    for i in range(0, subsegments_sheet.ncols):
        if subsegments_sheet.cell_value(0, i) == 'id_subsegments': #enter header of column you want to address
                col_number_id_subsegments = i

    for i in range(0, subsegments_sheet.ncols):
        if subsegments_sheet.cell_value(0, i) == 'name_subsegments': #enter header of column you want to address
                col_number_name_subsegments = i

    for i in range(0, subsegments_sheet.ncols):
        if subsegments_sheet.cell_value(0, i) == 'segment_subsegments': #enter header of column you want to address
                col_number_segment_subsegments = i

    add_subsegment = ("INSERT INTO `subsegments`"
                   "(`id_subsegments`, `name_subsegments`, `segment_subsegments`)"
                   "VALUES (%s, %s, %s)")

    for r in range(1, 55): #subsegments_sheet.nrows
        row =   (subsegments_sheet.cell_value(r, col_number_id_subsegments),
                 subsegments_sheet.cell_value(r, col_number_name_subsegments),
                 subsegments_sheet.cell_value(r, col_number_segment_subsegments))
        mycursor.execute(add_subsegment, row)
        mfa_plastics_ch.commit()






    # sheet "db_plastic_types"


    # creating table

    mycursor.execute("CREATE TABLE `plastic_types` "
                     "(`id_plastic_types` VARCHAR(6) PRIMARY KEY, "
                     "`name_plastic_types` VARCHAR(255) UNIQUE)")


    # inserting data into table

    for i in range(0, plastictypes_sheet.ncols):
        if plastictypes_sheet.cell_value(0, i) == 'id_plastic_types': #enter header of column you want to address
                col_number_id_plastictypes = i

    for i in range(0, plastictypes_sheet.ncols):
        if plastictypes_sheet.cell_value(0, i) == 'name_plastic_types': #enter header of column you want to address
                col_number_name_plastictypes = i

    add_plastictype = ("INSERT INTO `plastic_types`"
                   "(`id_plastic_types`, `name_plastic_types`)"
                   "VALUES (%s, %s)")

    for r in range(1, plastictypes_sheet.nrows):
        row =   (plastictypes_sheet.cell_value(r, col_number_id_plastictypes),
                 plastictypes_sheet.cell_value(r, col_number_name_plastictypes))
        mycursor.execute(add_plastictype, row)
        mfa_plastics_ch.commit()






    # sheet "db_processes"


    # creating table

    mycursor.execute("CREATE TABLE `processes`"
                     "(`id_processes` VARCHAR(6) PRIMARY KEY,"
                     "`name_processes` VARCHAR(255) UNIQUE,"
                     "life_cycle_stage_processes VARCHAR(255),"
                     "life_cycle_stage_number_processes INT(1),"
                     "location_processes VARCHAR(255))")


    # inserting data into table

    for i in range(0, processes_sheet.ncols):
        if processes_sheet.cell_value(0, i) == 'id_processes': #enter header of column you want to address
                col_number_id_processes = i

    for i in range(0, processes_sheet.ncols):
        if processes_sheet.cell_value(0, i) == 'name_processes': #enter header of column you want to address
                col_number_name_processes = i

    for i in range(0, processes_sheet.ncols):
        if processes_sheet.cell_value(0, i) == 'life_cycle_stage_processes': #enter header of column you want to address
                col_number_LC_stage_processes = i

    for i in range(0, processes_sheet.ncols):
        if processes_sheet.cell_value(0, i) == 'life_cycle_stage_number_processes': #enter header of column you want to address
                col_number_LC_stage_number_processes = i

    for i in range(0, processes_sheet.ncols):
        if processes_sheet.cell_value(0, i) == 'location_processes': #enter header of column you want to address
                col_number_location_processes = i

    add_process = ("INSERT INTO `processes`"
                   "(id_processes, name_processes, life_cycle_stage_processes, life_cycle_stage_number_processes, location_processes)"
                   "VALUES (%s, %s, %s, %s, %s)")

    for r in range(1, processes_sheet.nrows):
        row =   (processes_sheet.cell_value(r, col_number_id_processes),
                 processes_sheet.cell_value(r, col_number_name_processes),
                 processes_sheet.cell_value(r, col_number_LC_stage_processes),
                 processes_sheet.cell_value(r, col_number_LC_stage_number_processes),
                 processes_sheet.cell_value(r, col_number_location_processes))
        mycursor.execute(add_process, row)
        mfa_plastics_ch.commit()






    # sheet "db_scenarios"


    # creating table

    mycursor.execute("CREATE TABLE `scenarios`"
                     "(`id_scenarios` VARCHAR(6) PRIMARY KEY,"
                     "`name_scenarios` VARCHAR(255) UNIQUE)")


    # inserting data into table

    for i in range(0, scenarios_sheet.ncols):
        if scenarios_sheet.cell_value(0, i) == 'id_scenarios': #enter header of column you want to address
                col_number_id_scenarios = i

    for i in range(0, scenarios_sheet.ncols):
        if scenarios_sheet.cell_value(0, i) == 'name_scenarios': #enter header of column you want to address
                col_number_name_scenarios = i

    add_scenario = ("INSERT INTO `scenarios`"
                   "(`id_scenarios`, `name_scenarios`)"
                   "VALUES (%s, %s)")

    for r in range(1, scenarios_sheet.nrows):
        row =   (scenarios_sheet.cell_value(r, col_number_id_scenarios),
                 scenarios_sheet.cell_value(r, col_number_name_scenarios))
        mycursor.execute(add_scenario, row)
        mfa_plastics_ch.commit()






    # sheet "db_flows"


    # creating table

    mycursor.execute("CREATE TABLE `flows`"
                     "(id_flows VARCHAR(12) PRIMARY KEY,"
                     "origin_flows VARCHAR(6),"
                     "`subsegment_origin_flows` VARCHAR(6),"
                     "destination_flows VARCHAR(6),"
                     "`subsegment_destination_flows` VARCHAR(6),"
                     "plastic_type_flows VARCHAR(6),"
                     "year_flows VARCHAR(10),"   # partly 'N/D'
                     "value_flows FLOAT,"
                     "scenario_flows VARCHAR(6),"
                     "FOREIGN KEY (origin_flows)"           #foreign key ensures that only values inserted in respective column in referenced table can be inserted in respective column of this table
                     "REFERENCES processes (id_processes),"
                     "FOREIGN KEY (`subsegment_origin_flows`)"
                     "REFERENCES `subsegments` (`id_subsegments`),"
                     "FOREIGN KEY (destination_flows)"
                     "REFERENCES processes (id_processes),"
                     "FOREIGN KEY (`subsegment_destination_flows`)"
                     "REFERENCES `subsegments` (`id_subsegments`),"
                     "FOREIGN KEY (plastic_type_flows)"
                     "REFERENCES plastic_types (id_plastic_types),"
                     "FOREIGN KEY (scenario_flows)"
                     "REFERENCES scenarios (id_scenarios))")


    # inserting data into table

    for i in range(0, flows_sheet.ncols):
        if flows_sheet.cell_value(0, i) == 'id_flows':  # enter header of column you want to address
            col_number_id_flows = i

    for i in range(0, flows_sheet.ncols):
        if flows_sheet.cell_value(0, i) == 'origin_flows':  # enter header of column you want to address
            col_number_origin_flows = i

    for i in range(0, flows_sheet.ncols):
        if flows_sheet.cell_value(0, i) == 'subsegment_origin_flows':  # enter header of column you want to address
            col_number_subsegment_origin_flows = i

    for i in range(0, flows_sheet.ncols):
        if flows_sheet.cell_value(0, i) == 'destination_flows':  # enter header of column you want to address
            col_number_destination_flows = i

    for i in range(0, flows_sheet.ncols):
        if flows_sheet.cell_value(0, i) == 'subsegment_destination_flows':  # enter header of column you want to address
            col_number_subsegment_destination_flows = i

    for i in range(0, flows_sheet.ncols):
        if flows_sheet.cell_value(0, i) == 'plastic_type_flows':  # enter header of column you want to address
            col_number_plastic_type_flows = i

    for i in range(0, flows_sheet.ncols):
        if flows_sheet.cell_value(0, i) == 'year_flows':  # enter header of column you want to address
            col_number_year_flows = i

    for i in range(0, flows_sheet.ncols):
        if flows_sheet.cell_value(0, i) == 'value_flows':  # enter header of column you want to address
            col_number_value_flows = i

    for i in range(0, flows_sheet.ncols):
        if flows_sheet.cell_value(0, i) == 'scenario_flows':  # enter header of column you want to address
            col_number_scenario_flows = i

    add_flow = ("INSERT INTO `flows`"
                "(`id_flows`, `origin_flows`, `subsegment_origin_flows`, `destination_flows`, `subsegment_destination_flows`, `plastic_type_flows`, `year_flows`, `value_flows`, `scenario_flows`)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

    rows = []
    for r in range(1, flows_sheet.nrows):
        row = (flows_sheet.cell_value(r, col_number_id_flows),
               flows_sheet.cell_value(r, col_number_origin_flows),
               flows_sheet.cell_value(r, col_number_subsegment_origin_flows),
               flows_sheet.cell_value(r, col_number_destination_flows),
               flows_sheet.cell_value(r, col_number_subsegment_destination_flows),
               flows_sheet.cell_value(r, col_number_plastic_type_flows),
               flows_sheet.cell_value(r, col_number_year_flows),
               flows_sheet.cell_value(r, col_number_value_flows),
               flows_sheet.cell_value(r, col_number_scenario_flows))
        rows.append(row)
    mycursor.executemany(add_flow, rows)
    mfa_plastics_ch.commit()


    # creating flows not read-in from Excel, but calculated via TCs read-in from Excel, i.e. Packaging flows from Sorting to Recycling, with flow value 0, for which the values are calculated and inserted in a next step

    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0017', 'pr0026', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0017', 'pr0028', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0017', 'pr0030', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0017', 'pr0042', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0019', 'pr0026', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0019', 'pr0042', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0019', 'pr0028', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0019', 'pr0030', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0020', 'pr0026', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0020', 'pr0027', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0020', 'pr0029', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0020', 'pr0031', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0021', 'pr0026', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0021', 'pr0027', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0021', 'pr0029', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0021', 'pr0031', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0022', 'pr0043', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0022', 'pr0027', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0022', 'pr0029', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0022', 'pr0031', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0023', 'pr0027', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0023', 'pr0029', 'sc0001', 2017))
    mycursor.callproc('create_flows_pr_to_pr_scen', ('pr0023', 'pr0031', 'sc0001', 2017))
    mfa_plastics_ch.commit()






    # table "TCs"


    # creating table

    mycursor.execute("CREATE TABLE TCs"
                     "(inflow VARCHAR(12),"
                     "outflow VARCHAR(12),"
                     "scenario VARCHAR(6),"
                     "TC FLOAT,"
                     "source VARCHAR (1000),"
                     "FOREIGN KEY (inflow)"
                     "REFERENCES flows (id_flows),"
                     "FOREIGN KEY (outflow)"
                     "REFERENCES flows (id_flows),"
                     "FOREIGN KEY (scenario)"
                     "REFERENCES scenarios (id_scenarios))")


    # inserting data into table

    add_TC = ("INSERT INTO TCs (inflow, outflow, scenario, TC) VALUES"
              "((SELECT id_flows FROM flows"  # inflow
              "     WHERE destination_flows = (%s)"
              "     AND origin_flows = (%s)"
              "     AND scenario_flows = (%s)"
              "     AND `subsegment_origin_flows` = (%s)"
              "     AND plastic_type_flows = (%s)),"
              "(SELECT id_flows FROM flows"  # outflow
              "     WHERE origin_flows = (%s)"
              "     AND destination_flows = (%s)"
              "     AND scenario_flows = (%s)"
              "     AND `subsegment_origin_flows` = (%s)"
              "     AND plastic_type_flows = (%s)),"
              "(%s),"  # scenario
              "(%s))")

    for i in range(1, TCs_sheet.nrows):

        process_concerned = TCs_sheet.cell_value(i, 0)
        scenario = TCs_sheet.cell_value(i, 3)
        inflow_origin = TCs_sheet.cell_value(i, 4)  # inflow origin only needs to be specified, if for different flows to the same process different TCs apply (e.g. food bottles from hollow bodies collection or mixed plastics collection bags); if the same TC applies for flows coming from different processes, TC shall be specified only one time and origin_inflow denoted as "any" (in this case the specified TC is inserted in db for all processes with flows to pr0017 for respective subsegments from respective plastic types, even if respective flows amount to 0 (this is irrelevant, if no TC different from the one specified applies for any flows to pr0017)); if different TCs based on origin of ingoing flows, then single TC need to be specified and origin inflow needs to be specified for each;
        inflow_subsegment = TCs_sheet.cell_value(i, 5)
        outflow_destination = TCs_sheet.cell_value(i, 6)
        outflow_subsegment = TCs_sheet.cell_value(i, 8)
        plastic_type = TCs_sheet.cell_value(i, 9)
        TC = TCs_sheet.cell_value(i, 11)

        if inflow_origin != 'any':
            row = (process_concerned, inflow_origin, scenario, inflow_subsegment, plastic_type,
                   process_concerned, outflow_destination, scenario, outflow_subsegment, plastic_type,
                   scenario,
                   TC)
            mycursor.execute(add_TC, row)
            mfa_plastics_ch.commit()

        else:
            for j in range(1, processes_sheet.nrows):
                row_help = (processes_sheet.cell_value(j, 0), process_concerned, inflow_subsegment, plastic_type, scenario)
                mycursor.execute(
                    "SELECT id_flows from flows WHERE origin_flows = (%s) and destination_flows = (%s) and `subsegment_origin_flows` = (%s) and plastic_type_flows = (%s) and scenario_flows = (%s)",
                    row_help)       # for all existing processes (loop) it is checked whether there is a flow from the respective process to the concerned process, in order to insert a TC in this case
                exists = mycursor.fetchall()
                if exists != []:    # this causes also insertion of TC for ingoing flows from a processes to the concerned processes which exist but amount to zero, but this has no consequence, since this flows amounting to zero are later on multiplied with TC for flow calculation, so resulting flow is again 0 (e.g.,flow for C non-food films in hollow bodies collection to mixed plastics sorting abroad exists, but amounts to zero, gets TC specified for flows of C non-food films in mixed plastics collection bags to mixed plastics sorting abroad to respective outgoing processes)
                    inflow_origin = processes_sheet.cell_value(j, 0)
                    row = (process_concerned, inflow_origin, scenario, inflow_subsegment, plastic_type,
                           process_concerned, outflow_destination, scenario, outflow_subsegment, plastic_type,
                           scenario,
                           TC)
                    mycursor.execute(add_TC, row)
                    mfa_plastics_ch.commit()




    # table "TCs_definition"


    # creating table

    mycursor.execute("CREATE TABLE TCs_definition "
                     "(scenario VARCHAR(6), "
                     "process_concerned VARCHAR(6), "
                     "inflow_origin VARCHAR(6), "
                     "`inflow_subsegment` VARCHAR(6), "
                     "outflow_destination VARCHAR(6), "
                     "outflow_destination_LC_stage INT(1), "
                     "`outflow_subsegment` VARCHAR(6), "
                     "plastic_type VARCHAR(6), "                 
                     "TC FLOAT, "
                     "source VARCHAR (1000),"
                     "FOREIGN KEY (scenario)"
                     "REFERENCES scenarios (id_scenarios))")


    # inserting data into table

    add_TC_definition = ("INSERT INTO TCs_definition (scenario, process_concerned, inflow_origin, `inflow_subsegment`, outflow_destination, outflow_destination_LC_stage, `outflow_subsegment`, plastic_type, TC, source) "
                         "VALUES "
                         "((%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s))")

    rows = []

    for i in range(1, TCs_sheet.nrows):

        scenario = TCs_sheet.cell_value(i, 3)
        process_concerned = TCs_sheet.cell_value(i, 0)
        inflow_origin = TCs_sheet.cell_value(i, 4)
        inflow_subsegment = TCs_sheet.cell_value(i, 5)
        outflow_destination = TCs_sheet.cell_value(i, 6)
        outflow_destination_LC_stage = TCs_sheet.cell_value(i, 7)
        outflow_subsegment = TCs_sheet.cell_value(i, 8)
        plastic_type = TCs_sheet.cell_value(i, 9)
        TC = TCs_sheet.cell_value(i, 11)
        source = TCs_sheet.cell_value(i, 12)

        row = (scenario, process_concerned, inflow_origin, inflow_subsegment, outflow_destination, outflow_destination_LC_stage, outflow_subsegment, plastic_type, TC, source)
        rows.append(row)

    mycursor.executemany(add_TC_definition, rows)
    mfa_plastics_ch.commit()






    # create table secondary_material_subsegments_plastic_types

    mycursor.execute("CREATE TABLE `secondary_material_subsegments_plastic_types` "
                     "  (`scenario` VARCHAR(6) NULL, "
                     "  `subsegment` VARCHAR(6) NULL, "
                     "  `plastic_type` VARCHAR(6) NULL, "
                     "  `amount_secondary_material` FLOAT NULL,"
                     "  FOREIGN KEY (scenario)"
                     "  REFERENCES scenarios (id_scenarios), "
                     "  FOREIGN KEY (`subsegment`) "
                     "  REFERENCES `subsegments` (`id_subsegments`), "
                     "  FOREIGN KEY (plastic_type) "
                     "  REFERENCES plastic_types (id_plastic_types))")
    mfa_plastics_ch.commit()






    # create table uptaken_secondary_material_subsegments_plastic_types

    mycursor.execute("CREATE TABLE `uptaken_secondary_material_subsegments_plastic_types` "
                     "  (`scenario` VARCHAR(6) NULL, "
                     "   `plastic_type` VARCHAR(6) NULL, "
                     "   `subsegment` VARCHAR(100) NULL, "
                     "   `allocated_secondary_material` FLOAT NULL, "
                     "    `demand/limit` FLOAT NULL, "
                     "  FOREIGN KEY (scenario) "
                     "  REFERENCES scenarios (id_scenarios), "
                     "  FOREIGN KEY (plastic_type) "
                     "  REFERENCES plastic_types (id_plastic_types))")
    mfa_plastics_ch.commit()






    # create table results_optimization

    mycursor.execute("CREATE TABLE `results_optimization` "
                     "  (`scenario` VARCHAR(6) NULL, "
                     "   `plastic_type` VARCHAR(6) NULL, "
                     "   `uptaken_sec_mat` FLOAT NULL, "
                     "   `total_sec_mat` FLOAT NULL, "
                     "   `share_uptaken_sec_mat` FLOAT NULL, "
                     "   `recycling_rate` FLOAT NULL, "     #based on total waste (since 90% collected even of part exported in sc0001
                     "   `recycling_rate_uptaken` FLOAT NULL, "
                     "  FOREIGN KEY (scenario) "
                     "  REFERENCES scenarios (id_scenarios), "
                     "  FOREIGN KEY (plastic_type) "
                     "  REFERENCES plastic_types (id_plastic_types))")
    mfa_plastics_ch.commit()






    # create table waste_scen2

    mycursor.execute("CREATE TABLE `waste_scen2` "
                     "  (`subsegment` VARCHAR(6) NULL, "
                     "  `plastic_type` VARCHAR(6) NULL, "
                     "  `waste_amount` FLOAT NULL,"
                     "  FOREIGN KEY (`subsegment`) "
                     "  REFERENCES `subsegments` (`id_subsegments`), "
                     "  FOREIGN KEY (plastic_type) "
                     "  REFERENCES plastic_types (id_plastic_types))")
    mfa_plastics_ch.commit()


