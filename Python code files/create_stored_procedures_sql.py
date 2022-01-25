def create_stored_procedures_sql(mfa_plastics_ch, mycursor):

    # creating sql procedure for creating flows without flow value for all plastic types in all subsegments between two specified processes for a certain scenario and year
    mycursor.execute(   "CREATE PROCEDURE `create_flows_pr_to_pr_scen`( \n"
                        "in originating_process varchar(45), \n"
                        "in destination_process varchar(45), \n"
                        "in scenario varchar(45), \n"
                        "in year_flows varchar(4) \n"
                        ") \n"
                        "BEGIN \n"
                        "declare x int(4) zerofill; -- counter plastic types \n"
                        "declare y int(4) zerofill; -- counter subsegments \n" 
                        "declare idflows_number_temp int(10) zerofill;  -- idflows number (= idflows without 'fl') has 10 digits filled from left with 0s \n"
                        "declare idflows_temp varchar(12); \n"

                        "set x = 1; \n"

                            "loop_plastic_types: loop \n"
                                "if x > 11 then \n"
                                    "leave loop_plastic_types; \n"
                                    "end if; \n"
                                "set y = 1; \n"

                                "loop_subsegments: loop \n"
                                    "if y > 54 then \n"
                                    "leave loop_subsegments; \n" 
                                    "end if; \n"

                                    "set idflows_number_temp = ((select distinct substring((select max(id_flows) from flows), -10)) +1); -- selecting highest number of idflows(without 'fl', number has 10 digits) increased by 1 \n"
                                    "set idflows_temp = concat('fl', idflows_number_temp); \n"

                                    "insert into flows(id_flows, origin_flows, `subsegment_origin_flows`, destination_flows, `subsegment_destination_flows`, plastic_type_flows, year_flows, value_flows, scenario_flows) values( \n"
                                        "idflows_temp, \n"
                                        "originating_process, \n"
                                        "(select concat('su', y)), -- subsegment \n"
                                        "destination_process, \n"
                                        "(select concat('su', y)), -- subsegment \n"
                                        "(select \n"
                                        "concat('pl', x)), -- plastic type \n"
                                        "year_flows, \n"
                                        "null, \n"
                                        "scenario \n"
                                    "); \n"

                                    "set y = y + 1; \n"
                                "end loop; \n"

                                "set x = x + 1; \n"
                            "end loop; \n"
                        "END ")
    mfa_plastics_ch.commit()
