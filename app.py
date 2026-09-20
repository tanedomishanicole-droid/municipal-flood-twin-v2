import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Municipal Flood Digital Twin", layout="wide")

# Secure Access Gateway Simulation
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔒 Municipal Watershed Monitoring Portal")
    st.subheader("Restricted Access - Certified Disaster Personnel Only")
    st.write("Authorized access for PAGASA, Local DRRMCs, and environmental professionals.")
    
    passcode = st.text_input("Enter Institutional Access Passcode:", type="password")
    if st.button("Verify Credentials"):
        if passcode == "MUNICIPAL-DRRMC-SECURE911!":
            st.session_state['authenticated'] = True
            st.success("Access Granted. Initializing Digital Twin Environment...")
            st.rerun()
        else:
            st.error("Invalid Administrative Passcode. Access Denied.")
else:
    # Main Dashboard Layout
    st.title("🌊 Localized Watershed Digital Twin Dashboard")
    st.write("⚡ *A Science & Innovation Research Project Framework (Grade 8 STE)*")
    
    if st.button("Log Out"):
        st.session_state['authenticated'] = False
        st.rerun()
        
    st.markdown("---")
    
    # Sidebar Control Matrix (Independent Variables)
    st.sidebar.header("🛠️ Environmental Variable Simulator")
    st.sidebar.write("Adjust surface layouts to observe simulated flash flood outcomes.")
    
    concrete = st.sidebar.slider("Concrete / Urban Paved Area (%)", 0, 100, 30)
    forest = 100 - concrete
    st.sidebar.info(f"Natural Vegetated Ground Absorption Area: {forest}%")
    
    rain_intensity = st.sidebar.selectbox("Simulated Storm Profile (Rainfall Input):", 
                                         ["Standard Monsoon Shower (30mm/hr)", "Severe Tropical Storm (70mm/hr)", "Super Typhoon Event (120mm/hr)"])
    
    # Core Mathematical Hydrograph Calculations (P4F Engine)
    rain_multipliers = {"Standard Monsoon Shower (30mm/hr)": 1.2, "Severe Tropical Storm (70mm/hr)": 2.5, "Super Typhoon Event (120mm/hr)": 4.8}
    base_flow = rain_multipliers[rain_intensity]
    
    time_hours = np.arange(0, 12, 0.5)
    peak_factor = base_flow * (1.0 + (concrete / 35.0))
    peak_time = 6.0 - (concrete / 25.0)
    
    runoff_flow = base_flow + (peak_factor - base_flow) * np.exp(-((time_hours - peak_time)**2) / 4.0)
    p4f_value = max(runoff_flow)
    
    # Visual Output Cards & Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Calculated Peak Flood Flow (P4F)", value=f"{p4f_value:.2f} m³/s")
    with col2:
        soil_retention = max(0, forest * 0.8 - (base_flow * 2))
        st.metric(label="Estimated Ground Water Infiltration", value=f"{soil_retention:.1f} mm")
    with col3:
        if p4f_value < 4.0:
            status = "🟢 LEVEL 1: NORMAL INFRASTRUCTURE STABILITY"
            color_hex = "#239B56"
        elif p4f_value < 8.0:
            status = "🟡 LEVEL 2: INTENSE MONITORING (COLLAPSE HAZARD ALERT)"
            color_hex = "#D4AC0D"
        else:
            status = "🔴 LEVEL 3: IMMEDIATE EVACUATION ORDER ACTIVATED"
            color_hex = "#CB4335"
        st.markdown(f"<div style='padding:15px; border-radius:5px; background-color:{color_hex}; color:white; font-weight:bold; text-align:center;'>{status}</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Graphs and Maps Section
    col_graph, col_map = st.columns(2)
    
    with col_graph:
        st.subheader("📈 Real-Time Predictive Hydrograph Trend")
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.plot(time_hours, runoff_flow, color="blue", linewidth=2, label="Simulated Runoff Volume")
        ax.axhline(y=8.0, color="red", linestyle="--", label="Critical Flash Flood Threshold")
        ax.set_xlabel("Storm Duration Timeline (Hours)")
        ax.set_ylabel("Discharge Capacity Rate (m³/s)")
        ax.legend()
        st.pyplot(fig)
        
    with col_map:
        st.subheader("🗺️ Sector Risk Classification Mapping")
        st.write("Grid coordinates corresponding to municipal riverbank zones:")
        
        grid_rows = []
        for r in range(4):
            row_vals = []
            for c in range(4):
                sector_risk = (p4f_value * (1.2 if r >= 2 else 0.7))
                if sector_risk < 4.0:
                    row_vals.append("🟢 Safe")
                elif sector_risk < 8.0:
                    row_vals.append("🟡 Alert")
                else:
                    row_vals.append("🚨 Collapse Threat")
            grid_rows.append(row_vals)
            
        df_map = pd.DataFrame(grid_rows, columns=["Zone A", "Zone B", "Zone C", "Zone D"], index=["Sect 1", "Sect 2", "Sect 3", "Sect 4"])
        st.dataframe(df_map)
