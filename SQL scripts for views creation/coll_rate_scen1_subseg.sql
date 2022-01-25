CREATE 
    ALGORITHM = UNDEFINED 
    SQL SECURITY DEFINER
VIEW `coll_rate_scen1_subseg` AS
    SELECT 
        `t1`.`subsegment_origin_flows` AS `subsegment_origin_flows`,
        `t1`.`total_waste` AS `total_waste`,
        `t2`.`collected_waste` AS `collected_waste`,
        (`t2`.`collected_waste` / `t1`.`total_waste`) AS `collected_waste/total_waste`
    FROM
        (((SELECT 
            `mfa_plastics_ch`.`flows`.`subsegment_origin_flows` AS `subsegment_origin_flows`,
                SUM(`mfa_plastics_ch`.`flows`.`value_flows`) AS `total_waste`
        FROM
            `mfa_plastics_ch`.`flows`
        WHERE
            ((`mfa_plastics_ch`.`flows`.`scenario_flows` = 'sc0001')
                AND (`mfa_plastics_ch`.`flows`.`origin_flows` = 'pr0008'))
        GROUP BY `mfa_plastics_ch`.`flows`.`subsegment_origin_flows`)) `t1`
        JOIN (SELECT 
            `mfa_plastics_ch`.`flows`.`subsegment_origin_flows` AS `subsegment_origin_flows`,
                SUM(`mfa_plastics_ch`.`flows`.`value_flows`) AS `collected_waste`
        FROM
            `mfa_plastics_ch`.`flows`
        WHERE
            ((`mfa_plastics_ch`.`flows`.`scenario_flows` = 'sc0001')
                AND (`mfa_plastics_ch`.`flows`.`origin_flows` = 'pr0008')
                AND (`mfa_plastics_ch`.`flows`.`destination_flows` NOT IN ('pr0029' , 'pr0002', 'pr0003')))
        GROUP BY `mfa_plastics_ch`.`flows`.`subsegment_origin_flows`) `t2` ON ((`t1`.`subsegment_origin_flows` = `t2`.`subsegment_origin_flows`)))