import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Configuration (Wide horizontal matrix matching laboratory monitors)
st.set_page_config(page_title="Philippine Watershed Digital Twin", layout="wide")

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
    
    # 4. Main Core Dashboard Layout - Creating Your Clean Columns!
    col_regions, col_province, col_local = st.columns([1, 1, 1.2])
    
    # ==========================================
    # COLUMN 1: ISLAND GROUP & REGION SELECTOR
    # ==========================================
    with col_regions:
        st.header("📋 1. Location Filters")
        
        # Step A: Choose Master Island Group
        island = st.selectbox("Choose Island Group:", ["Luzon", "Visayas", "Mindanao"])
        st.markdown("---")
        
        # Step B: Cleanly display regions based on chosen Island
        if island == "Luzon":
            selected_region = st.radio("Select Admin Region:", ["NCR - Metro Manila", "Region IV-A (CALABARZON)", "Region II - Cagayan Valley"])
        elif island == "Visayas":
            selected_region = st.radio("Select Admin Region:", ["Region VI - Western Visayas", "Region VII - Central Visayas", "Region VIII - Eastern Visayas"])
        else:
            selected_region = st.radio("Select Admin Region:", ["Region XI - Davao Region", "Region XIII - Caraga", "BARMM Region"])
            
        st.markdown("---")
        st.subheader("🛠️ Environmental Variables")
        concrete = st.slider("Concrete / Urban Paved Area (%)", 0, 100, 50, key="concrete_slider")
        rain_intensity = st.selectbox("Simulated Rainfall Input:", ["Standard Monsoon Shower (30mm/hr)", "Severe Tropical Storm (70mm/hr)", "Super Typhoon Event (120mm/hr)"])

    # ==========================================
    # COLUMN 2: CLEAN PROVINCE SECTOR FOCUS
    # ==========================================
    with col_province:
        st.header("🏢 2. Province Focus")
        st.write(f"Active domain vectors for: **{selected_region}**")
        
        # Clean data routing arrays matching each option
        if selected_region == "Region IV-A (CALABARZON)":
            provinces = ["Laguna", "Cavite", "Batangas", "Rizal"]
        elif selected_region == "NCR - Metro Manila":
            provinces = ["Marikina District", "Manila District", "Quezon City District"]
        elif selected_region == "Region VI - Western Visayas":
            provinces = ["Iloilo", "Negros Occidental", "Capiz"]
        elif selected_region == "Region VII - Central Visayas":
            provinces = ["Cebu", "Bohol", "Siquijor"]
        elif selected_region == "Region XI - Davao Region":
            provinces = ["Davao del Sur", "Davao del Norte", "Davao Oriental"]
        elif selected_region == "Region XIII - Caraga":
            provinces = ["Agusan del Norte", "Agusan del Sur", "Surigao del Sur"]
        else:
            provinces = ["Base Sector Alpha", "Base Sector Beta"]

        selected_prov = st.selectbox("Select Target Province to Map:", provinces)
        st.info(f"🔄 Analyzing geological surface vectors for {selected_prov}...")

    # ==========================================
    # COLUMN 3: MAP DATA & HYDROGRAPH GENERATOR
    # ==========================================
    with col_local:
        st.header("🌊 3. Runoff Metrics & Map")
        
        # Core Hydrograph Calculation Processing
        rain_multipliers = {"Standard Monsoon Shower (30mm/hr)": 1.2, "Severe Tropical Storm (70mm/hr)": 2.5, "Super Typhoon Event (120mm/hr)": 4.8}
        base_flow = rain_multipliers[rain_intensity]
        time_hours = np.arange(0, 12, 0.5)
        peak_factor = base_flow * (1.0 + (concrete / 35.0))
        peak_time = 6.0 - (concrete / 25.0)
        runoff_flow = base_flow + (peak_factor - base_flow) * np.exp(-((time_hours - peak_time)**2) / 4.0)
        p4f_value = max(runoff_flow)
        
        st.write("📍 **Active Watershed Tracking Nodes:**")
        
        # Simplified, crash-free coordinate matrix router
        if selected_region == "Region IV-A (CALABARZON)" and selected_prov == "Laguna":
            map_data = {'lat': [14.2137, 14.2215, 14.2250], 'lon': [121.1744, 121.1620, 121.1810]}
            zoom_lvl = 11
        elif selected_region == "NCR - Metro Manila" and selected_prov == "Marikina District":
            map_data = {'lat': [14.6501, 14.6342], 'lon': [121.1044, 121.0965]}
            zoom_lvl = 12
        elif selected_region == "Region VI - Western Visayas" and selected_prov == "Iloilo":
            map_data = {'lat': [10.7202, 10.6978], 'lon': [122.5621, 122.5855]}
            zoom_lvl = 12
        elif selected_region == "Region VII - Central Visayas" and selected_prov == "Cebu":
            map_data = {'lat': [10.3157, 10.2930], 'lon': [123.8854, 123.8620]}
            zoom_lvl = 12
        elif selected_region == "Region XI - Davao Region" and selected_prov == "Davao del Sur":
            map_data = {'lat': [7.0736, 7.0920], 'lon': [125.6120, 125.5980]}
            zoom_lvl = 11
        elif selected_region == "Region XIII - Caraga" and selected_prov == "Agusan del Norte":
            map_data = {'lat': [8.9475, 8.9610], 'lon': [125.5406, 125.5122]}
            zoom_lvl = 11
        else:
            # Fallback point to keep the app working if a base region is chosen
            map_data = {'lat': [12.8797], 'lon': [121.7740]}
            zoom_lvl = 5
            
        df_map = pd.DataFrame(map_data)
        st.map(df_map, zoom=zoom_lvl)
        
        # Render graph plot line
        st.write(f"📈 **Predictive Hydrograph Waveform (P4F Peak Flow: {p4f_value:.2f} m³/s)**")
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(time_hours, runoff_flow, color="blue", linewidth=2.5, label="Runoff Volume")
        ax.axhline(y=8.0, color="red", linestyle="--", label="Flood Line Threshold")
        ax.set_xlabel("Timeline Duration (Hours)")
        ax.set_ylabel("Discharge rate (m³/s)")
        ax.legend()
        st.pyplot(fig)
