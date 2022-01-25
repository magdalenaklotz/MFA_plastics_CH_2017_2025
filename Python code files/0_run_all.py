import mysql.connector

# connecting to database
mfa_plastics_ch = mysql.connector.connect(
    host="<your_db_host>",                              # e.g. server_name.ethz.ch
    user="<your_db_user_name>",                         # e.g. magdalenaklotz
    passwd="<your_db_user_password>",                   # e.g. mypassword
    database="<your_db_schema_name>")                   # e.g. mfa_plastics
# print(mfa_plastics_ch)
mycursor = mfa_plastics_ch.cursor()



# MFA for 2017

from create_stored_procedures_sql import create_stored_procedures_sql
create_stored_procedures_sql(mfa_plastics_ch, mycursor)
"""
create sql stored procedures called via python scripts
"""

from excel_read_in import excel_read_in
excel_read_in(mfa_plastics_ch, mycursor)
"""
- creating tables and reading in data on scenarios, segments, subsegments, plastic types, processes, TCs (see below), flows (see below)
- reading in all flows for all plastic types for all subsegments from flows from Production CH / Production abroad (over Use and Collection and Sorting) till flows into Recycling, incl. flows to Energy recovery
(for Packaging only until flows into Sorting)
- reading in TCs for Packaging for Sorting to Recycling and Energy recovery - converted from definition in Excel file via process, subsegment and plastic type to TCs from flow to flow,
and creation of flows without flow value for Packaging from Sorting to Recycling and Energy recovery),
- reading in TCs for all Recycling processes (in slightly different format than for Packaging TCs, but from same sheet, writing into separate table in the db) [actually read in for all Packaging Sorting processes as well, but later only used for Recycling processes]
- creation of tables for storing waste amounts in 2025,
amounts secondary material in different scenarios (on subsegment level),
uptaken secondary material amounts,
optimization results
"""

from pack_calc_flows_56 import pack_calc_flows_56
pack_calc_flows_56(mfa_plastics_ch, mycursor)
"""
- calculation of flows from Sorting into Recycling and Energy Recovery via TCs read-in for Packaging (so that all flows into Recycling are in db)
"""

from calc_sec_mat_scen_1 import calc_sec_mat_scen_1
calc_sec_mat_scen_1(mfa_plastics_ch, mycursor)
"""
- calculation of amount secondary material from flows into Recycling via Recycling TCs read-in for all subsegments and plastic types for scenario 1 (2017)
- writing calculated secondary material flows in table 'secondary_material_subsegments_plastic_types' in db
(NOTE: the secondary material amounts are only stored in this table, not in the 'flows' table)
"""

from calc_rec_losses import calc_rec_losses
calc_rec_losses(mfa_plastics_ch, mycursor)
"""
- calculation of flow amounts of Recycling losses into waste-to-energy plants and cement kilns in CH and abroad
based on flows into Recycling via Recycling TCs read-in for all subsegments and plastic types for scenario 1
- writing calculated secondary material flows in secondary-material table in db
"""



# SCENARIO FOR 2025

from calc_TCs_3_4 import calc_TCs_3_4
calc_TCs_3_4(mfa_plastics_ch, mycursor)
"""
- calculation of TCs for read-in flows for Use (LC stage 3) and Collection (LC stage 4) (so from into Use to till Sorting)
(NOTE: TCs for 3 are applied to the Use amounts, but the collection rate refers to the Waste amounts, thus, a specified collection rate needs to be multiplied with amount_waste/amount_use if meant to be used as TC for LC stage 3 to calculate the Collection amounts from the Use amounts)
"""

from calc_TCs_5_other_than_pack import calc_TCs_5_other_than_pack
calc_TCs_5_other_than_pack(mfa_plastics_ch, mycursor)
"""
- calculation of TCs for Sorting for other than Packaging flows (read in for Packaging) for sc0001 (because same in sc0002 - in scen_2 taken over)
"""

from scen_2 import scen_2
scen_2(mfa_plastics_ch, mycursor)
"""
[NOTE: sums up if run several subsequent times]
- inserting sc0002 in scenario table and creating all empty flows
- inserting use amounts scaled up from scenario 1 into flows for scenario 2
- calculating TCs for Use (to Collection) so that overall specified (higher-than-in-2017) collection rate is reached,
while shares going to different separate collection systems are kept constant
(some adjustments are done for obtaining correct results, see description in code),
increased waste amounts considered
- writing same TCs as for scenario 1 for Collection and Sorting in TC table for scenario 2
- calculating flows from Use to into Recycling starting from flows into Use via TCs for scenario 2
- calculating secondary material from flows into Recycling via respective TCs and store in db table for secondary material
"""

from allocation_sec_mat import allocation_sec_mat
allocation_sec_mat(mycursor)
"""
- getting definition and value of all individual flows into the different recycling processes
- inserting values of flows into recycling processes into Excel file “flows_into_rec_suitability_sec_mat” (the order is correct),
where recycling efficiencies are specified and via those, the values of all secondary material flows leaving recycling are calculated;
in the same Excel file, for each flow out from recycling, the suitable uptaking product subsegments are specified,
based on which the optimization is carried out (in the next step)
"""

from optimization import optimization
optimization(mfa_plastics_ch, mycursor)
"""
- based on the amounts of the individual flows leaving recycling and specified product subsegments in which the respective flows can be utilized
(from Excel file “flows_into_rec_suitability_sec_mat”), for each plastic type, the secondary material is allocated to the suitable uptaking product subsegments,
considering the applicable amount of secondary material in each product subsegment,
calculated via the forecasted demand in 2025 (consumption amount) and the shares of secondary material that can be applied in each product subsegment (specified in Excel file 'demand_reduction'),
so to maximize the total uptaken secondary material amount
"""

from results_depiction import results_depiction
results_depiction(mfa_plastics_ch, mycursor)
"""
- figures are created and shown as well as stored in the project folder regarding:
    . total secondary material amounts in 2025 and uptaken secondary material amounts for each sub-scenario
    . recycling rate in 2025 and true recycling rates for each sub-scenario
    . total demand coverable by secondary material and uptaken secondary material for all subsegments in each sub-scenario for each plastic type
"""