CREATE 
    ALGORITHM = UNDEFINED 
    SQL SECURITY DEFINER
VIEW `use_amounts_subsegments_sorted` AS
    SELECT 
        `t2`.`name_subsegments` AS `name_subsegments`,
        `t1`.`use_amount` AS `use_amount`
    FROM
        (((SELECT 
            `mfa_plastics_ch`.`flows`.`subsegment_destination_flows` AS `subsegment_destination_flows`,
                SUM(`mfa_plastics_ch`.`flows`.`value_flows`) AS `use_amount`
        FROM
            `mfa_plastics_ch`.`flows`
        WHERE
            ((`mfa_plastics_ch`.`flows`.`scenario_flows` = 'sc0001')
                AND (`mfa_plastics_ch`.`flows`.`destination_flows` = 'pr0008'))
        GROUP BY `mfa_plastics_ch`.`flows`.`subsegment_destination_flows`)) `t1`
        JOIN `mfa_plastics_ch`.`subsegments` `t2` ON ((`t1`.`subsegment_destination_flows` = `t2`.`id_subsegments`)))
    ORDER BY `t1`.`use_amount` DESC