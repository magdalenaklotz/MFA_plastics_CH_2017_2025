CREATE 
    ALGORITHM = UNDEFINED 
    SQL SECURITY DEFINER
VIEW `uptaken_sec_mat_subseg_plast_high_applic` AS
    SELECT 
        `tHDPE`.`subsegment` AS `subsegment`,
        `tHDPE`.`allocated_secondary_material_HDPE` AS `allocated_secondary_material_HDPE`,
        `tLDPE`.`allocated_secondary_material_LDPE` AS `allocated_secondary_material_LDPE`,
        `tPET`.`allocated_secondary_material_PET` AS `allocated_secondary_material_PET`,
        `tPP`.`allocated_secondary_material_PP` AS `allocated_secondary_material_PP`,
        `tPS`.`allocated_secondary_material_PS` AS `allocated_secondary_material_PS`,
        `tPVC`.`allocated_secondary_material_PVC` AS `allocated_secondary_material_PVC`,
        `tABS`.`allocated_secondary_material_ABS` AS `allocated_secondary_material_ABS`,
        `tHIPS`.`allocated_secondary_material_HIPS` AS `allocated_secondary_material_HIPS`
    FROM
        (((((((((SELECT 
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` AS `subsegment`,
                `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`allocated_secondary_material` AS `allocated_secondary_material_HDPE`
        FROM
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`
        WHERE
            ((`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`plastic_type` = 'pl0001')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`scenario` = 'sc0022')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` <> 'variable')))) `tHDPE`
        JOIN (SELECT 
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` AS `subsegment`,
                `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`allocated_secondary_material` AS `allocated_secondary_material_LDPE`
        FROM
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`
        WHERE
            ((`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`plastic_type` = 'pl0002')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`scenario` = 'sc0022')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` <> 'variable'))) `tLDPE` ON ((`tHDPE`.`subsegment` = `tLDPE`.`subsegment`)))
        JOIN (SELECT 
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` AS `subsegment`,
                `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`allocated_secondary_material` AS `allocated_secondary_material_PET`
        FROM
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`
        WHERE
            ((`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`plastic_type` = 'pl0003')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`scenario` = 'sc0022')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` <> 'variable'))) `tPET` ON ((`tHDPE`.`subsegment` = `tPET`.`subsegment`)))
        JOIN (SELECT 
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` AS `subsegment`,
                `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`allocated_secondary_material` AS `allocated_secondary_material_PP`
        FROM
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`
        WHERE
            ((`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`plastic_type` = 'pl0004')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`scenario` = 'sc0022')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` <> 'variable'))) `tPP` ON ((`tHDPE`.`subsegment` = `tPP`.`subsegment`)))
        JOIN (SELECT 
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` AS `subsegment`,
                `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`allocated_secondary_material` AS `allocated_secondary_material_PS`
        FROM
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`
        WHERE
            ((`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`plastic_type` = 'pl0005')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`scenario` = 'sc0022')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` <> 'variable'))) `tPS` ON ((`tHDPE`.`subsegment` = `tPS`.`subsegment`)))
        JOIN (SELECT 
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` AS `subsegment`,
                `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`allocated_secondary_material` AS `allocated_secondary_material_PVC`
        FROM
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`
        WHERE
            ((`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`plastic_type` = 'pl0006')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`scenario` = 'sc0022')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` <> 'variable'))) `tPVC` ON ((`tHDPE`.`subsegment` = `tPVC`.`subsegment`)))
        JOIN (SELECT 
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` AS `subsegment`,
                `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`allocated_secondary_material` AS `allocated_secondary_material_ABS`
        FROM
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`
        WHERE
            ((`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`plastic_type` = 'pl0007')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`scenario` = 'sc0022')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` <> 'variable'))) `tABS` ON ((`tHDPE`.`subsegment` = `tABS`.`subsegment`)))
        JOIN (SELECT 
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` AS `subsegment`,
                `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`allocated_secondary_material` AS `allocated_secondary_material_HIPS`
        FROM
            `mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`
        WHERE
            ((`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`plastic_type` = 'pl0008')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`scenario` = 'sc0022')
                AND (`mfa_plastics_ch`.`uptaken_secondary_material_subsegments_plastic_types`.`subsegment` <> 'variable'))) `tHIPS` ON ((`tHDPE`.`subsegment` = `tHIPS`.`subsegment`)))