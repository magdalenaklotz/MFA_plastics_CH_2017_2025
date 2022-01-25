def allocation_sec_mat(mycursor):


    from openpyxl import load_workbook
    import pandas as pd


    # select all flows into recycling

    mycursor.execute("select "
        "	id_flows, "
        "    origin, "
        "    name_processes as 'destination', "
        "    `name_subsegments`, "
        "   `id_subsegments`, "
        "    name_plastic_types, "
        "    id_plastic_types, "
        "	value_flows, "
        "    scenario_flows "
        "from "
        "(select "
        "	id_flows, "
        "    name_processes as 'origin', "
        "    `subsegment_destination_flows` as 'subsegment', "
        "    plastic_type_flows, "
        "    destination_flows, "
        "    value_flows, "
        "    scenario_flows "
        "from "
        "(select * from flows "
        "where "
        "	scenario_flows = 'sc0002' and "
        "    value_flows > 0 and "
        "    destination_flows in "
        "	(select "
        "		id_processes "
        "	from "
        "		processes "
        "	where "
        "		life_cycle_stage_number_processes = 6)) t1 "
        "inner join "
        "     processes t2 "
        "on "
        "	t1.origin_flows = t2.id_processes) t3 "
        "inner join "
        "	processes t4 "
        "on "
        "	t3.destination_flows = t4.id_processes "
        "inner join "
        "	`subsegments` t5 "
        "on "
        "	t3.subsegment = t5.`id_subsegments` "
        "inner join "
        "	plastic_types t6 "
        "on "
        "	t3.plastic_type_flows = t6.id_plastic_types "
        "order by origin, destination, id_plastic_types, `id_subsegments`")

    all_flows_into_rec = mycursor.fetchall()
    # print(all_flows_into_rec)


    # write flow values of all flows into recycling into Excel sheet, where amounts of secondary material for each flow into recycling are calculated via specified recycling efficiencies, and subsegments suitable for taking up each secondary material flow are specified

    df = pd.DataFrame(all_flows_into_rec, columns=['flow_id', 'origin', 'recycling process', 'subsegment', 'id subsegment', 'plastic_type', 'id plastic', 'value', 'scenario'])

    """
    writer = pd.ExcelWriter('flows_into_rec.xlsx')
    df.to_excel(writer, 'data')
    writer.save()
    """

    workbook = load_workbook('flows_into_rec_suitability_sec_mat.xlsx')
    worksheet = workbook['data']
    for index, row in df.iterrows():
        # print(row[7])
        cell_in = 'I%d' % (index + 2)  # cell into which to write flow value: column I of Excel workbook ('value'), row number = (index + 2) (value of first row in dataframe is written in second row of Excel workbook (which has number 2, because starting from 0), because Excel workbook has headers in first row, etc.)
        # print(cell)
        worksheet[cell_in] = row[7]  # value
        cell_eff = 'J%d' % (index + 2)
        if worksheet[cell_eff].value != 'N/A':
            cell_out = 'K%d' % (index + 2)
            worksheet[cell_out] = worksheet[cell_eff].value * row[7]
    workbook.save('flows_into_rec_suitability_sec_mat.xlsx')