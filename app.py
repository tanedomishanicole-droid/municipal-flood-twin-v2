import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Configuration (Wide horizontal matrix matching laboratory monitors)
st.set_page_config(page_title="Luzon Watershed Digital Twin Matrix", layout="wide")

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
    # COLUMN 1: LUZON REGIONAL LIST
    # ==========================================
    with col_regions:
        st.header("📋 1. Luzon Regions")
        st.write("Select an active administrative region:")
        
        # Exact list of all 8 Luzon regions you requested
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
            ], index=5 # Defaults cleanly to CALABARZON
        )
            
        st.markdown("---")
        st.subheader("🛠️ Environmental Variables")
        concrete = st.slider("Concrete / Urban Paved Area (%)", 0, 100, 50, key="concrete_slider")
        rain_intensity = st.selectbox("Simulated Rainfall Input:", 
                                     ["Standard Monsoon Shower (30mm/hr)", "Severe Tropical Storm (70mm/hr)", "Super Typhoon Event (120mm/hr)"])

    # ==========================================
    # COLUMN 2: PROVINCE SECTOR FOCUS
    # ==========================================
    with col_province:
        st.header("🏢 2. Province Selection")
        st.write(f"Active domain vectors for: **{selected_region}**")
        
        # Simplified to just show the provinces directly
        if selected_region == "Region IV-A (CALABARZON)":
            provinces = ["Laguna", "Cavite", "Batangas", "Rizal", "Quezon"]
        elif selected_region == "National Capital Region (NCR)":
            provinces = ["Manila District", "Marikina District", "Caloocan District", "Taguig District"]
        else:
            provinces = ["North Sector Area", "South Sector Area"]

        selected_prov = st.selectbox("Select Target Province to Map Area:", provinces)
        
        # Quick data info card instead of a massive messy table
        st.info(f"🔄 Analyzing geological surface absorption for {selected_prov}...")

    # ==========================================
    # COLUMN 3: RUNOFF METRICS & TARGET ADVANCED MAP
    # ==========================================
    with col_local:
        st.header("🌊 3. Local Runoff Metrics")
        
        # Run hydrograph calculations
        rain_multipliers = {"Standard Monsoon Shower (30mm/hr)": 1.2, "Severe Tropical Storm (70mm/hr)": 2.5, "Super Typhoon Event (120mm/hr)": 4.8}
        base_flow = rain_multipliers[rain_intensity]
        time_hours = np.arange(0, 12, 0.5)
        peak_factor = base_flow * (1.0 + (concrete / 35.0))
        peak_time = 6.0 - (concrete / 25.0)
        runoff_flow = base_flow + (peak_factor - base_flow) * np.exp(-((time_hours - peak_time)**2) / 4.0)
        p4f_value = max(runoff_flow)
        
        st.write("📍 **Active Watershed Tracking Nodes:**")
        
        # Cleaned map setup routing directly to your real target sectors
        if selected_region == "Region IV-A (CALABARZON)" and selected_prov == "Laguna":
            map_data = {
                'lat': [14.2137, 14.2215, 14.2250, 14.2800],
                'lon': [121.1744, 121.1620, 121.1810, 121.4100]
            }
            zoom_lvl = 10
        elif selected_region == "National Capital Region (NCR)" and selected_prov == "Marikina District":
            map_data = {
                'lat': [14.6501, 14.6342, 14.6680],
                'lon': [121.1044, 121.0965, 121.1120]
            }
            zoom_lvl = 12
        else:
            map_data = {
                'lat': [15.2100], 
                'lon': [120.9600]
            }
            zoom_lvl = 7
            
        df_map = pd.DataFrame(map_data)
        st.map(df_map, zoom=zoom_lvl)
        
        # Render the P4F hydrograph graph
        st.write(f"📈 **Predictive Hydrograph Waveform (P4F Peak Flow: {p4f_value:.2f} m³/s)**")
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(time_hours, runoff_flow, color="blue", linewidth=2.5, label="Runoff Volume")
        ax.axhline(y=8.0, color="red", linestyle="--", label="Flood Line Threshold")
        ax.set_xlabel("Timeline Duration (Hours)")
        ax.set_ylabel("Discharge rate (m³/s)")
        ax.legend()
        st.pyplot(fig)
