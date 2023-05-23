#!/usr/bin/env python
# coding: utf-8
# In[5]:
# TO RUN THIS:
# 1- GO TO COMMAND LINE FOR RUN THE APP
# 2- streamlit run SAP2009_ST.py

#Importing streamlit and others 
import streamlit as st

#Python Imaging Library is a free and open-source additional library for the Python programming language
from PIL import Image

#Topologicpy Python library for conceptual 3D model 
import topologicpy
from topologicpy.Cell import Cell
from topologicpy.Plotly import Plotly

#Python code developed by Dr Simon Lannon, 2013. It will be used for evaluating the energy performance of the project (SAP analysis).
import sap_engine_2009
import math

# Python libraries considered for presenting SAP analysis results in charts. After some test it was decided to develop this section in a further study and for this stage using an image for showing SAP rating representation.
#import altair as alt
#import pandas as pd
#import matplotlib as mpl

#defining wide layout for Streamlit

st.set_page_config(
    page_title="Energy performance Evaluation for dwellings, based on SST2009",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Natalia Diaz is the author of this app. For more information send an email to diazdiazna@cardiff.ac.uk"})

#Defining elements to organise dashboard layout
#header = st.container()
#energy_performance = st.container()
#geometric_features = st.container()
colA, colB, colC, colD = st.columns(4)
col1, col2 = st.columns([3,1])

#Images to explain obstacles codification
obs_image1 = Image.open('Obs_Image.jpg')
obs_image2 = Image.open('Obs_Image_Sides.jpg')

#Image SAP rating
epc_image = Image.open('EPC_Chart.jpg')
surf_ratio = Image.open("Surface_Ratio.jpg")

#Image Location
loc_UK_map = Image.open("Location_maps.jpg")


#if statement for defining the 
#correspondednt letter according to SAP result
def SAP_letter(za):
    if 0 <= round(za) < 21:
        return "G"
    elif 21 <= round(za) < 39:
        return "F"
    elif 39 <= round(za) < 55:
        return "E"
    elif 55 <= round(za) < 69:
        return "D"
    elif 69 <= round(za) < 81:
        return "C"
    elif 81 <= round(za) < 91:
        return "B"
    elif 91 <= round(za):
        return "A"
    
#defining arrays according to the logic provided in sap_engine_2009 file

#Geometric input (tab 1)
floor_area_array =[50,60,70,80,90,100,110,120]
living_area_array =[22.5,18,17.5,18.4,18.9,21,20.9,19.2]
surface_ratio_array = ["Compact = 1:1","Rectangular = 1:1.6","Narrow = 1:2.7", "Wide = 1.6:1", "Extra-Wide= 2.7:1"] 

#Orientation input (tab 2)
orientation_array = ["North","North West","West","South West","South","South East","East","Nort East"]

#location input (tab3)
location_array = ["1. Thames",
        "2. South East England",
        "3. Southern England",
        "4. South West England",
        "5. Severn Wales/Severn England", 
        "6. Midlands",
        "7. West Pennines Wales/West Pennines England", 
        "8. North West England/South West Scotland", 
        "9. Borders Scotland/Borders England", 
        "10. North East England", 
        "11. East Pennines", 
        "12. East Anglia", 
        "13. Wales", 
        "14. West Scotland", 
        "15. North East Scotland", 
        "16. North East Scotland", 
        "17. Highland", 
        "18. Western Isles", 
        "19. Orkney", 
        "20. Shetland",
        "21. Northern Ireland"]
region_solar_array = ["800-850"," 850-900", "900-950", "950-1000", "1000-1050", "1050-1100", "1100-1150"]

#Fabric input(tab 4): 
thermal_mass_array = ["Low","Medium","High"]
wall_UValue_array =[2.1,2.0,1.7,1.0,0.6,0.45,
                    0.35,0.3,0.25,0.2,0.15,0.10]
floor_UValue_array =[2.0,0.6,0.45,0.3,0.25,0.2,
                     0.15,0.14,0.13,0.12,0.11,0.10]
roof_UValue_array =[2.0,1.5,1.,0.6,0.35,
                    0.25,0.2,0.13,0.1]
window_UValue_array =[4.8,3.1,3,2.2,2,1.8,
                      1.6,1.4,1.2,1,0.8]
glazing_ratio_array =["10%","15%","20%","25%",
                      "30%","35%","40%","45%","50%"]
shading_dev_array = [0.24, 0.27, 0.60, 0.65, 0.70, 
                     0.80, 0.85, 0.88, 0.90, "NONE"]
thermal_bridge_array =["0.15 or NO INFO",0.08,0.04]

#System input(tab 5):
PV_array =[0,3.5,7,10.5,14,17.5,21,24.5,28]
heating_system_array = ["Electric","Solid Fuel","Oil","Nat. Gas","Heat Pump","Biomass"]
q50_array =["Poor/N.A.","Normal Practice","Good Practice","Best Practice"]
ventilation_array = ["Natural Ventilation", "MVHR"]
solar_thermal_array = ["NONE", "1.00", "2.00", "3.00", "4.00", "5.00", "6.00"]
PV_panel_array = ["NONE", "0.50", "1.00", "1.50","2.00", "2.50", "3.00", "3.50", "4.00"]
lighting_array=[0,10,20,30,40,50,60,70,80,90,100]


#Defining tabs with input to be included in the sidebar
with st.sidebar:
    tab1,tab2,tab3, tab4, tab5 = st.tabs(["1.Geometric","2.Orientation", "3.Location","4.Fabric","5.Systems"])
    tab1.subheader('Project input: Geometric Information')
    tab2.subheader('Project input: Orientation')
    tab3.subheader('Project input: Location Information')
    tab4.subheader('Project input: Fabric specification')
    tab5.subheader('Project input: Systems specification ')

    #TAB1: Defining building geometric input(Floor area, surface ratio, and orientation).
    floor_area_slider = tab1.select_slider("Floor Area(m2)",options = floor_area_array, value=floor_area_array[2])
    tab1.markdown("Total floor area should be mesured as the sum of the actual floor area of each floor. Unheated spaces clearly divided from the dwelling should not be included(SAP 2009 version 9.90 - March 2010. Note: Living area is calculated in relation to total floor area.")
    surface_ratio_slider = tab1.select_slider("Surface Ratio", options = surface_ratio_array)
    surf_ratio_image = tab1.image(surf_ratio) 
    surf_ratio_text = tab1.caption("Image Plan/Footprint Ratio (Crobu et al. 2013)")
    tab1.markdown("Surface ratio relates to the plan form of the building, either compact (square), rectangular or narrow. This should be apparent from a visual check of the exterior of teh building or from plans.")
    
    #TAB2: Defining Orientation and obstables input
    #Obstacles: Expllaining the logic of obastables and checkbox for indicate facades with the three condicions
    orientation_slider = tab2.select_slider("Orientation: Select the orientation of the most glazed facade of your building:", options = orientation_array, value=orientation_array[4])
    obs_text1 = tab2.subheader("Shelter Sides and Obstacles (Overshading):")
    obs_text2 = tab2.text("A side should be considered if all the following apply:")
    obs_diag1 = tab2.image(obs_image1)
    obs_diag1_text = tab2.caption("Image shelter sides and obstacles(Crobu et al. 2013)")
    obs_diag2 = tab2.image(obs_image2)
    obs_diag2_text = tab2.caption("Image: Facades designation (based on Crobu et al. 2013)")
    obs_text3 = tab2.markdown("Click on the options below to identify the facades of your building where all the three conditions apply:")
    obs_OF = tab2.checkbox("Main glazed facade")
    obs_OL = tab2.checkbox("Side 1")
    obs_OR = tab2.checkbox("Side 2")
    obs_OB = tab2.checkbox("Side 3")
    
    #TAB3: Defining location input
    tab3.markdown("Location is used for calculating cooling requirements and to estimate solar thermal output and the electricity produced by PV panel (if installed). Select the solar irradiation band in your region. Annual solar irradiation will be usde in the calculation of PV panel outputs.") 
    location_selectbox= tab3.selectbox("Location",options = location_array, index=4)

    region_solar_slider = tab3.select_slider("Region Solar", options = region_solar_array, value= region_solar_array[3])
    map = tab3.image(loc_UK_map, caption="Map of UK's climatic regions used in SAP2009 and averaga sum of horizontal solar radiation in KWh/m2/y (Based on Crobu et al. 2013)")
  

    #TAB4: Defining building fabric input: according 
    # to information required in sap_engine_2009.py.
    thermal_mass_slider = tab4.select_slider("Thermal mass", 
                                             options=(thermal_mass_array), 
                                             value=thermal_mass_array[1])
    wall_UValue_slider = tab4.select_slider("Walls U-value",
                                            options=(wall_UValue_array), 
                                            value=wall_UValue_array[7])
    floor_UValue_slider = tab4.select_slider("Floor U-value", 
                                             options=(floor_UValue_array), 
                                             value=floor_UValue_array[4])
    roof_UValue_slider = tab4.select_slider("Roof U-value",
                                            options=(roof_UValue_array),
                                            value=roof_UValue_array[6])
    window_UValue_slider = tab4.select_slider("Windows U-value",
                                              options=(window_UValue_array), 
                                              value=window_UValue_array[4])
    glazing_ratio_slider = tab4.select_slider("Glazing Ratio",
                                              options=(glazing_ratio_array), 
                                              value=glazing_ratio_array[3])
    shading_dev_slider = tab4.select_slider("Shading Dev.",
                                            options=(shading_dev_array))
    thermal_bridging_slider = tab4.select_slider("Thermal Bridging",
                                                 options=(thermal_bridge_array))
        
    #TAB5: Defining graphic selection section for systems
    heating_system_slider = tab5.select_slider("Heating System",options=(heating_system_array), value=heating_system_array[3])
    infiltration_rate_slider = tab5.select_slider("Infiltration Rate",options=(q50_array), value=q50_array[1])
    ventilation_slider = tab5.select_slider("Ventilation",options=(ventilation_array))
    solar_thermal_slider = tab5.select_slider("Solar Thermal (m2)",options=(solar_thermal_array))
    PV_panel_slider = tab5.select_slider("PV Panels (KWp)",options=(PV_panel_array))
    lighting_slider = tab5.select_slider("Low-Energy Lights (%)",options=(lighting_array), value=lighting_array[5])

    
# Connecting array with sliders. The information defined in this section is the result of the study of the tool SAP sensitivity Tool 2009 for domestic buildings, based on SAP 2009 (Version: V.1.03 August 2013), developed by Centre For Research in the Built Environment, Welsh School of Architecture, Cardiff University.

# Thermal mass index
def TMi(a):
    return(thermal_mass_array.index(a))

# Wall U value index
def MWi(b):
    return(wall_UValue_array.index(b))

# Floor U value index
def MFi(c):
    return(floor_UValue_array.index(c))

# Roof U value index           
def MRi(d):
    return(roof_UValue_array.index(d))

# Windows U value index
def MOi(e):
    return(window_UValue_array.index(e))

# Glazing ratio index
def GRi(f):
    return(glazing_ratio_array.index(f))

# Shading device index
def SDi(g):
    return(shading_dev_array.index(g))

# Thermal bridge index
def THi(h):
    return(thermal_bridge_array.index(h))

# Heating system index 
def HSi(i):
    return(heating_system_array.index(i))

# q50 index
def IRi(j):
    return(q50_array.index(j))

# Ventilation Type index
def VTi(k):
    return(ventilation_array.index(k))

#Solar Thermal index
def STi(l):
    return(solar_thermal_array.index(l))

#PV panel index
def PVi(m):
    return(PV_panel_array.index(m))

# Type of house is detached fot his project      
TPi = 0

#floor/living area index 
def LAi(o):
    return(floor_area_array.index(o))

#orientation index
def ORi(p):
    return(orientation_array.index(p))

#region index
def RTi(q):
    return(location_array.index(q))

# Surface ratio index
def SRi(r):
    return(surface_ratio_array.index(r))

# Obstacle front boolean
def OFront(s):
    if s:
        return 1
    else:
        return 0

# Obstacle back boolean
def OBack(t):
    if t:
        return 1
    else:
        return 0

# Obstacle left boolean
def OLeft(u):
    if u:
        return 1
    else:
        return 0

# Obstacle right boolean
def ORight(v):
    if v:
        return 1
    else:
        return 0
#Efficient lighthing index 
def ELi(w): 
    return(lighting_array.index(w))

#def EAi(x): not included
#def ECi(y): not included
#def OVi(z): not included
#def ODi(aa): not included
#def HAi(ab): not included
#def SHi(ac):

#Region Solar index
def RSi(ad):
    return(region_solar_array.index(ad))

#calculating width box from floor area and surface ratio provided by user in sliders
def width_box(floor_area_slider,surface_ratio_slider):
    if SRi(surface_ratio_slider) ==0:
        result = (math.sqrt(floor_area_slider))
    elif SRi(surface_ratio_slider) == 1:
        result = (math.sqrt(floor_area_slider/1.6))
    elif SRi(surface_ratio_slider) == 2:
        result = (math.sqrt(floor_area_slider/2.7))
    elif SRi(surface_ratio_slider) == 3:
        result = (math.sqrt(floor_area_slider*1.6))
    elif SRi(surface_ratio_slider) == 4:
        result = (math.sqrt(floor_area_slider*2.7))
    return result
width_box = width_box(floor_area_slider,surface_ratio_slider)
length_box = floor_area_slider/width_box

#Standar Baseline -  SAP calculation
instring_baseline="TM_1_MW_7_MF_4_MR_6_MO_4_GR_3_SD_0_TH_0_HS_3_IR_1_VT_0_ST_0_PV_0_TP_0_LA_2_OR_4_RT_4_SR_0_OF_0_OB_0_OL_0_OR_0_EL_5_EA_0_EC_0_OV_0_OD_0_HA_0_SH_0_RS_3"
baseline_initial = sap_engine_2009.sap_result(instring_baseline,"","","","","","","","","","")
baseline_separated = baseline_initial.split(",")
baseline_result = (baseline_separated[0:6])
# transforming to float (baseline_result) using loop
for i in range(0, len(baseline_result)):
    baseline_result[i] = float(baseline_result[i])

#Modified Project by updating sliders - SAP calculation
instring_modified = "TM_"+str(TMi(thermal_mass_slider))+"_MW_"+str(MWi(wall_UValue_slider))+"_MF_"+str(MFi(floor_UValue_slider))+"_MR_"+str((MRi(roof_UValue_slider)))+"_MO_"+str(MOi(window_UValue_slider))+"_GR_"+str(GRi(glazing_ratio_slider))+"_SD_"+str(SDi(shading_dev_slider))+"_TH_"+str(THi(thermal_bridging_slider))+"_HS_"+str(HSi(heating_system_slider))+"_IR_"+str(IRi(infiltration_rate_slider))+"_VT_"+str(VTi(ventilation_slider))+"_ST_"+str(STi(solar_thermal_slider))+"_PV_"+str(PVi(PV_panel_slider))+"_TP_0_LA_"+str(LAi(floor_area_slider))+"_OR_"+str(ORi(orientation_slider))+"_RT_"+str(RTi(location_selectbox))+"_SR_"+str(SRi(surface_ratio_slider))+"_OF_"+str(OFront(obs_OF))+"_OB_"+str(OBack(obs_OB))+"_OL_"+str(OLeft(obs_OL))+"_OR_"+str(ORight(obs_OR))+"_EL_"+str(ELi(lighting_slider))+"_EA_0_EC_0_OV_0_OD_0_HA_0_SH_0_RS_"+str(RSi(region_solar_slider))
SAP_modified = sap_engine_2009.sap_result((instring_modified),"","","","","","","","","","")
SAP_modified_separated = SAP_modified.split(",")
SAP_modified_result = (SAP_modified_separated[0:6])
#transforming SAP modified to float (result) using loop
for i in range(0, len(SAP_modified_result)):
    SAP_modified_result[i] = float(SAP_modified_result[i])

col1.title(':blue[SAP 2009 SENSITIVITY TOOL]')
col1.subheader(':grey[for domestic buildings]')
col1.caption("Application based on 'Simple Simulation Sensitivity Tool' (Crobu et al. 2013)")


#3D concept model
#box = Cell.Prism(width=width_box, length=length_box, height=3)
#data_box = Plotly.DataByTopology(box)
fig_box = Plotly.FigureByData(data_box)
#col1.plotly_chart(fig_box, use_container_width=True)
#col1.subheader(":blue[Project dimensions]")
#col1.markdown(":blue[Width:] "+str(round(width_box,2))+" m, "+ ":blue[Length:] "+str(round(length_box,2))+" m, " +":blue[Surface:] "+str(round(width_box*length_box))+" m2")
#col1.markdown(":blue[Length:] "+str(round(length_box,2))+" m")
#col1.markdown(":blue[Surface:] "+str(round(width_box*length_box))+" m2")

col2.subheader("Analysis Result")

#Use this button for define project baseline to compare with the modified project. First set baseline as the standard and the second apply modification as baseline to compare with further updated project.
standard_baseline = col2.button("Standard Baseline")
modified_baseline = col2.button("Update Baseline")
#Define bsaeline used in the SAP baseline analysis
def baseline_used():
    if modified_baseline == True:
        col2.markdown(":blue[Baseline:] Modified")
    elif standard_baseline == True:
        col2.markdown(":blue[Baseline:] Standard")
    else:
        col2.markdown(":blue[Baseline:] Standard")
baseline_used()

#Reporting Energy number and letter for the baseline 
# defined (standard or modified)
col2.metric("SAP Baseline", 
            str((SAP_modified_result[2])
                if modified_baseline == True 
                else (baseline_result[2])))   
col2.metric("Rating Baseline", 
            SAP_letter(float(baseline_result[2])))

#Use this button for apply project modifications and show energy performance rating
update_SAP = col2.button("Calculate Updated Project")   

#Reporting Energy number and letter for the updated project
col2.metric("SAP - Updated project",(((SAP_modified_result[2]) if modified_baseline == True else (baseline_result[2])))if update_SAP == False else (SAP_modified_result[2]))  
col2.metric("Rating - Updated Project", SAP_letter(float(baseline_result[2])) if update_SAP == False else SAP_letter(float(SAP_modified_result[2])))
epc_diag = col2.image(epc_image, caption=" Energy PErformance Certificate Chart (Crobu et al. 2013)")


    #test for creating epc diag from horizontal bar chart
    #bar_chart = alt.Chart(SAP_data).mark.bar().encode(y='values', x='SAP Letter'), st.altair_chart(bar_chart)

    #with colA:
        #Table_result = colA.metric("Baseline", str(baseline_result[2]))
    #with colB:
        #Letter_result = colB.metric("Baseline Rating", SAP_letter(float(baseline_result[2])))
    #with colC:    
        #Number_result = colC.metric("SAP updated", str(SAP_modified_result[2]))
    #with colD:
        #Letter_result = colD.metric("Updated Rating", SAP_letter(float(SAP_modified_result[2])))


#def baseline():
  #  if modified_baseline:
   #     st.write(str(SAP_modified_result[2]))
   # elif standard_baseline:
   #     st.write(str(baseline_result[2]))
#else:
    #st.write("Baseline: " +str(baseline_result[2])

    #Temporary code for comparing Baseline and modified SAP analysis
#col1.text(True if instring_baseline == instring_modified else False)
#col1.text("baseline:"+ instring_baseline)
#col1.text("modified:"+ instring_modified)
