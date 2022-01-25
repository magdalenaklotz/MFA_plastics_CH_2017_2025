def write_sec_mat_subseg_into_db(list_of_tuples, mfa_plastics_ch, mycursor):


    write_sec_mat_into_db = ("INSERT INTO "
                             "  `secondary_material_subsegments_plastic_types` (scenario, `subsegment`, plastic_type, amount_secondary_material) "
                             "  VALUES ((%s), (%s), (%s), (%s))")
    mycursor.executemany(write_sec_mat_into_db, list_of_tuples)
    mfa_plastics_ch.commit()

