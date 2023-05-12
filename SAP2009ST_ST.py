#!/usr/bin/env python
# coding: utf-8
# In[5]:
# TO RUN THIS:
# 1- GO TO TERMINAL
# 2- 
# 3- streamlit run SAP2009ST_ST.py

import streamlit as st
import topologicpy
import pandas as pd
import math
import sap_engine_2009
import plotly.express as px
from PIL import Image
from topologicpy.Cell import Cell
from topologicpy.Plotly import Plotly

#defining wide layout for Streamlit
st.set_page_config(layout="wide")

#Defining horizontal sections of dashboard
header = st.container()
general_info = st.container()
energy_performance = st.container()
features = st.container()
obs_layout= st.sidebar.columns([2,1])


colA, colB, colC, colD = st.columns(4)
#Fabric input
thermal_mass_array = [0,1,2]
wall_UValue_array =[2.1,2.0,1.7,1.0,0.6,0.45,0.35,0.3,0.25,0.2,0.15,0.10]
floor_UValue_array =[2.0,0.6,0.45,0.3,0.25,0.2,0.15,0.14,0.13,0.12,0.11,0.10]
roof_UValue_array =[2.0,1.5,1.,0.6,0.35,0.25,0.2,0.13,0.1]
window_UValue_array =[4.8,3.1,3,2.2,2,1.8,1.6,1.4,1.2,1,0.8]
thermal_bridge_array =["0.15 or NO INFO",0.08,0.04]

#System input
PV_array =[0,3.5,7,10.5,14,17.5,21,24.5,28]
heating_system_array = ["Electric","Solid Fuel","Oil","Nat. Gas","Heat Pump","Biomass"]
q50_array =["Poor/N.A.","Normal Practice","Good Practice","Best Practice"]
ventilation_array = ["Natural Ventilation", "MVHR"]
solar_thermal_array = ["NONE", "1.00", "2.00", "3.00", "4.00", "5.00", "6.00"]
PV_panel_array = ["NONE", "0.50", "1.00", "1.50","2.00", "2.50", "3.00", "3.50", "4.00"]
lighting_array=[0,10,20,30,40,50,60,70,80,90,100]

#input that affect the building size
glazing_ratio_array =[0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50]
floor_area_array =[50,60,70,80,90,100,110,120]
living_area_array =[22.5,18,17.5,18.4,18.9,21,20.9,19.2]
surface_ratio_array = ["Compact = 1:1","Rectangular = 1:1.6","Narrow = 1:2.7", "Wide = 1.6:1", "Extra-Wide= 2.7:1"] 
shading_dev_array = [0.24, 0.27, 0.60, 0.65, 0.70, 0.80, 0.85, 0.88, 0.90, "NONE"]
orientation_array = ["North","North West","West","South West","South","South East","East","Nort East"]
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
obs_image1 = Image.open('Obs_Image.jpg')
obs_image2 = Image.open('Obs_Image_Sides.jpg')

#Defining tabs with input to be included in the sidebar
with st.sidebar:
    tab1,tab2,tab3 = st.tabs(["Location and Geometric Input","Fabric input","Systems Input"])
    with tab1:
        col1, col2 = st.columns(2)
    
    #Defining building geometry
    tab1.subheader("Location and Geometric Input")
    location_selectbox= tab1.selectbox("Location",options = location_array)
    floor_area_slider = tab1.select_slider("Floor Area(m2)",options = floor_area_array)
    surface_ratio_slider = tab1.select_slider("Surface Ratio", options = surface_ratio_array)
    orientation_slider = tab1.select_slider("Orientation: Select the orientation of the most glazed facade of your building:", options = orientation_array)
    obs_text1 = tab1.subheader("Shelter Sides and Obstacles (Overshading):")
    obs_text2 = tab1.text("A side should be considered if all the following apply:")
    obs_diag1 = tab1.image(obs_image1)
    obs_diag2 = tab1.image(obs_image2)
    obs_text3 = tab1.caption("Click on the options below to identify the facades of your building where all the three conditions apply:")
    obs_OF = tab1.checkbox("Main glazed facade")
    obs_OL = tab1.checkbox("Side 1")
    obs_OR = tab1.checkbox("Side 2")
    obs_OB = tab1.checkbox("Side 3")
    
   
    #Defining graphic selection section for fabric
    tab2.subheader("Fabric Input")
    thermal_mass_slider = tab2.select_slider("Thermal mass", options=(thermal_mass_array))
    wall_UValue_slider = tab2.select_slider("Walls U-value",options=(wall_UValue_array))
    floor_UValue_slider = tab2.select_slider("Floor U-value", options=(floor_UValue_array))
    roof_UValue_slider = tab2.select_slider("Roof U-value",options=(roof_UValue_array))
    window_UValue_slider = tab2.select_slider("Windows U-value",options=(window_UValue_array))
    glazing_ratio_slider = tab2.select_slider("Glazing Ratio",options=(glazing_ratio_array))
    shading_dev_slider = tab2.select_slider("Shading Dev.",options=(shading_dev_array))
    thermal_bridging_slider = tab2.select_slider("Thermal Bridging",options=(thermal_bridge_array))
        
    #Defining graphic selection section for systems
    tab3.subheader("Systems Input")
    heating_system_slider = tab3.select_slider("Heating System",options=(heating_system_array))
    infiltration_rate_slider = tab3.select_slider("Infiltration Rate",options=(q50_array))
    ventilation_slider = tab3.select_slider("Ventilation",options=(ventilation_array))
    solar_thermal_slider = tab3.select_slider("Solar Thermal (m2)",options=(solar_thermal_array))
    PV_panel_slider = tab3.select_slider("PV Panels (KWp)",options=(PV_panel_array))
    lighting_slider = tab3.select_slider("Low-Energy Lights (%)",options=(lighting_array))

    
#Connecting array with sliders
#Thermal mass index
def TMi(a):
    return(thermal_mass_array.index(a))

def MWi(b):
    return(wall_UValue_array.index(b))

def MFi(c):
    return(floor_UValue_array.index(c))
           
def MRi(d):
    return(roof_UValue_array.index(d))

def MOi(e):
    return(window_UValue_array.index(e))

def GRi(f):
    return(glazing_ratio_array.index(f))

def SDi(g):
    return(shading_dev_array.index(g))

def THi(h):
    return(thermal_bridge_array.index(h))

#Defining systems selection 
def HSi(i):
    return(heating_system_array.index(i))

def IRi(j):
    return(q50_array.index(j))

def VTi(k):
    return(ventilation_array.index(k))
    
def STi(l):
    return(solar_thermal_array.index(l))

def PVi(m):
    return(PV_panel_array.index(m))
        
TPi = 0
        
def LAi(o):
    return(floor_area_array.index(o))

def ORi(p):
    return(orientation_array.index(p))


def RTi(q):
    return(location_array.index(q))

def SRi(r):
    return(surface_ratio_array.index(r))

def OFront(s):
    if s:
        return 1
    else:
        return 0

def OBack(t):
    if t:
        return 1
    else:
        return 0


def OLeft(u):
    if u:
        return 1
    else:
        return 0

def ORight(v):
    if v:
        return 1
    else:
        return 0
    


#def ELi(w): Not needed ! explain why

#def EAi(x):
#def ECi(y):
#def OVi(z):
#def ODi(aa):
#def HAi(ab):
#def SHi(ac):
#def RSi(ad):

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
 
#Defining baseline SAP
instring_baseline="TM_1_MW_7_MF_4_MR_6_MO_4_GR_3_SD_0_TH_0_HS_3_IR_1_VT_0_ST_0_PV_0_TP_0_LA_6_OR_0_RT_5_SR_1_OF_0_OB_0_OL_0_OR_0_EL_10_EA_0_EC_0_OV_0_OD_0_HA_0_SH_0_RS_3"

baseline_initial = sap_engine_2009.sap_result(instring_baseline,"","","","","","","","","","")

#Definining SAP updating sliders
instring_modified = "TM_"+str(TMi(thermal_mass_slider))+"_MW_"+str(MWi(wall_UValue_slider))+"_MF_"+str(MFi(floor_UValue_slider))+"_MR_"+str(MRi(roof_UValue_slider))+"_MO_"+str(MOi(window_UValue_slider))+"_GR_"+str(GRi(glazing_ratio_slider))+"_SD_"+str(SDi(shading_dev_slider))+"_TH_"+str(THi(thermal_bridging_slider))+"_HS_"+str(HSi(heating_system_slider))+"_IR_"+str(IRi(infiltration_rate_slider))+"_VT_"+str(VTi(ventilation_slider))+"_ST_"+str(STi(solar_thermal_slider))+"_PV_"+str(PVi(PV_panel_slider))+"_TP_"+str(TPi)+"_LA_"+str(LAi(floor_area_slider))+"_OR_"+str(ORi(orientation_slider))+"_RT_5_SR_"+str(SRi(surface_ratio_slider))+"_OF_"+str(OFront(obs_OF))+"_OB_"+str(OBack(obs_OB))+"_OL_"+str(OLeft(obs_OL))+"_OR_"+str(ORight(obs_OR))+"_EL_"+str(lighting_slider)+"_EA_0_EC_0_OV_0_OD_0_HA_0_SH_0_RS_3"

SAP_modified = sap_engine_2009.sap_result(instring_modified,"","","","","","","","","","")

with header:
    st.title('Energy performance')
    st.subheader("This platform is based on the SST2009 data")
    st.text("Width = "+str(round(width_box))+"m")
    st.text("Length = "+str(round(length_box))+"m")
    st.text("Surface "+str(width_box*length_box) +"m2")
    
    #baseline initial number
    baseline_separated = baseline_initial.split(",")
    baseline_result = (baseline_separated[0:6])
    
    # transforming to float (baseline_result) using loop
    for i in range(0, len(baseline_result)):
        baseline_result[i] = float(baseline_result[i])

    #SAP modified number
    SAP_modified_separated = SAP_modified.split(",")
    SAP_modified_result = (SAP_modified_separated[0:6])

    #transforming SAP modified to float (result) using loop
    for i in range(0, len(SAP_modified_result)):
        SAP_modified_result[i] = float(SAP_modified_result[i])
        
    #Defininf SAP letter according to SAP result
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

    with colA:
        Table_result = colA.metric("Baseline", str(baseline_result[2]))
        
    with colB:
        Letter_result = colB.metric("Baseline Rating", SAP_letter(float(baseline_result[2])))

    with colC:    
        Number_result = colC.metric("SAP updated", str(SAP_modified_result[2]))

    with colD:
        Letter_result = colD.metric("Updated Rating", SAP_letter(float(SAP_modified_result[2])))
        #Number_result2 = colC.metric("SAP modified", str(SAP_modified_result[2]))

#visualise box
    box = Cell.Prism(width=width_box, length=length_box, height=3)
    data_box = Plotly.DataByTopology(box)
    fig_box = Plotly.FigureByData(data_box)
    st.plotly_chart(fig_box)