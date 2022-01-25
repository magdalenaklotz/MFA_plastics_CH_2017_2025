def results_depiction(mfa_plastics_ch, mycursor):


    # create sql views called via python scripts

    from create_views_sql import create_views_sql
    create_views_sql(mfa_plastics_ch, mycursor)


    # --- DEPICT TOTAL AND UPTAKEN SECONDARY MATERIAL FOR EACH SUB-SCENARIO FOR EACH PLASTIC TYPE ---

    from depiction_uptaken_sec_mat_scen import depic_uptaken_sec_mat_scen
    depic_uptaken_sec_mat_scen(mycursor)


    # --- DEPICT RECYCLING RATE AND TRUE RECYCLING RATE FOR EACH SUB-SCENARIO FOR EACH PLASTIC TYPE---

    from depiction_RR import depic_RR
    depic_RR(mfa_plastics_ch, mycursor)


    # --- DEPICT AMOUNTS OF SECONDARY MATERIAL THAT CAN BE AND THAT ARE UPTAKEN BY THE INDIVIDUAL SUBSEGMENTS IN THE INDIVIDUAL SUB-SCENARIOS FOR EACH PLASTIC TYPE ---

    from depiction_uptaken_subsegments_plastic_type import depic_uptaken_subsegments_plastic_type
    depic_uptaken_subsegments_plastic_type('pl0001', mycursor)
    depic_uptaken_subsegments_plastic_type('pl0002', mycursor)
    depic_uptaken_subsegments_plastic_type('pl0003', mycursor)
    depic_uptaken_subsegments_plastic_type('pl0004', mycursor)
    depic_uptaken_subsegments_plastic_type('pl0005', mycursor)
    depic_uptaken_subsegments_plastic_type('pl0006', mycursor)
    depic_uptaken_subsegments_plastic_type('pl0007', mycursor)
    depic_uptaken_subsegments_plastic_type('pl0008', mycursor)

    from depiction_uptaken_subs_plast_nonzero import depic_uptaken_subs_plast_nonzero
    depic_uptaken_subs_plast_nonzero('pl0001', mycursor)


