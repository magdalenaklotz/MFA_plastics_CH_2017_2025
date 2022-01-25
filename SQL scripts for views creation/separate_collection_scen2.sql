CREATE 
    ALGORITHM = UNDEFINED 
    SQL SECURITY DEFINER
VIEW `separate_collection_scen2` AS
    SELECT 
        `t2`.`id_subsegments` AS `id_subsegments`,
        `t2`.`name_subsegments` AS `name_subsegments`,
        `t1`.`sep_coll` AS `sep_coll`
    FROM
        (((SELECT 
            `mfa_plastics_ch`.`flows`.`subsegment_destination_flows` AS `subsegment_destination_flows`,
                SUM(`mfa_plastics_ch`.`flows`.`value_flows`) AS `sep_coll`
        FROM
            `mfa_plastics_ch`.`flows`
        WHERE
            ((`mfa_plastics_ch`.`flows`.`scenario_flows` = 'sc0002')
                AND (`mfa_plastics_ch`.`flows`.`origin_flows` = 'pr0008')
                AND (`mfa_plastics_ch`.`flows`.`destination_flows` NOT IN ('pr0002' , 'pr0003', 'pr0029')))
        GROUP BY `mfa_plastics_ch`.`flows`.`subsegment_destination_flows`)) `t1`
        JOIN `mfa_plastics_ch`.`subsegments` `t2` ON ((`t1`.`subsegment_destination_flows` = `t2`.`id_subsegments`)))
    ORDER BY `t2`.`id_subsegments`