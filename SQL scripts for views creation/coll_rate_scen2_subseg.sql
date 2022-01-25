CREATE 
    ALGORITHM = UNDEFINED 
    SQL SECURITY DEFINER
VIEW `coll_rate_scen2_subseg` AS
    SELECT 
        `t1`.`id_subsegments` AS `id_subsegments`,
        `t2`.`waste` AS `waste`,
        `t1`.`sep_coll` AS `sep_coll`,
        (`t1`.`sep_coll` / `t2`.`waste`) AS `sep_coll/waste`
    FROM
        (((SELECT 
            `separate_collection_scen2`.`id_subsegments` AS `id_subsegments`,
                `separate_collection_scen2`.`name_subsegments` AS `name_subsegments`,
                `separate_collection_scen2`.`sep_coll` AS `sep_coll`
        FROM
            `mfa_plastics_ch`.`separate_collection_scen2`)) `t1`
        JOIN (SELECT 
            `mfa_plastics_ch`.`waste_scen2`.`subsegment` AS `subsegment`,
                SUM(`mfa_plastics_ch`.`waste_scen2`.`waste_amount`) AS `waste`
        FROM
            `mfa_plastics_ch`.`waste_scen2`
        GROUP BY `mfa_plastics_ch`.`waste_scen2`.`subsegment`) `t2` ON ((`t1`.`id_subsegments` = `t2`.`subsegment`)))