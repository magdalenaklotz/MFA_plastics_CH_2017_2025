CREATE 
    ALGORITHM = UNDEFINED 
    SQL SECURITY DEFINER
VIEW `overall_results_opt` AS
    SELECT 
        (SELECT 
                SUM(`results_optimization`.`total_sec_mat`)
            FROM
                `results_optimization`
            WHERE
                (`results_optimization`.`scenario` = 'sc0022')
            GROUP BY `results_optimization`.`scenario`) AS `total_sec_mat_scen2`,
        (SELECT 
                SUM(`waste_scen2`.`waste_amount`)
            FROM
                `waste_scen2`) AS `total_waste_scen2`,
        (SELECT (`total_sec_mat_scen2` / `total_waste_scen2`) AS `overall RR scen2`) AS `overall_RR_scen2`,
        (SELECT 
                ((SELECT 
                            SUM(`results_optimization`.`uptaken_sec_mat`)
                        FROM
                            `results_optimization`
                        WHERE
                            (`results_optimization`.`scenario` = 'sc0022')
                        GROUP BY `results_optimization`.`scenario`) / `total_waste_scen2`)
            ) AS `TRR_high_appl`,
        (SELECT 
                ((SELECT 
                            SUM(`results_optimization`.`uptaken_sec_mat`)
                        FROM
                            `results_optimization`
                        WHERE
                            (`results_optimization`.`scenario` = 'sc0023')
                        GROUP BY `results_optimization`.`scenario`) / `total_waste_scen2`)
            ) AS `TRR_mod_appl`,
        (SELECT 
                ((SELECT 
                            SUM(`results_optimization`.`uptaken_sec_mat`)
                        FROM
                            `results_optimization`
                        WHERE
                            (`results_optimization`.`scenario` = 'sc0024')
                        GROUP BY `results_optimization`.`scenario`) / `total_waste_scen2`)
            ) AS `TRR_low_appl`