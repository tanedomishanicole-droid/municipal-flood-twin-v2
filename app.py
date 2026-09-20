import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Configuration (Wide horizontal matrix matching laboratory monitors)
st.set_page_config(page_title="Philippine Watershed Digital Twin Matrix", layout="wide")

# 2. Secure Access Gateway Simulation
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔒 National Watershed Monitoring Portal")
    st.subheader("Restricted Access - Certified Disaster Personnel Only")
    st.write("Authorized access for PAGASA, National DRRMC, and local municipal disaster boards.")
    
    passcode = st.text_input("Enter Institutional Access Passcode:", type="password")
    if st.button("Verify Credentials"):
        if passcode == "MUNICIPAL-DRRMC-SECURE911!":
            st.session_state['authenticated'] = True
            st.success("Access Granted. Initializing National Digital Twin Environment...")
            st.rerun()
        else:
            st.error("Invalid Administrative Passcode. Access Denied.")
else:
    # 3. Main Dashboard Header
    st.title("🇵🇭 Philippine Watershed Digital Twin Drill-Down Matrix")
    st.write("⚡ *Science & Innovation Research Interface — Grade 8 STE (Conde, Fatallar, Tañedo)*")
    
    if st.button("Log Out"):
        st.session_state['authenticated'] = False
        st.rerun()
        
    st.markdown("---")
    
    # 4. Main Core Dashboard Layout - Creating Your Columns!
    col_regions, col_province, col_local = st.columns([1, 1, 1.2])
    
    # ==========================================
    # COLUMN 1: ISLAND GROUP & REGIONAL OVERVIEW
    # ==========================================
    with col_regions:
        st.header("📋 1. Regional Sector")
        
        # Master Filter: Island Group Selector
        island_group = st.selectbox("Choose Target Island Group:", ["Luzon", "Visayas", "Mindanao"])
        st.markdown("---")
        
        # Dynamic rendering of regions based on your chosen Island Group
        if island_group == "Luzon":
            selected_region = st.radio(
                "Select Admin Region:",
                [
                    "National Capital Region (NCR)",
                    "Cordillera Administrative Region (CAR)",
                    "Region I (Ilocos Region)",
                    "Region II (Cagayan Valley)",
                    "Region III (Central Luzon)",
                    "Region IV-A (CALABARZON)",
                    "MIMAROPA Region",
                    "Region V (Bicol Region)"
                ], index=5 # Defaults to CALABARZON
            )
        elif island_group == "Visayas":
            selected_region = st.radio(
                "Select Admin Region:",
                [
                    "Region VI (Western Visayas)",
                    "Region VII (Central Visayas)",
                    "Region VIII (Eastern Visayas)",
                    "Negros Island Region (NIR)"
                ]
            )
        else: # Mindanao
            selected_region = st.radio(
                "Select Admin Region:",
                [
                    "Region IX (Zamboanga Peninsula)",
                    "Region X (Northern Mindanao)",
                    "Region XI (Davao Region)",
                    "Region XII (SOCCSKSARGEN)",
                    "Region XIII (Caraga)",
                    "BARMM (Bangsamoro Autonomous Region)"
                ]
            )
            
        # Environmental Variables placed underneath column 1 controls
        st.markdown("---")
        st.subheader("🛠️ Environmental Variables")
        concrete = st.slider("Concrete / Urban Paved Area (%)", 0, 100, 50, key="concrete_slider")
        rain_intensity = st.selectbox("Simulated Rainfall Input:", 
                                     ["Standard Monsoon Shower (30mm/hr)", "Severe Tropical Storm (70mm/hr)", "Super Typhoon Event (120mm/hr)"])

    # ==========================================
    # COLUMN 2: REGIONAL FOCUS (PROVINCES & CAPITALS)
    # ==========================================
    with col_province:
        st.header("🏢 2. Province & Capital Focus")
        st.write(f"Displaying structure vectors for: **{selected_region}**")
        
        # Structural data routing based on selection rules
        if selected_region == "Region IV-A (CALABARZON)":
            province_data = {
                "Province": ["Laguna", "Cavite", "Batangas", "Rizal", "Quezon"],
                "Capital City/Town": ["Santa Cruz", "Imus", "Batangas City", "Antipolo", "Lucena City"],
                "Risk Classification": ["⚠️ High Runoff Coastal", "⚡ Rapid Urban Runoff", "🌊 Flash Flood Basins", "⛰️ Landslide Vulnerable", "🌊 Tidal Flood Vulnerable"]
            }
        elif selected_region == "National Capital Region (NCR)":
            province_data = {
                "Province": ["Metro Manila District 1", "Metro Manila District 2", "Metro Manila District 3", "Metro Manila District 4"],
                "Capital City/Town": ["Manila City", "Marikina City", "Caloocan City", "Taguig City"],
                "Risk Classification": ["🌊 Tidal Runoff Basin", "🚨 High P4F Catchment", "⚠️ Urban Flash Flood", "🌊 Low-lying Coastal"]
            }
        elif selected_region == "Region VI (Western Visayas)":
            province_data = {
                "Province": ["Iloilo", "Negros Occidental", "Capiz", "Aklan", "Antique"],
                "Capital City/Town": ["Iloilo City", "Bacolod City", "Roxas City", "Kalibo", "San Jose de Buenavista"],
                "Risk Classification": ["🚨 Jaro River Basin", "⚠️ Urban Flash Flooding", "🌊 Lowland Flood Basin", "🌊 Coastal Runoff Basin", "⛰️ Mountain Flash Runoff"]
            }
        elif selected_region == "Region VII (Central Visayas)":
            province_data = {
                "Province": ["Cebu", "Bohol", "Negros Oriental", "Siquijor"],
                "Capital City/Town": ["Cebu City", "Tagbilaran City", "Dumaguete City", "Siquijor"],
                "Risk Classification": ["🚨 Tejero Creek Basin", "⚠️ Valley Flash Flood", "🌊 Port Dredging Basin", "🟢 Stable Coastlines"]
            }
        elif selected_region == "Region XI (Davao Region)":
            province_data = {
                "Province": ["Davao del Sur", "Davao del Norte", "Davao de Oro", "Davao Oriental"],
                "Capital City/Town": ["Davao City", "Tagum City", "Nabunturan", "Mati City"],
                "Risk Classification": ["🚨 Davao River System", "⚠️ Agricultural Runoff", "⛰️ High Landslide Risk", "🌊 Open Ocean Surge"]
            }
        elif selected_region == "Region XIII (Caraga)":
            province_data = {
                "Province": ["Agusan del Norte", "Agusan del Sur", "Surigao del Norte", "Surigao del Sur"],
                "Capital City/Town": ["Butuan City", "Prosperidad", "Surigao City", "Tandag City"],
                "Risk Classification": ["🚨 Agusan River Delta", "🌊 Lowland Plain Basin", "⛰️ Mining Runoff Threat", "🌊 Coastal Wave Exposure"]
            }
        else:
            # Universal placeholder layout for remaining sectors to optimize code size
            province_data = {
                "Province": ["Primary Sector Alpha", "Secondary Sector Beta"],
                "Capital City/Town": ["Capital Hub Town A", "Capital Hub Town B"],
                "Risk Classification": ["🟢 Absorbent Ground Base", "⚠️ Moderate Surface Runoff"]
            }

        df_prov = pd.DataFrame(province_data)
        selected_prov = st.selectbox("Select Target Area to Analyze Local Municipalities:", df_prov["Province"])
        st.dataframe(df_prov, use_container_width=True)

    # ==========================================
    # COLUMN 3: LOCAL MONITORING NODE (MUNICIPALITIES & HYDROGRAPHS)
    # ==========================================
    with col_local:
        st.header("🌊 3. Local Runoff Metrics")
        
        # Run hydrograph parsing scripts matching Column 1 adjustments
        rain_multipliers = {"Standard Monsoon Shower (30mm/hr)": 1.2, "Severe Tropical Storm (70mm/hr)": 2.5, "Super Typhoon Event (120mm/hr)": 4.8}
        base_flow = rain_multipliers[rain_intensity]
        time_hours = np.arange(0, 12, 0.5)
        peak_factor = base_flow * (1.0 + (concrete / 35.0))
        peak_time = 6.0 - (concrete / 25.0)
        runoff_flow = base_flow + (peak_factor - base_flow) * np.exp(-((time_hours - peak_time)**2) / 4.0)
        p4f_value = max(runoff_flow)
        
        st.write(f"📍 **Active Watershed Tracking Nodes ({island_group}):**")
        
        # Coordinate mapping logic blocks tailored by province selection
        if island_group == "Luzon" and selected_region == "Region IV-A (CALABARZON)" and selected_prov == "Laguna":
            map_data = {
                'lat': [14.2137, 14.2215, 14.2250, 14.2800],
                'lon': [121.1744, 121.1620, 121.1810, 121.4100],
                'Vulnerable Towns': ['Calamba City (Sucol Waterfront)', 'San Cristobal Riverbank', 'Barangay Lingga Coastline', 'Santa Cruz Capital Basin']
            }
            zoom_lvl = 10
        elif island_group == "Luzon" and selected_region == "National Capital Region (NCR)":
            map_data = {
                'lat': [14.6501, 14.6342, 14.6680],
                'lon': [121.1044, 121.0965, 121.1120],
                'Vulnerable Towns': ['Tumana Floodway, Marikina', 'Marikina Bridge Node', 'Nangka River Junction']
            }
            zoom_lvl = 12
        elif island_group == "Visayas" and selected_region == "Region VI (Western Visayas)" and selected_prov == "Iloilo":
            map_data = {
                'lat': [10.7202, 10.6978, 10.7411],
                'lon': [122.5621, 122.5855, 122.5310],
                'Vulnerable Towns': ['Jaro River Mouth Hub', 'Mandurriao Inundation Basin', 'Lapaz High Runoff Zone']
            }
            zoom_lvl = 12
Use code with caution.elif island_group == "Visayas" and selected_region == "Region VII (Central Visayas)" and selected_prov == "Cebu":map_data = {'lat': [10.3157, 10.2930, 10.3420],'lon': [123.8854, 123.8620, 123.9144],'Vulnerable Towns': ['Tejero Waterway Point', 'Kinalumsan Creek Area', 'Mahiga Runoff Base']}zoom_lvl = 12elif island_group == "Mindanao" and selected_region == "Region XI (Davao Region)" and selected_prov == "Davao City":map_data = {'lat': [7.0736, 7.0920, 7.0511],'lon': [125.6120, 125.5980, 125.6315],'Vulnerable Towns': ['Davao River Bridge Node', 'Matina Pangi Runoff Point', 'Agdao Coastal Interface']}zoom_lvl = 11elif island_group == "Mindanao" and selected_region == "Region XIII (Caraga)" and selected_prov == "Agusan del Norte":map_data = {'lat': [8.9475, 8.9610],'lon': [125.5406, 125.5122],'Vulnerable Towns': ['Agusan River Delta Outlet', 'Magallanes Riverbank Monitor']}zoom_lvl = 11else:map_data = {'lat': [12.8797],'lon': [121.7740],'Vulnerable Towns': ['Philippine Geographic Center']}zoom_lvl = 5df_map = pd.DataFrame(map_data)st.map(df_map, zoom=zoom_lvl)# Display corresponding data graph plotsst.write(f"📈 Predictive Hydrograph Waveform (P4F Peak Flow: {p4f_value:.2f} m³/s)")fig, ax = plt.subplots(figsize=(6, 3))ax.plot(time_hours, runoff_flow, color="blue", linewidth=2.5, label="Runoff Volume")ax.axhline(y=8.0, color="red", linestyle="--", label="Flood Line Threshold")ax.set_xlabel("Timeline Duration (Hours)")ax.set_ylabel("Discharge rate (m³/s)")ax.legend()st.pyplot(fig)
