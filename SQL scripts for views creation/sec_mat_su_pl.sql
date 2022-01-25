CREATE 
    ALGORITHM = UNDEFINED 
    SQL SECURITY DEFINER
VIEW `sec_mat_su_pl` AS
    SELECT 
        `t2`.`name_subsegments` AS `name_subsegments`,
        `t3`.`name_plastic_types` AS `name_plastic_types`,
        `t4`.`id_scenarios` AS `id_scenarios`,
        ROUND(`t1`.`amount_secondary_material`, 0) AS `amount_secondary_material`
    FROM
        (((`secondary_material_subsegments_plastic_types` `t1`
        JOIN `subsegments` `t2` ON ((`t1`.`subsegment` = `t2`.`id_subsegments`)))
        JOIN `plastic_types` `t3` ON ((`t1`.`plastic_type` = `t3`.`id_plastic_types`)))
        JOIN `scenarios` `t4` ON ((`t1`.`scenario` = `t4`.`id_scenarios`)))