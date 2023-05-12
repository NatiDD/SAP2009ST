import math

def sap_data(i):
    sap_data_input = ["detached,0,0,0,0,0,0,0,2,0,0,0,100,10,1,0,0,0,0,0,0,0,0,2,0.0152,150,0,360,0,0,0,0.48,0,0,42,0.76,0.7,1,90,10,0.76,0.7,1,180,48,0.76,0.7,1,270,0,0.76,0.7,1,21,1,1,0,0,0,0,91,0,0,91,175,0,0,3.1,0,0,3.1,11.46,11.46,0,0,106,0.198,0,0,0.198,0.517,0.517,0,0,1.58,13.97,38,0,113.53,0,38,2,2,0.25,0.25,0.3,0,0.2",
    "semidetached,0,0,0,0,0,0,0,2,0,0,0,100,10,2,0,0,0,0,0,0,0,0,2,0.0152,150,0,360,0,0,0,0.48,0,0,45,0.76,0.7,1,90,5,0.76,0.7,1,180,50,0.76,0.7,1,270,0,0.76,0.7,1,21,1,1,0,0,0,0,91,0,0,91,175,0,0,3.1,0,0,3.1,11.46,11.46,0,0,106,0.198,0,0,0.198,0.517,0.517,0,0,1.58,13.97,38,0,73.53,40,38,2,2,0.25,0.25,0.3,0.2,0.2",
    "terraced,0,0,0,0,0,0,0,2,0,0,0,100,10,3,0,0,0,0,0,0,0,0,2,0.0152,150,0,360,0,0,0,0.48,0,0,45,0.76,0.7,1,90,0,0.76,0.7,1,180,55,0.76,0.7,1,270,0,0.76,0.7,1,21,1,1,0,0,0,0,91,0,0,91,175,0,0,3.1,0,0,3.1,11.46,11.46,0,0,106,0.198,0,0,0.198,0.517,0.517,0,0,1.58,13.11,38,0,34.39,80,38,2,2,0.25,0.25,0.3,0.2,0.2",
    "midflat,0,0,0,0,0,0,0,1,0,0,0,100,10,3,0,0,0,0,0,0,0,0,2,0.0152,150,0,360,0,0,0,0.48,0,0,0,0.76,0.7,1,90,0,0.76,0.7,1,180,100,0.76,0.7,1,270,0,0.76,0.7,1,21,1,1,0,0,0,0,91,0,0,91,175,0,0,3.1,0,0,3.1,11.46,11.46,0,0,106,0.198,0,0,0.198,0.517,0.517,0,0,0,3.215,0,0,20.535,51.875,0,2,2,0.25,0.25,0.3,0.2,0.2"
    ]
    return sap_data_input[int(i)]

def sap_result(instring,intemp,replace_what,replace_with,dimension_out,in_wall_area,in_floor_area,in_win_north,in_win_east,in_win_south,in_win_west):
# based sap_engine_ww.php

#instring =_GET['code']
#intemp =_GET['temp']
#replace_what =_GET['replace']
#replace_with =_GET['with']
#dimension_out =_GET['dimensions']
    print("enter SAP result")
    return_string = ""
    if (replace_what!="" and replace_with!="" and instring !=""):
        instring = instring.replace(replace_what,replace_with)

    dhwcalc = 0
    DHW_usage = [0,0,0,0,0,0,0,0,0,0,0,0]
    dhw_eng_cont = 0
    dhw_dist_loss = 0
    dhw_cylinder_loss = 0
    DHW_heat_out = [0,0,0,0,0,0,0,0,0,0,0,0]
    dhw_heat_gain = 0
    DHW_gains = [0,0,0,0,0,0,0,0,0,0,0,0]
    heat_require = [0,0,0,0,0,0,0,0,0,0,0,0]
    temp_eff_water = 100

    month_windspeed  =[5.4, 5.1, 5.1, 4.5, 4.1, 3.9, 3.7, 3.7, 4.2, 4.5, 4.8, 5.1]
    number_of_days =[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    hot_water_factor =[1.1, 1.06, 1.02, 0.98, 0.94, 0.9, 0.9, 0.94, 0.98, 1.02, 1.06, 1.1]
    drawoff_temp_rise =[41.2, 41.4, 40.1, 37.6, 36.4, 33.9, 30.4, 33.4, 33.5, 36.3, 39.4, 39.9]
    solar_radiaion =[26, 54, 94, 150, 190, 201, 194, 164, 116, 68, 33, 21]
    solar_declination =[-20.7, -12.8, -1.8, 9.8, 18.8, 23.1, 21.2, 13.7, 2.9, -8.7, -18.4, -23]
    external_temp =[4.5, 5.0, 6.8, 8.7, 11.7, 14.6, 16.9, 16.9, 14.3, 10.8, 7, 4.9]
    region_summer_solar =[214,204,177,214,204,177,225,213,186,225,213,190,218,208,186,218,208,184,204,194,168,196,186,159,192,187,156,186,178,149,188,183,154,201,194,164,212,203,173,209,198,172,186,183,154,187,177,146,187,170,142,181,163,140,189,175,147,199,178,141,183,163,138,188,175,152]
    region_summer_temp =[15.4,17.8,17.8,15.4,17.8,17.8,15.2,17.6,17.8,15.2,17.4,17.6,14.7,16.8,17,15.2,17.4,17.3,14.9,17.2,17.1,14.5,16.6,16.5,13.5,15.5,15.4,13.4,15.5,15.4,14,16.2,16.1,14.6,16.9,16.9,15,17.5,17.6,14.3,16.4,16.3,13.1,14.9,14.8,13.2,15.2,15,12.8,14.9,14.7,12.5,14.5,14.4,11.7,13.7,13.7,11.2,13.3,13.6,10.6,12.7,13,13.4,15.4,15.2]
    region_lat =[51.5,51.5,51,50.8,50.6,51.5,52.7,53.4,54.8,55.5,54.5,53.4,52.3,52.5,55.8,56.4,57.2,57.5,58,59,60.2,54.7]				
    overhang_N_array =[1,1,1,1,1,1,1,1,0.94,0.9,0.88,0.86,0.85,0.84,1,0.92,0.85,0.79,0.73,0.69,0.66]
    overhang_NE_array =[1,1,1,1,1,1,1,1,0.91,0.85,0.81,0.79,0.77,0.76,1,0.89,0.8,0.72,0.65,0.59,0.55]
    overhang_E_array =[1,1,1,1,1,1,1,1,0.89,0.79,0.72,0.66,0.61,0.57,1,0.88,0.76,0.66,0.58,0.51,0.46]
    overhang_SE_array =[1,1,1,1,1,1,1,1,0.84,0.72,0.62,0.55,0.52,0.5,1,0.83,0.67,0.54,0.43,0.36,0.31]
    overhang_S_array =[1,1,1,1,1,1,1,1,0.79,0.64,0.53,0.5,0.49,0.48,1,0.77,0.55,0.38,0.32,0.3,0.29]

    PV_array =[0,3.5,7,10.5,14,17.5,21,24.5,28]
    PV_locations =[1150,1100,1050,1000,950,900,850,800]

    WallUValue_array  =[2.1,2.0,1.7,1.0,0.6,0.45,0.35,0.3,0.25,0.2,0.15,0.10]
    FloorUValue_array =[2.0,0.6,0.45,0.3,0.25,0.2,0.15,0.14,0.13,0.12,0.11,0.10]
    RoofUValue_array =[2.0,1.5,1.,0.6,0.35,0.25,0.2,0.13,0.1]
    WindowUValue_array =[4.8,3.1,3,2.2,2,1.8,1.6,1.4,1.2,1,0.8]
    thermalbridge_array =[0.15,0.08,0.04]
#for the size of the building
    Glazingratio_array =[0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50]
    floorarea_array =[50,60,70,80,90,100,110,120]
    livingarea_array =[22.5,18,17.5,18.4,18.9,21,20.9,19.2]

    externalwall_array = [70.7, 77.5, 83.7, 89.4, 94.9, 100.0, 104.9, 109.5, 72.7, 79.6, 86.0, 91.9, 97.5, 102.8, 107.8, 112.6, 79.6, 87.2, 94.2, 100.7, 106.8, 112.6, 118.1, 123.3, 79.6, 87.2, 94.2, 100.7, 106.8, 112.6, 118.1, 123.3, 72.7, 79.6, 86.0, 91.9, 97.5, 102.8, 107.8, 112.6,
            53.0, 58.1, 62.7, 67.1, 71.2, 75.0, 78.7, 82.2, 50.3, 55.1, 59.5, 63.6, 67.5, 71.2, 74.6, 77.9, 50.6, 55.4, 59.8, 64.0, 67.8, 71.5, 75.0, 78.3, 68.9, 75.4, 81.5, 87.1, 92.4, 71.5, 75.0, 78.3, 58.7, 64.3, 69.5, 74.2, 78.8, 71.2, 74.6, 77.9,
            35.4, 38.7, 41.8, 44.7, 47.4, 50.0, 52.4, 54.8, 28.0, 30.6, 33.1, 35.4, 37.5, 39.5, 41.5, 43.3, 21.5, 23.6, 25.5, 27.2, 28.9, 30.4, 31.9, 33.3, 58.1, 63.6, 68.7, 73.5, 77.9, 30.4, 31.9, 33.3, 44.7, 49.0, 52.9, 56.6, 60.0, 39.5, 41.5, 43.3,
            17.7, 19.4, 20.9, 22.4, 23.7, 25.0, 26.2, 27.4, 14.0, 15.3, 16.5, 17.7, 18.8, 19.8, 20.7, 21.7, 10.8, 11.8, 12.7, 13.6, 14.4, 15.2, 16.0, 16.7, 29.0, 31.8, 34.4, 36.7, 39.0, 15.2, 16.0, 16.7, 22.4, 24.5, 26.5, 28.3, 30.0, 19.8, 20.7, 21.7]


# efficiency is split into new and old
    system_efficiency_array = [100,70,93,91,320,70, 100,70,93,91,320,70, 100,65,66,66,320,65, 100,50,50,50,320,50, 100,32,50,40,320,37]
    water_efficiency_array = [100,70,93,91,320,70, 100,70,93,91,320,70, 100,65,54,56,320,65, 100,50,50,50,320,50, 100,32,50,40,320,37]
    system_fuel_array = [4.78,2.97,4.06,3.1,11.46,2.49,   4.78,2.97,4.06,3.1,11.46,2.49,  4.78,2.97,4.06,3.1,11.46,2.49, 6.17,2.97,4.06,3.1,11.46,2.49,  11.46,3.73,4.06,5.73,11.46,2.49]
    system_co2_array = [0.517,0.301,0.274,0.198,0.517,0.009]
    responsivness_array = [0.75,0.75,1,1,1,1, 0.5,0.75,1,1,1,1, 0.5,0.75,1,1,1,1, 0.5,0.75,1,1,1,1, 0.25,0.5,1,1,1,1]
    heat_control_array = [3,3,3,3,3,3, 2,2,2,2,2,2, 2,2,2,2,2,2, 2,2,2,2,2,2, 1,1,1,1,1,1]
    temp_adjust_array = [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0.6,0,0,0,0,0, 0.3,0.6,0.6,0.6,0.3,0.6]
    second_eff_array = [0,100,63,55,35,250,35]
    second_fuel_array = [0,4.78,3.1,4.06,2.97,11.46,2.49]
    second_co2_array = [0,0.517,0.198,0.274,0.301,0.517,0.009]
    pumpgains_array = [0,10,20,10,10,10]
    pumpenergy_array = [0,130,230,175,135,135]
    fuelfactor_array = [1.47,1.28,1.17,1.0,1.47,1.0]

    q50_array =[20,10,5,3]
    solar_thermal_energy_array  =[0,30,60,90,120,150,180]
    solar_thermal_tank_volume_array  =[0,200,200,300,300,400,400]

    effective_ach_array =[0.1,0.8,3,6,0.1,0.5,2,4,0.2,1,4,8,0.1,0.6,2.5,5]
    blinds_array =[0.24,0.27,0.60,0.65,0.70,0.8,0.85,0.88,0.99,1]

    win_orient =[0,0,0,0]
    out_win_orient =[0,0,0,0]
    win_area =[0,0,0,0]
    out_win_area =[0,0,0,0]
    win_g =[0,0,0,0]
    win_ff =[0,0,0,0]
    win_access =[0,0,0,0]
    fab_area =[0,0,0,0,0,0,0,0,0,0]
    out_fab_area =[0,0,0,0,0,0,0,0,0,0]
    fab_uvalue =[0,0,0,0,0,0,0,0,0,0]

    light_c2_calc =0

    vent_type = 0
    ventcalc = 0
    Mventcalc = [0,0,0,0,0,0,0,0,0,0,0,0]
    air_change = [0,0,0,0,0,0,0,0,0,0,0,0]
    fab_loss = 0
    N = 0
    number_people = 0
    dhw_volume = 0
    HLP = [0,0,0,0,0,0,0,0,0,0,0,0]
    gains_app = 0
    gains_lighting = 0
    gains_met = 0
    gains_cooking = 0
    light_energy = 0
    other_losses = 0
    int_gains = 0
    total_int_gains = [0,0,0,0,0,0,0,0,0,0,0,0]

    solar_gains = [0,0,0,0,0,0,0,0,0,0,0,0]
    solar_coeff_a = 0
    solar_coeff_b = 0
    solar_coeff_c = 0
    Rhtov = 0
    total_gains = [0,0,0,0,0,0,0,0,0,0,0,0]

    heat_off = [0,0,0,0]
    time_constant = 0
    util_a = 0
    util_y = 0
    util_factor = 0
    temp_noheat = 0
    temp_t1 = [0,0,0,0,0,0,0,0,0,0,0,0]
    temp_u = [0,0,0,0]
    temp_rest = 0
    temp_t2 = [0,0,0,0,0,0,0,0,0,0,0,0]
    internal_temp = [0,0,0,0,0,0,0,0,0,0,0,0]

    heat_sys_main1 = [0,0,0,0,0,0,0,0,0,0,0,0]
    heat_sys_main2 = [0,0,0,0,0,0,0,0,0,0,0,0]
    heat_sys_water = [0,0,0,0,0,0,0,0,0,0,0,0]
    heat_sys_second = [0,0,0,0,0,0,0,0,0,0,0,0]

    tot_co2 = 0
    tot_cost = 0
    DER = 0
    TER = 0
    TER_Calc = 0
    ecf = 0
    sap = 0
    heating_out = 0
    PV_out = 0
    OH = [0,1,2,1,2,0,2,0,1,1,1,1]
    AppElec_calc = 0
    AppElec_total = 0
    FF = 1.170
    EFAh = 0.198/0.194
    EFAl = 0.517/0.422

    eff_app = 0
    eff_light = 0
    eff_cook = 0

    heating_age  = 0

    typology_value =0
    window_opening  = 2
    Zsummer  = 0
    summer_solar_gains = 0
    summer_gains_ratio = 0
    summer_int_gains =[0,0,0,0,0,0,0,0,0,0,0,0]
    Tthreshold = 0
    region_value = 0
    blind =0
    overhang_type =0

    heating = 0
    annual_sys_main1 = 0
    annual_sys_main2 = 0
    annual_sys_second = 0
    annual_sys_water = 0

# new variables for warm wales
    total_heating_out = 0
    total_heating_second = 0
    total_water_heating_out = 0

# split the input line
    line_vars = instring.split("_")
#building type
    typology_value = line_vars[27]

# *****************************************************************************************
# load database
# *****************************************************************************************

    in_fields = sap_data(typology_value).split(",")

    Buildname = in_fields[0]
    floor_area= float(in_fields[1])
    total_volume= float(in_fields[2])
    num_chim= float(in_fields[3])
    num_flue= float(in_fields[4])
    num_fan= float(in_fields[5])
    num_passvent= float(in_fields[6])
    num_flueless= float(in_fields[7])
    num_storey= float(in_fields[8])
    constr_type= in_fields[9]
    floor_type= in_fields[10]
    drau_lobby= in_fields[11]
    num_strip= float(in_fields[12])
    q50= float(in_fields[13])
    num_shelt= float(in_fields[14])
    exhaust_heatpump= float(in_fields[15])
    mvhr_efficency= float(in_fields[16])
    vent_type= in_fields[17]
    ext_ele_area= float(in_fields[18])
    fabric_heat_loss= float(in_fields[19])
    heat_capacity= float(in_fields[20])
    thermal_bridge= float(in_fields[21])
    water_target= float(in_fields[22])
    dhw_source= int(in_fields[23])
    tank_loss= float(in_fields[24])
    tank_volume= float(in_fields[25])
    solar_storage_volume= float(in_fields[26])
    circuit_loss= float(in_fields[27])
    combi_loss= float(in_fields[28])
    solar_energy= float(in_fields[29])
    new_dwelling= in_fields[30]
    light_c1_c2= float(in_fields[31])
    pump_gains= float(in_fields[32])
    for i in range(0,4,1):
        win_orient[i] = float(in_fields[i * 5 + 33])
        win_area[i] = float(in_fields[i * 5 + 34])
        win_g[i] = float(in_fields[i * 5 + 35])
        win_ff[i] = float(in_fields[i * 5 + 36])
        win_access[i] = float(in_fields[i * 5 + 37])
    internal_temp_set= float(in_fields[53])
    responsiveness= float(in_fields[54])
    heat_control= in_fields[55]
    living_area= float(in_fields[56])
    temp_adjust= float(in_fields[57])
    second_fraction= float(in_fields[58])
    main2_fraction= float(in_fields[59])
    eff_main1= float(in_fields[60])
    eff_main2= float(in_fields[61])
    eff_second= float(in_fields[62])
    eff_water= float(in_fields[63])
    elec_fan_pumps= float(in_fields[64])
    elec_renew_gen= float(in_fields[65])
    elec_renew_used= float(in_fields[66])
    fuel_main1= float(in_fields[67])
    fuel_main2= float(in_fields[68])
    fuel_second= float(in_fields[69])
    fuel_water= float(in_fields[70])
    fuel_pumps= float(in_fields[71])
    fuel_lights= float(in_fields[72])
    fuel_renew_gen= float(in_fields[73])
    fuel_renew_used= float(in_fields[74])
    standing_charges= float(in_fields[75])
    co2_main1= float(in_fields[76])
    co2_main2= float(in_fields[77])
    co2_second= float(in_fields[78])
    co2_water= float(in_fields[79])
    co2_pumps= float(in_fields[80])
    co2_lights= float(in_fields[81])
    co2_renew_gen= float(in_fields[82])
    co2_renew_used= float(in_fields[83])
    for i in range(0,7,1):
        fab_area[i] = float(in_fields[84 + i])
    for i in range(0,7,1):
        fab_uvalue[i] = float(in_fields[91 + i])


# *****************************************************************************************
# alter the values according to the input values
# *****************************************************************************************
    if (intemp==""):
        internal_temp_set = 21
    else:
        internal_temp_set = intemp
#echo internal_temp_set.","

#code format TM_1_MW_7_MF_4_MR_6_MO_4GR_3_SD_0_TH_0_HS_3_IR_1_VT_0_ST_0_PV_0_TP_1_LA_2_OR_0_RT_5_SR_1_OF_0_OB_0_OL_1_OR_0_EL_10_EA_1_EC_1_OV_0_OD_0_HA_0_SH_0_RS_2
	
# thermal mass TM
    if (int(line_vars[1])==0):
# case 0:
        constr_type = 0
        heat_capacity = 100

    if (int(line_vars[1])==1):
# case 1:
        constr_type = 1
        heat_capacity = 250

    if (int(line_vars[1])==2):
# case 2:
        constr_type = 1
        heat_capacity = 450
	
# wall Uvalue MW
    if (int(line_vars[3])>len(WallUValue_array)-1):
        line_vars[3]=len(WallUValue_array)-1
    fab_uvalue[4]= WallUValue_array[int(line_vars[3])]
# floor Uvalue MF
    if (int(line_vars[5])>len(FloorUValue_array)-1):
        line_vars[5]=len(FloorUValue_array)-1
    fab_uvalue[2]= FloorUValue_array[int(line_vars[5])]
# roof Uvalue MR
    if (int(line_vars[7])>len(RoofUValue_array)-1):
        line_vars[7]=len(RoofUValue_array)-1
    fab_uvalue[6]= RoofUValue_array[int(line_vars[7])]

# window Uvalue MO
    if (int(line_vars[9])>len(WindowUValue_array)-1):
        line_vars[9]=len(WindowUValue_array)-1
    fab_uvalue[1]= WindowUValue_array[int(line_vars[9])]

    fab_uvalue[0]=fab_uvalue[1]
	
# set the g value according to the glazing type
    temp_gvalue = 0.65
    if (fab_uvalue[1]>3.1):
        temp_gvalue = 0.85
    else:
        if (fab_uvalue[1]>2.0):
            temp_gvalue = 0.76
            for j in range(0,4,1):
                win_g[j] = temp_gvalue
	
# Living area LA
    if (int(line_vars[29])>len(floorarea_array)-1):
        line_vars[29]=len(floorarea_array)-1
    floor_area = floorarea_array[int(line_vars[29])]
    living_area = livingarea_array[int(line_vars[29])]

    total_volume = floor_area *2.5
# surf_ratio SR 
    if (int(line_vars[35])>4):
        line_vars[35]=4

	
# wall area
    if (in_wall_area==""):
        fab_area[4]=  externalwall_array[int(typology_value)*40 + int(line_vars[29])+int(line_vars[35])*8]
    else:
        fab_area[4]= float(in_wall_area)
# party wall area
    fab_area[5]= 0
# floor area
    if (in_floor_area==""):
        fab_area[2] = floorarea_array[int(line_vars[29])]/2
    else:
        fab_area[2]=float(in_floor_area)
# roof area
    fab_area[6] = floorarea_array[int(line_vars[29])]/2
# door area
    fab_area[0] = 4
	
    if (typology_value == 3):
        fab_area[0] = 0
        fab_area[2] = 0
        fab_area[6] = 0
	
	
# glazing ratio GR
    total_wall_area = fab_area[4]
    if (int(line_vars[11])>len(Glazingratio_array)-1):
        line_vars[11]=len(Glazingratio_array)-1
		
	
    if (in_wall_area==""):
        if (total_wall_area>0):
            fab_area[1] = 0
            for k in range(0,4,1):
                win_area[k] = win_area[k]/100 * total_wall_area * Glazingratio_array[int(line_vars[11])]
                fab_area[1] = fab_area[1] + win_area[k]
            fab_area[4] = total_wall_area - fab_area[1]
    else:
         fab_area[1] = float(in_win_north)+float(in_win_east)+float(in_win_south)+float(in_win_west)
         win_area[0] = float(in_win_north)
         win_area[1] = float(in_win_east)
         win_area[2] = float(in_win_south)
         win_area[3] = float(in_win_west)
         win_orient[0] = 0
         win_orient[1] = 90
         win_orient[2] = 180
         win_orient[3] = 270
         
# store the fabric areas
    for k in range(0,7,1):
        out_fab_area[k] = fab_area[k]
# store the window areas
    for k in range(0,4,1):
        out_win_area[k] = win_area[k]
	
# shading device SD
    if (int(line_vars[13])>len(blinds_array)-1):
        line_vars[13]=len(blinds_array)-1
    blind = blinds_array[int(line_vars[13])]
	
	
# thermal bridges TH
    if (int(line_vars[15])>len(thermalbridge_array)-1):
        line_vars[15]=len(thermalbridge_array)-1
    thermal_bridge= thermalbridge_array[int(line_vars[15])]
	
	
# heating_age HA 
    if (int(line_vars[55])==0):
# case 0:
# very good
        heating_age = 0

    if (int(line_vars[55])==1):
# case 1:
# average
        heating_age = 2
    if (int(line_vars[55])==2):
# case 2:
# very poor
        heating_age = 4

    if (int(line_vars[55])==3):
# case 3:
# good
        heating_age = 1

    if (int(line_vars[55])==4):
# case 4:
# poor
        heating_age = 3
	
# heating system HS
    if (int(line_vars[17])>len(system_efficiency_array)-1):
        line_vars[17]=len(system_efficiency_array)-1
    eff_main1 = system_efficiency_array[int(line_vars[17])+ heating_age * 6]
    eff_water = water_efficiency_array[int(line_vars[17])+ heating_age * 6]
    fuel_main1 =system_fuel_array[int(line_vars[17])+ heating_age * 6]
    fuel_water = system_fuel_array[int(line_vars[17])+ heating_age * 6]
    co2_main1 = system_co2_array[int(line_vars[17])]
    co2_water = system_co2_array[int(line_vars[17])]
# heating responsiveness
    responsiveness = responsivness_array[int(line_vars[17]) + heating_age * 6]
# heating controls
    heat_control = heat_control_array[int(line_vars[17]) + heating_age * 6]
# temperature adjust
    temp_adjust  = temp_adjust_array[int(line_vars[17]) + heating_age * 6]
    pump_gains = pumpgains_array[int(line_vars[17])]
    elec_fan_pumps = pumpenergy_array[int(line_vars[17])]
    if (int(line_vars[17])==3):
        standing_charges =106
    else:
        standing_charges = 0
    FF = fuelfactor_array[int(line_vars[17])]
	
# q50 IR
    if (int(line_vars[19])>len(q50_array)-1):
        line_vars[19]=len(q50_array)-1
    q50= q50_array[int(line_vars[19])]
	
# vent type VT
    if (int(line_vars[21])==1):
        exhaust_heatpump=0.5
        vent_type =2
        mvhr_efficency = 0.85
	
# solar thermal ST
    if (int(line_vars[23])>len(solar_thermal_tank_volume_array)-1):
        line_vars[23]=len(solar_thermal_tank_volume_array)-1
# assume a tank thickness
    tank_loss  = 0.0152
    if (int(line_vars[23])>0):
        tank_volume  =solar_thermal_tank_volume_array[int(line_vars[23])]/2
        solar_energy = solar_thermal_energy_array[int(line_vars[23])]
        solar_storage_volume = solar_thermal_tank_volume_array[int(line_vars[23])]/2
        dhw_source = 2
	
# regional solar RS 
    if (int(line_vars[59])>len(PV_locations)-1):
        line_vars[59]=len(PV_locations)-1
# PV
    if (int(line_vars[25])>len(PV_array)-1):
        line_vars[25]=len(PV_array)-1
    elec_renew_gen  = PV_array[int(line_vars[25])] * PV_locations[int(line_vars[59])]*0.1
    fuel_renew_gen = 11.46
    co2_renew_gen = 0.529
	
#code format continues TP_0_LA_0_OR_0_RT_0_SR_0_OF_0_OB_0_OL_0_OR_0_EL_0_EA_0_EC_0_OV_0_OD_0_HA_0_SH_0
	
# typology TP
    if  (typology_value==0):
# case 0:
        window_opening = 2
    if  (typology_value==1):
# case 1:
        window_opening = 2
    if  (typology_value==2):
# case 2:
        window_opening = 2
    if  (typology_value==3):
# case 3:
        window_opening = 1
	
# Orientation OR
	
    if (int(line_vars[31])==0):
# case 0:
        win_orient[0] = 0
        win_orient[1] = 90
        win_orient[2] = 180
        win_orient[3] = 270
    if (int(line_vars[31])==1):
# case 1:
        win_orient[0] = 315
        win_orient[1] = 45
        win_orient[2] = 135
        win_orient[3] = 225
    if (int(line_vars[31])==2):
# case 2:
        win_orient[0] = 270
        win_orient[1] = 0
        win_orient[2] = 90
        win_orient[3] = 180
    if (int(line_vars[31])==3):
# case 3:
        win_orient[0] = 225
        win_orient[1] = 315
        win_orient[2] = 45
        win_orient[3] = 135
    if (int(line_vars[31])==4):
# case 4:
        win_orient[0] = 180
        win_orient[1] = 270
        win_orient[2] = 0
        win_orient[3] = 90
    if (int(line_vars[31])==5):
# case 5:
        win_orient[0] = 135
        win_orient[1] = 225
        win_orient[2] = 315
        win_orient[3] = 45
    if (int(line_vars[31])==6):
# case 6:
        win_orient[0] = 90
        win_orient[1] = 180
        win_orient[2] = 270
        win_orient[3] = 0
    if (int(line_vars[31])==7):
# case 7:
        win_orient[0] = 45
        win_orient[1] = 135
        win_orient[2] = 225
        win_orient[3] = 315
    for k in range(0,4,1):
        out_win_orient[k] = win_orient[k]

# region for overheating RT
    if (int(line_vars[33])>len(region_lat)-1):
        line_vars[33]=len(region_lat)-1
    region_value = int(line_vars[33])
	
# obstacle_front OF 
    if (int(line_vars[37])>0):
        win_access[2]= 0.3
# obstacle_back OB 
    if (int(line_vars[39])>0):
        win_access[0]= 0.3
# obstacle_side1 OL 
    if (int(line_vars[41])>0):
        win_access[1]= 0.3
# obstacle_side2 OR 
    if (int(line_vars[43])>0):
        win_access[3]= 0.3
# eff_lights EL 
    if (int(line_vars[45])>0):
        eff_light = int(line_vars[45])
# eff_appliances EA 
    if (int(line_vars[47])>0):
        eff_app = int(line_vars[47])
# eff_cooking EC 
    if (int(line_vars[49])>0):
        eff_cook = int(line_vars[49])
# overhang OV 
    overhang_type = int(line_vars[51])*7

# overhang_depth OD 
    overhang_type = overhang_type +int(line_vars[53])
	
# second_heating SH 
    if (int(line_vars[57])>len(second_eff_array)-1):
        line_vars[57]=len(second_eff_array)-1
    if (int(line_vars[57])>0):
        second_fraction = 0.10
        eff_second = second_eff_array[int(line_vars[57])]
        fuel_second = second_fuel_array[int(line_vars[57])]
        co2_second = second_co2_array[int(line_vars[57])]
	
	
# *****************************************************************************************
# Do the calculation 3 times DER, FEE and TER
# *****************************************************************************************
    for k in range(0,3,1):
        heating = 0
        annual_sys_main1 = 0
        annual_sys_main2 = 0
        annual_sys_second = 0
        annual_sys_water = 0
# fee building
        if (k==1):
# natural ventialtion
            vent_type=0
# extract fans
            if (floor_area<70):
                num_fan = 2
            else:
                if (floor_area<100):
                    num_fan = 3
                else:
                    num_fan = 4
# 100% low energy lights
            eff_light = 10
# heating responsiveness
            responsiveness = 1
# heating controls
            heat_control = 2
# temperature adjust
            temp_adjust =0
# pump gains
            pump_gains = 0
# efficency
            eff_cook==1
            eff_app==1
# set the values for the TER
        if (k==2):
# wall Uvalue
            fab_uvalue[4]= 0.35
# party wall Uvalue
            fab_uvalue[5]= 0
# floor Uvalue
            fab_uvalue[2]= 0.25
# roof Uvalue
            fab_uvalue[6]= 0.16
# window Uvalue
            fab_uvalue[1]= 2.0
# door Uvalue
            fab_uvalue[0]= 2.0
# thermal mass
            heat_capacity = 250

# number of sides sheltered
            num_shelt = 2
# thermal bridging
            thermal_bridge = 0.11
# natural ventialtion
            vent_type=0
# extract fans
            if (floor_area<80):
                num_fan = 2
            else:
                num_fan = 3
# q50
            q50 =10
# windows
            for j in range(0,4,1):
                win_orient[j] = 0
                win_access[j] = 0.77
                win_area[j] = 0
                win_ff[j] = 0.7
                win_g[j] = 0.72
            win_orient[0] = 90
            if ((fab_area[4]+fab_area[1]+fab_area[0])>(floor_area*0.25)):
                win_area[0] = floor_area *.25 - 1.85
                fab_area[4] = fab_area[4]+fab_area[1]+fab_area[0] - win_area[0]-1.85
                fab_area[1] = win_area[0]
                fab_area[0] = 1.85
                if (fab_area[4]<0):
                    fab_area[4]=0
            else:
                fab_area[1]= fab_area[4]+fab_area[1]- 1.85
                win_area[0] = fab_area[1]
                fab_area[4] = 0
                fab_area[0] = 1.85

# 100% low energy lights
            eff_light = 3

# mains gas heating
            eff_main1 = 78.9
            eff_second= 100
            eff_water = 68.8
            fuel_main1 =3.1
            fuel_main2 =0
            fuel_second =11.46
            fuel_water = 3.1
            co2_main1 = 0.194
            co2_main2 = 0
            co2_second = 0.422
            co2_water = 0.194
            co2_lights = 0.422
            co2_pumps = 0.422
            second_fraction = 0.10
            responsiveness = 1
            heat_control = 2
# temperature adjust
            temp_adjust =0
# pump gains
            pump_gains = 10
            elec_fan_pumps = 175
# hot water
            water_target=0
            tank_volume  =150
            solar_energy = 0
            solar_storage_volume = 0
            dhw_source = 2
            tank_loss  = 0.0191
            circuit_loss = 610

            elec_renew_gen =0
            elec_renew_used =0
# efficency
            eff_cook==0
            eff_app==0

# do calcs
        if (num_storey != 0 and total_volume != 0 ):
# add up the chimneys,flues and fans
            ventcalc = (num_chim) * 40
            ventcalc = ventcalc + num_flue * 20
            ventcalc = ventcalc + num_fan * 10
            ventcalc = ventcalc + num_passvent * 10
            ventcalc = ventcalc + num_flueless * 40
            ventcalc = ventcalc / total_volume
# additional infiltration has the been a pressure test
            if (q50 < 0):
                ventcalc = ventcalc + (num_storey - 1) * 0.1
# additional for construction
                if (constr_type == 0):
                    ventcalc = ventcalc + 0.35
                else:
                    ventcalc = ventcalc + 0.25
# additional for floor type
                if (floor_type == 1): 
                    ventcalc = ventcalc + 0.2
                if (floor_type == 2):
                    ventcalc = ventcalc + 0.1
# draught lobby
                if (drau_lobby == 0):
                    ventcalc = ventcalc + 0.05
# window draught stripping
                ventcalc = ventcalc + 0.25 - (0.2 * num_strip / 100)
            else:
# if there has been a pressure test
                ventcalc = ventcalc + q50 / 20
            ventcalc = ventcalc * (1 - (0.075 * num_shelt))
            for i in range(0,12,1):
                Mventcalc[i] = ventcalc * month_windspeed[i] / 4
                if (vent_type==0):
#0 for natural and postive vent, 
                    if (Mventcalc[i] < 1):
                        Mventcalc[i] = 0.5 + (0.5 * Mventcalc[i] * Mventcalc[i])
                if (vent_type==1):
#1 for balanced mech without heat recovery,
                    Mventcalc[i] = Mventcalc[i] + exhaust_heatpump
                if (vent_type==2):
#2 for balanced mech with heat recovery
                    Mventcalc[i] = Mventcalc[i] + exhaust_heatpump * (1 - (mvhr_efficency))
                if (vent_type==3):
#3 for mech without heat recovery,
                    if (Mventcalc[i] < (0.5 * exhaust_heatpump)):
                        Mventcalc[i] = exhaust_heatpump
                    else:
                        Mventcalc[i] = Mventcalc[i] + 0.5 * exhaust_heatpump
            air_change[i] = Mventcalc[i]


# calculate the heat loss and the rest ********************************************************
        if (floor_area > 0):
            fab_loss = fab_uvalue[0] * fab_area[0] + thermal_bridge * fab_area[0]
            fab_loss = fab_loss + (1/(1/fab_uvalue[1]+0.04)) * fab_area[1] + thermal_bridge * fab_area[1]
            fab_loss = fab_loss + fab_uvalue[2] * fab_area[2] + thermal_bridge * fab_area[2]
            fab_loss = fab_loss + fab_uvalue[3] * fab_area[3] + thermal_bridge * fab_area[3]
            fab_loss = fab_loss + fab_uvalue[4] * fab_area[4] + thermal_bridge * fab_area[4]
            fab_loss = fab_loss + fab_uvalue[6] * fab_area[6] + thermal_bridge * fab_area[6]
	
            for i in range(0,12,1):
                HLP[i] = (fab_loss + 0.33 * Mventcalc[i] * total_volume) / floor_area
# calculate the hot water usage ********************************************************
            if (floor_area > 13.9):
                N = 1 + 1.76 * (1 - math.exp(-0.000349 * pow((floor_area - 13.9), 2))) + 0.0013 * (floor_area - 13.9)
            else:
                N = 1
            number_people = N
            if (water_target == 1):
                dhw_volume = ((25 * N) + 36) * 0.95
            else:
                dhw_volume = ((25 * N) + 36)
# do the monthly calcs ---------------------------------
            for i in range(0,12,1):
# box 44
                dhwcalc = 0
                DHW_usage[i] = hot_water_factor[i] * dhw_volume
# box 45
                dhw_eng_cont = 4.19 * DHW_usage[i] * number_of_days[i] * drawoff_temp_rise[i] / 3600
# dhw source
# 0 is instantaneous
# 1 is combi
# 2 is a tank electric immersion

# 3 is a cylinder indirect
# 4 is storage combi boiler primary store
# 5 is storage combi boiler secondary store
# 6 is instantaneous combi boiler with close coupled external store
# 7 is a hot water only thermal store
# 8 is integrated thermal store and gas fired CPSU
# 9 is electric CPSU 
# 10 is a plate heat exchanger community heating
                if (dhw_source > 1 and k!=1):
#it's a tank
                    dhw_dist_loss = 0.15 * dhw_eng_cont
# box 56
                    dhwcalc = tank_volume * (pow(120/tank_volume,1/3))*tank_loss * 0.54 * number_of_days[i]
# box 57
                    dhw_cylinder_loss = dhwcalc * (tank_volume - solar_storage_volume) / tank_volume
# box 59
                    dhwcalc = dhw_cylinder_loss + circuit_loss / 365 * number_of_days[i]
# box 61
                    dhwcalc = dhwcalc + combi_loss
				
                if (dhw_source > 1 and k!=1):
                    dhwcalc = dhw_eng_cont + dhwcalc
                else:
                    dhwcalc = 0.85 * dhw_eng_cont + dhwcalc
                    dhwcalc = dhwcalc - solar_energy

                if (dhwcalc < 0):
                    dhwcalc = 0
                DHW_heat_out[i] = dhwcalc
# need to do box 65
                dhw_heat_gain = 0.25 *(0.85* dhw_eng_cont + combi_loss)
                dhw_heat_gain  = dhw_heat_gain + 0.8 * (dhw_dist_loss + dhw_cylinder_loss + circuit_loss / 365 * number_of_days[i])
                DHW_gains[i] = dhw_heat_gain
# end the monthly calcs ---------------------------------

# calculate the internal gains ********************************************************
            AppElec_calc = 0
            light_c1_c2 = 1 - 0.5 * eff_light/10
            light_c2_calc  = 0
            temp_GL = 0
            temp_ZL = 1
            for j in range(0,4,1):
                if (win_g[j]> 0.85):
                    temp_GL = 0.9
                else:
                    if (win_g[j]> 0.7):
                        temp_GL = 0.8
                    else:
                        temp_GL = 0.7

                if (win_access[j]<0.5):
                    temp_ZL = 0.5
                else:
                    if (win_access[j]< 0.7):
                        temp_ZL = 0.67
                    else:
                        if (win_access[j]< 0.8):
                            temp_ZL = 0.83
                        else:
                            temp_ZL = 1.0

                light_c2_calc = light_c2_calc + 0.9 * win_area[j] * temp_GL * win_ff[j] * temp_ZL

			
            light_c2_calc = light_c2_calc / floor_area
            if (light_c2_calc>0.095):
                light_c2_calc = 0.96
            else:
                light_c2_calc  = 52.2 * pow(light_c2_calc,2) - 9.94 * light_c2_calc + 1.433
            light_c1_c2 = light_c1_c2 * light_c2_calc
            light_energy = 0
            for i in range(0,12,1):
                gains_app = 207.8 * pow(floor_area * N, 0.4714)
                gains_app = gains_app * (1 + 0.157 * math.cos(2 * math.pi * (i + 1 - 1.78) / 12)) * number_of_days[i] / 365
                gains_lighting = 59.73 * pow(floor_area * N, 0.4714) * light_c1_c2
                gains_lighting = gains_lighting * (1 + 0.5 * math.cos(2 * math.pi * (i + 1 - 0.2) / 12)) * number_of_days[i] / 365
                light_energy = light_energy + gains_lighting

                if (new_dwelling == 1 or k==2):
                    gains_met = 50 * N
                else:
                    gains_met = 60 * N

                if  (eff_app==0 and k!=2):
                    gains_app = gains_app * 1000 / (24 * number_of_days[i])
                else:
                    gains_app = 0.67 * gains_app * 1000 / (24 * number_of_days[i])

                if  (eff_cook==0 and k!=2):
                    gains_cooking = 35 + 7 * N
                else:
                    gains_cooking = 23 + 5 * N

                if  (eff_light==0):
                    gains_lighting = gains_lighting * 0.85 * 1000 / (24 * number_of_days[i])
                else:
                    gains_lighting = 0.4 * gains_lighting * 0.85 * 1000 / (24 * number_of_days[i])

                AppElec_calc = AppElec_calc + (gains_lighting + gains_cooking + gains_app + pump_gains) *( 24 / 1000 * number_of_days[i])
                other_losses = -40 * N
                int_gains = 1000 * DHW_gains[i] / (24 * number_of_days[i])
                int_gains = int_gains + gains_met + gains_lighting + gains_app + gains_cooking + pump_gains + other_losses
                summer_int_gains[i] = gains_met + gains_lighting + gains_app + gains_cooking + other_losses
                total_int_gains[i] = int_gains

# calculate the monthly gains ********************************************************
            for i in range(0,12,1):
# calculate the solar gains ********************************************************
                solar_gains[i] = 0
                for j in range(0,4,1):
                    solar_coeff_a = 0.702 - 0.0119 * (53.4 - solar_declination[i]) + 0.000204 * pow((53.4 - solar_declination[i]),2)
                    solar_coeff_b = -0.107 + 0.0081 * (53.4 - solar_declination[i]) - 0.000218 * pow((53.4 - solar_declination[i]),2)
                    solar_coeff_c = 0.117 - 0.0098 * (53.4 - solar_declination[i]) + 0.000143 * pow((53.4 - solar_declination[i]),2)

                    Rhtov = solar_coeff_a + solar_coeff_b * math.cos((math.pi * win_orient[j] / 180)) + solar_coeff_c * math.cos((2 * math.pi * win_orient[j] / 180))
                # seems okay up to this point
                    solar_gains[i] = solar_gains[i] + (Rhtov * solar_radiaion[i] * win_access[j] * win_area[j] * win_ff[j] * win_g[j] * 0.9)
                total_gains[i] = total_int_gains[i] + solar_gains[i]
                                
# calculate the internal temperature ********************************************************
                heat_off[0] = 7
                heat_off[1] = 8
                heat_off[2] = 0
                heat_off[3] = 8

# calculate the utilisation factor for living space ********************************************************
                time_constant = heat_capacity / (3.6 * HLP[i])
                util_a = 1 + (time_constant / 15)
                util_y = total_gains[i] / (HLP[i] * floor_area * (internal_temp_set - external_temp[i]))
                if (util_y <= 0):
                    util_factor = 1
                else: 
                    if (util_y == 1):
                        util_factor = util_a / (util_a + 1)
                    else:
                        util_factor = (1 - pow(util_y, util_a)) / (1 - pow(util_y , (util_a + 1)))
# calculate the temperature for living space********************************************************
                for j in range(0,4,1):
                    temp_noheat = (1 - responsiveness) * (internal_temp_set - 2) + responsiveness * (external_temp[i] + util_factor * total_gains[i] / (HLP[i] * floor_area))
                    if (heat_off[j] > (4 + 0.25 * time_constant)):
                        temp_u[j] = (internal_temp_set - temp_noheat) * (heat_off[j] - 0.5 * (4 + 0.25 * time_constant)) / 24
                    else:
                        temp_u[j] = (0.5 * pow(heat_off[j] ,2)) * (internal_temp_set - temp_noheat) / (24 * (4 + 0.25 * time_constant))
                temp_t1[i] = (5 * (internal_temp_set - temp_u[0] - temp_u[1]) + 2 * (internal_temp_set - temp_u[2] - temp_u[3])) / 7

                    # calculate the temperature for rest of building********************************************************
                if (heat_control == 1):
                    temp_rest = internal_temp_set - 0.5 * HLP[i]
                else:
                    temp_rest = internal_temp_set - HLP[i] + 0.085 * pow(HLP[i] , 2)
                if (heat_control == 3):
                    heat_off[0] = 9
                    heat_off[1] = 8
                    heat_off[2] = 9
                    heat_off[3] = 8
                util_y = total_gains[i] / (HLP[i] * floor_area * (temp_rest - external_temp[i]))
                if (util_y <= 0):
                    util_factor = 1
                else:
                    if (util_y == 1):
                        util_factor = util_a / (util_a + 1)
                    else:
                        util_factor = (1 - pow(util_y, util_a)) / (1 - pow(util_y , (util_a + 1)))
                for j in range(0,4,1):
                    temp_noheat = (1 - responsiveness) * (temp_rest - 2) + responsiveness * (external_temp[i] + util_factor * total_gains[i] / (HLP[i] * floor_area))
                    if (heat_off[j] > (4 + 0.25 * time_constant)):
                        temp_u[j] = (internal_temp_set - temp_noheat) * (heat_off[j] - 0.5 * (4 + 0.25 * time_constant)) / 24
                    else:
                        temp_u[j] = (0.5 * pow(heat_off[j], 2)) * (temp_rest - temp_noheat) / (24 * (4 + 0.25 * time_constant))
                temp_t2[i] = (5 * (temp_rest - temp_u[0] - temp_u[1]) + 2 * (temp_rest - temp_u[2] - temp_u[3])) / 7
                internal_temp[i] = living_area / floor_area * temp_t1[i] + (1 - (living_area / floor_area)) * temp_t2[i]
                internal_temp[i] = internal_temp[i] + temp_adjust

# calculate the utilisation factor for rest of building ********************************************************
		 
# calculate the utilisation factor for adjusted temperature ********************************************************
                util_y = total_gains[i] / (HLP[i] * floor_area * (internal_temp[i] - external_temp[i]))
                if (util_y <= 0):
                    util_factor = 1
                else: 
                    if (util_y == 1):
                        util_factor = util_a / (util_a + 1)
                    else:
                        util_factor = (1 - pow(util_y, util_a)) / (1 - pow(util_y ,(util_a + 1)))
# calculate the  heating requirement for just the heating season ********************************************************
                heat_require[i] = HLP[i] * floor_area * (internal_temp[i] - external_temp[i])
                heat_require[i] = 0.024 * (heat_require[i] - util_factor * total_gains[i]) * number_of_days[i]

                if (i >= 5 and i <= 8):
                    heat_require[i] = 0
                heating  = heating + heat_require[i]
# calculate the space heating fuel required ********************************************************
                if (eff_main1 > 0):
                    heat_sys_main1[i] = heat_require[i] * (1 - main2_fraction-second_fraction) * 100 / eff_main1
                if (eff_main2 > 0):
                    heat_sys_main2[i] = heat_require[i] * main2_fraction * 100 / eff_main2
                if (eff_second > 0):
                    heat_sys_second[i] = heat_require[i] * second_fraction * 100 / eff_second
                if (eff_water > 0):
                    temp_eff_water =  (heat_require[i] * (1 - main2_fraction-second_fraction))+ DHW_heat_out[i]
                    if (temp_eff_water>0): 
                        temp_eff_water =  temp_eff_water /((heat_require[i] * (1 - main2_fraction-second_fraction))/eff_main1 + (DHW_heat_out[i]/ eff_water))
                        if (temp_eff_water>0): 
                            heat_sys_water[i] = DHW_heat_out[i] * 100 / temp_eff_water
                        else:
                            heat_sys_water[i]=0
                    else:
                        heat_sys_water[i]=0
                annual_sys_main1 = annual_sys_main1 + heat_sys_main1[i]
                annual_sys_main2 = annual_sys_main2 + heat_sys_main2[i]
                annual_sys_second = annual_sys_second + heat_sys_second[i]
                annual_sys_water = annual_sys_water + heat_sys_water[i]
	
# end of gains month loop
# calculate the total cost and SAP ********************************************************
            tot_cost = annual_sys_main1 * fuel_main1
            tot_cost = tot_cost + annual_sys_main2 * fuel_main2
            tot_cost = tot_cost + annual_sys_second * fuel_second
            tot_cost = tot_cost + annual_sys_water * fuel_water
            tot_cost = tot_cost + elec_fan_pumps * fuel_pumps
            tot_cost = tot_cost + light_energy * fuel_lights
            tot_cost = tot_cost - elec_renew_gen * fuel_renew_gen
            tot_cost = tot_cost + elec_renew_used * fuel_renew_used
            tot_cost = tot_cost / 100
            tot_cost = tot_cost + standing_charges
            tot_co2 = annual_sys_main1 * co2_main1
            tot_co2 = tot_co2 + annual_sys_main2 * co2_main2
            tot_co2 = tot_co2 + annual_sys_second * co2_second
            tot_co2 = tot_co2 + annual_sys_water * co2_water
            tot_co2 = tot_co2 + elec_fan_pumps * co2_pumps
            tot_co2 = tot_co2 + light_energy * co2_lights
            tot_co2 = tot_co2 - elec_renew_gen * co2_renew_gen
            tot_co2 = tot_co2 + elec_renew_used * co2_renew_used
			
# ---------------------------- in k loop with floor area ok 3 indents 
            if (k==0):
# if the first time through this is the building
                AppElec_total = AppElec_calc
                total_heating_out = annual_sys_main1 + annual_sys_main2 + annual_sys_second + annual_sys_water
                total_heating_second = annual_sys_second
                total_water_heating_out = annual_sys_water
# add the solar pump
                if (solar_energy >0):
                    AppElec_total  = AppElec_total +75
# add the mvhr
                if (vent_type ==2):
                    AppElec_total  = AppElec_total + 0.4 * 2.44 * mvhr_efficency * total_volume

                PV_out = elec_renew_gen
                DER = tot_co2 / floor_area
                ecf = tot_cost * 0.47 / (floor_area + 45)
                if (ecf >= 3.5):
                    sap = 117 - 121 * math.log10(ecf)
                else:
                    sap = 100 - 13.95 * ecf
# calculate the overheating
                for i in range(5,8,1):
                    summer_solar_gains = 0
# calculate solar gains for all windows
                    for j in range(0,4,1):
                        solar_coeff_a = 0.702 - 0.0119 * (region_lat[region_value] - solar_declination[i]) + 0.000204 * pow((region_lat[region_value] - solar_declination[i]),2)
                        solar_coeff_b = -0.107 + 0.0081 * (region_lat[region_value] - solar_declination[i]) - 0.000218 * pow((region_lat[region_value] - solar_declination[i]),2)
                        solar_coeff_c = 0.117 - 0.0098 * (region_lat[region_value] - solar_declination[i]) + 0.000143 * pow((region_lat[region_value] - solar_declination[i]),2)

                        Rhtov = solar_coeff_a + solar_coeff_b * math.cos((math.pi * win_orient[j] / 180)) + solar_coeff_c * math.cos((2 * math.pi * win_orient[j] / 180))
# seems okay up to this point
                        if (win_access[j]<0.5):
                            temp_ZL = 0.5
                        else:
                            if (win_access[j]< 0.7):
                                temp_ZL = 0.7
                            else:
                                if (win_access[j]< 0.8):
                                    temp_ZL = 0.9
                                else:
                                    temp_ZL = 1.0
                            if (win_orient[j]<45):
                                Zsummer = blind * (temp_ZL + overhang_N_array[overhang_type] - 1)
                            else:
                                if (win_orient[j]<90):
                                    Zsummer = blind * (temp_ZL + overhang_NE_array[overhang_type] - 1)
                                else:
                                    if (win_orient[j]<135):
                                        Zsummer = blind * (temp_ZL + overhang_E_array[overhang_type] - 1)
                                    else:
                                            if (win_orient[j]<180):
                                                Zsummer = blind * (temp_ZL + overhang_SE_array[overhang_type] - 1)
                                            else:
                                                if (win_orient[j]<225):
                                                    Zsummer = blind * (temp_ZL + overhang_S_array[overhang_type] - 1)
                                                else:
                                                    if (win_orient[j]<270):
                                                        Zsummer = blind * (temp_ZL + overhang_SE_array[overhang_type] - 1)
                                                    else:
                                                        if (win_orient[j]<315):
                                                            Zsummer = blind * (temp_ZL + overhang_E_array[overhang_type] - 1)
                                                        else:
                                                            Zsummer = blind * (temp_ZL + overhang_NE_array[overhang_type] - 1)
                        summer_solar_gains = summer_solar_gains + (Rhtov * region_summer_solar[3 * (region_value-1)+ (i-5)] * Zsummer * win_area[j] * win_ff[j] * win_g[j] * 0.9)
# calculate for all window conditons
                    for j in range(0,4,1):
                        summer_gains_ratio = (summer_solar_gains + summer_int_gains[i])/(fab_loss + (0.33 * total_volume * effective_ach_array[window_opening*4+j]))
# trace(i+" "+summer_solar_gains+" "+ summer_int_gains[i]+" "+summer_gains_ratio)
                        if (heat_capacity< 285):
                            Tthreshold = region_summer_temp[3 * (region_value-1)+ (i-5)] + summer_gains_ratio + (2.0 - 0.007 * heat_capacity)
                        else:
                            Tthreshold = region_summer_temp[3 * (region_value-1)+ (i-5)] + summer_gains_ratio
                        if (Tthreshold< 20.5):
                            OH[i-5+j*3] = 1
                        else:
                            if (Tthreshold< 22.0):
                                OH[i-5+j*3] = 2
                            else:
                                if (Tthreshold< 23.5):
                                    OH[i-5+j*3] = 3
                                else:
                                    OH[i-5+j*3] = 4
            else:
                if (k==1):
                # if the second time through this is the fee building
                    heating_out = heating / floor_area
                else:
                # if the third time through this is the notional building
                    TER_Calc = (tot_co2 - light_energy * co2_lights) * FF * EFAh
                    TER_Calc = TER_Calc+ (light_energy * co2_lights) * EFAl
                    TER = TER_Calc * (1 - 0.2)*(1 - 0.25)/ floor_area

# build the output
    return_string = return_string + str(round(DER,1))
    return_string = return_string + ","+ str(round(TER,1))
    return_string = return_string + ","+ str(round(sap,1))
    return_string = return_string + ","+ str(round(heating_out,1))
    return_string = return_string + ","+ str(round(PV_out,1))
    return_string = return_string + ","+ str(round(AppElec_total,0))
    return_string = return_string + ","+ str(OH[9])
    return_string = return_string + ","+ str(OH[10])
    return_string = return_string + ","+ str(OH[11])
    return_string = return_string + ","+ str(OH[6])
    return_string = return_string + ","+ str(OH[7])
    return_string = return_string + ","+ str(OH[8])
    return_string = return_string + ","+ str(OH[3])
    return_string = return_string + ","+ str(OH[4])
    return_string = return_string + ","+ str(OH[5])
    return_string = return_string + ","+ str(OH[0])
    return_string = return_string + ","+ str(OH[1])
    return_string = return_string + ","+ str(OH[2])
    return_string = return_string + ","+ str(total_heating_out)
    return_string = return_string + ","+ str(total_water_heating_out)
    return_string = return_string + ","+ str(floor_area)
    return_string = return_string + ","+ str(total_heating_second)
    if (dimension_out!=""):
        for i in range(0,4,1):
            return_string = return_string + ","+ str(out_win_area[i])
            return_string = return_string + ","+ str(out_win_orient[i])
        for i in range(0,7,1):
            return_string = return_string + ","+ str(out_fab_area[i])
    print("exit SAP result", return_string)
    return return_string

#tempcode="TM_1_MW_10_MF_11_MR_7_MO_7_GR_3_SD_0_TH_1_HS_5_IR_3_VT_0_ST_0_PV_8_TP_0_LA_6_OR_0_RT_5_SR_1_OF_0_OB_0_OL_0_OR_0_EL_10_EA_0_EC_0_OV_0_OD_0_HA_0_SH_0_RS_3"

#sap_result(instring,intemp,replace_what,replace_with,dimension_out,in_wall_area,in_floor_area,in_win_north,in_win_east,in_win_south,in_win_west):
#result = sap_result(tempcode,"","","","","15","50","2","2","2","2")
#print (result)
