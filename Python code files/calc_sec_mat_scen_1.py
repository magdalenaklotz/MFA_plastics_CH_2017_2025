def calc_sec_mat_scen_1(mfa_plastics_ch, mycursor):


    scenario = 'sc0001'


    # calculating secondary material amounts

    from calc_sec_mat import calc_mat_out_from_rec_subsegments


    # writing calculated secondary material amounts into db

    from functions import write_sec_mat_subseg_into_db
    write_sec_mat_subseg_into_db(calc_mat_out_from_rec_subsegments(scenario, mycursor), mfa_plastics_ch, mycursor)

