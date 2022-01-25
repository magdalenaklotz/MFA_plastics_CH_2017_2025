def optimization(mfa_plastics_ch, mycursor):


    # high applicability scenario

    from opt_applicability_scenario import opt_applicability_scenario
    opt_applicability_scenario('share of demand suitable for taking up secondary material - high applicability',
                               'share of demand suitable for taking up secondary material - high applicability PET',
                               'sc0022',
                               'sc0002_high_applic_sec_mat',
                               mfa_plastics_ch,
                               mycursor)


    # moderate applicability scenario

    from opt_applicability_scenario import opt_applicability_scenario
    opt_applicability_scenario('share of demand suitable for taking up secondary material - moderate applicability',
                               'share of demand suitable for taking up secondary material - moderate applicability PET',
                               'sc0023',
                               'sc0002_moderate_applic_sec_mat',
                               mfa_plastics_ch,
                               mycursor)


    # low applicability scenario

    from opt_applicability_scenario import opt_applicability_scenario
    opt_applicability_scenario('share of demand suitable for taking up secondary material - low applicability',
                               'share of demand suitable for taking up secondary material - low applicability PET',
                               'sc0024',
                               'sc0002_low_applic_sec_mat',
                               mfa_plastics_ch,
                               mycursor)
