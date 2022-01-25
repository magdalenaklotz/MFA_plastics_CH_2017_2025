def create_views_sql(mfa_plastics_ch, mycursor):

    mycursor.execute(
        "CREATE \n"
            "ALGORITHM = UNDEFINED \n"
            "SQL SECURITY DEFINER \n"
        "VIEW `res_opt_scen_only` AS \n"
            "SELECT \n"
                "`t5`.`name_plastic_types` AS `name_plastic_types`, \n"
                "`t2`.`uptaken_sec_mat_sc0022` AS `uptaken_sec_mat_sc0022`, \n"
                "`t3`.`uptaken_sec_mat_sc0023` AS `uptaken_sec_mat_sc0023`, \n"
                "`t4`.`uptaken_sec_mat_sc0024` AS `uptaken_sec_mat_sc0024`, \n"
                "`t2`.`total_sec_mat_sc0022` AS `total_sec_mat_sc0022`, \n"
                "`t3`.`total_sec_mat_sc0023` AS `total_sec_mat_sc0023`, \n"
                "`t4`.`total_sec_mat_sc0024` AS `total_sec_mat_sc0024`, \n"
                "`t2`.`share_uptaken_sec_mat_sc0022` AS `share_uptaken_sec_mat_sc0022`, \n"
                "`t3`.`share_uptaken_sec_mat_sc0023` AS `share_uptaken_sec_mat_sc0023`, \n"
                "`t4`.`share_uptaken_sec_mat_sc0024` AS `share_uptaken_sec_mat_sc0024`, \n"
                "`t2`.`recycling_rate_sc0022` AS `recycling_rate_sc0022`, \n"
                "`t3`.`recycling_rate_sc0023` AS `recycling_rate_sc0023`, \n"
                "`t4`.`recycling_rate_sc0024` AS `recycling_rate_sc0024`, \n"
                "`t2`.`recycling_rate_uptaken_sc0022` AS `recycling_rate_uptaken_sc0022`, \n"
                "`t3`.`recycling_rate_uptaken_sc0023` AS `recycling_rate_uptaken_sc0023`, \n"
                "`t4`.`recycling_rate_uptaken_sc0024` AS `recycling_rate_uptaken_sc0024` \n"
            "FROM \n"
                "(((((SELECT \n"
                    "`mfa_plastics_ch`.`results_optimization`.`plastic_type` AS `plastic_type`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`uptaken_sec_mat` AS `uptaken_sec_mat_sc0022`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`total_sec_mat` AS `total_sec_mat_sc0022`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`share_uptaken_sec_mat` AS `share_uptaken_sec_mat_sc0022`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`recycling_rate` AS `recycling_rate_sc0022`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`recycling_rate_uptaken` AS `recycling_rate_uptaken_sc0022` \n"
                "FROM \n"
                    "`mfa_plastics_ch`.`results_optimization` \n"
                "WHERE \n"
                    "(`mfa_plastics_ch`.`results_optimization`.`scenario` = 'sc0022'))) `t2` \n"
                "JOIN (SELECT  \n"
                        "`mfa_plastics_ch`.`results_optimization`.`plastic_type` AS `plastic_type`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`uptaken_sec_mat` AS `uptaken_sec_mat_sc0023`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`total_sec_mat` AS `total_sec_mat_sc0023`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`share_uptaken_sec_mat` AS `share_uptaken_sec_mat_sc0023`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`recycling_rate` AS `recycling_rate_sc0023`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`recycling_rate_uptaken` AS `recycling_rate_uptaken_sc0023` \n"
                "FROM \n"
                    "`mfa_plastics_ch`.`results_optimization` \n"
                "WHERE \n"
                    "(`mfa_plastics_ch`.`results_optimization`.`scenario` = 'sc0023')) `t3` ON ((`t2`.`plastic_type` = `t3`.`plastic_type`))) \n"
                "JOIN (SELECT \n"
                        "`mfa_plastics_ch`.`results_optimization`.`plastic_type` AS `plastic_type`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`uptaken_sec_mat` AS `uptaken_sec_mat_sc0024`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`total_sec_mat` AS `total_sec_mat_sc0024`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`share_uptaken_sec_mat` AS `share_uptaken_sec_mat_sc0024`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`recycling_rate` AS `recycling_rate_sc0024`, \n"
                        "`mfa_plastics_ch`.`results_optimization`.`recycling_rate_uptaken` AS `recycling_rate_uptaken_sc0024` \n"
                "FROM \n"
                    "`mfa_plastics_ch`.`results_optimization` \n"
                "WHERE \n"
                    "(`mfa_plastics_ch`.`results_optimization`.`scenario` = 'sc0024')) `t4` ON ((`t2`.`plastic_type` = `t4`.`plastic_type`))) \n"
                "JOIN `mfa_plastics_ch`.`plastic_types` `t5` ON ((`t2`.`plastic_type` = `t5`.`id_plastic_types`))) \n"
    )
    mfa_plastics_ch.commit()