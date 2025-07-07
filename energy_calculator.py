import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4682B4;
        margin-bottom: 1rem;
    }
    .energy-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4682B4;
        margin: 1rem 0;
    }
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<div class="main-header">⚡ Energy Consumption Calculator</div>', unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    st.markdown('<div class="sub-header">📋 Personal Information</div>', unsafe_allow_html=True)
    
    name = st.text_input("👤 Enter your name:", placeholder="Your full name")
    age = st.number_input("🎂 Enter your age:", min_value=1, max_value=120, value=25)
    city = st.text_input("🏙️ Enter your city:", placeholder="Your city")
    area = st.text_input("📍 Enter your area name:", placeholder="Your area/locality")
    
    st.markdown('<div class="sub-header">🏠 Housing Information</div>', unsafe_allow_html=True)
    
    flat_tenament = st.selectbox(
        "🏠 Type of residence:",
        ["Select an option", "Flat", "Tenement"],
        index=0
    )
    
    facility = st.selectbox(
        "🏠 Housing configuration:",
        ["Select an option", "1BHK", "2BHK", "3BHK"],
        index=0
    )
    
    st.markdown('<div class="sub-header">⚡ Appliances</div>', unsafe_allow_html=True)
    
    ac = st.radio("❄️ Are you using AC?", ["No", "Yes"])
    fridge = st.radio("🧊 Are you using Fridge?", ["No", "Yes"])
    washing_machine = st.radio("🧺 Are you using Washing Machine?", ["No", "Yes"])

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if name and facility != "Select an option":
        # Calculate energy consumption
        cal_energy = 0
        
        # Base consumption based on housing type
        if facility.lower() == "1bhk":
            cal_energy += 2 * 0.4 + 2 * 0.8  # 2.4 kWh
        elif facility.lower() == "2bhk":
            cal_energy += 3 * 0.4 + 3 * 0.8  # 3.6 kWh
        elif facility.lower() == "3bhk":
            cal_energy += 4 * 0.4 + 4 * 0.8  # 4.8 kWh
        
        # Additional appliances
        if ac == "Yes":
            cal_energy += 3
        if fridge == "Yes":
            cal_energy += 3
        if washing_machine == "Yes":
            cal_energy += 3
        
        # Display results
        st.markdown(f"## 👋 Hello {name}!")
        
        # Energy consumption card
        st.markdown(f"""
        <div class="energy-card">
            <h2>⚡ Your Daily Energy Consumption</h2>
            <h1>{cal_energy:.1f} kWh</h1>
            <p>Based on your housing and appliances</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Breakdown of consumption
        st.markdown("### 📊 Energy Breakdown")
        
        # Calculate breakdown
        breakdown_data = []
        base_consumption = 0
        
        if facility.lower() == "1bhk":
            base_consumption = 2.4
        elif facility.lower() == "2bhk":
            base_consumption = 3.6
        elif facility.lower() == "3bhk":
            base_consumption = 4.8
        
        breakdown_data.append({"Category": "Base Consumption", "Energy (kWh)": base_consumption})
        
        if ac == "Yes":
            breakdown_data.append({"Category": "Air Conditioner", "Energy (kWh)": 3.0})
        if fridge == "Yes":
            breakdown_data.append({"Category": "Refrigerator", "Energy (kWh)": 3.0})
        if washing_machine == "Yes":
            breakdown_data.append({"Category": "Washing Machine", "Energy (kWh)": 3.0})
        
        # Create DataFrame
        df = pd.DataFrame(breakdown_data)
        
        # Create pie chart
        fig = px.pie(df, values='Energy (kWh)', names='Category', 
                     title='Energy Consumption by Category',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly and yearly projections
        st.markdown("### 📈 Consumption Projections")
        
        col_monthly, col_yearly = st.columns(2)
        
        with col_monthly:
            monthly_consumption = cal_energy * 30
            st.metric(
                label="Monthly Consumption",
                value=f"{monthly_consumption:.0f} kWh",
                delta=f"₹{monthly_consumption * 5:.0f} (approx. cost)"
            )
        
        with col_yearly:
            yearly_consumption = cal_energy * 365
            st.metric(
                label="Yearly Consumption",
                value=f"{yearly_consumption:.0f} kWh",
                delta=f"₹{yearly_consumption * 5:.0f} (approx. cost)"
            )
        
        # Environmental impact
        st.markdown("### 🌱 Environmental Impact")
        co2_emission = cal_energy * 0.82  # kg CO2 per kWh (India average)
        trees_needed = co2_emission / 22  # Trees needed to offset daily CO2
        
        col_co2, col_trees = st.columns(2)
        
        with col_co2:
            st.metric(
                label="Daily CO2 Emission",
                value=f"{co2_emission:.2f} kg",
                delta="Carbon footprint"
            )
        
        with col_trees:
            st.metric(
                label="Trees needed per day",
                value=f"{trees_needed:.2f}",
                delta="To offset emissions"
            )
        
    else:
        st.markdown("""
        <div class="info-box">
            <h3>🎯 Welcome to the Energy Consumption Calculator!</h3>
            <p>Please fill in your details in the sidebar to calculate your energy consumption.</p>
            <ul>
                <li>Enter your personal information</li>
                <li>Select your housing type</li>
                <li>Choose your appliances</li>
                <li>Get instant energy consumption analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if name and facility != "Select an option":
        st.markdown("### 📋 Your Profile")
        
        profile_data = {
            "Field": ["Name", "Age", "City", "Area", "Residence Type", "Housing", "AC", "Fridge", "Washing Machine"],
            "Value": [name, age, city, area, flat_tenament, facility, ac, fridge, washing_machine]
        }
        
        profile_df = pd.DataFrame(profile_data)
        st.dataframe(profile_df, use_container_width=True, hide_index=True)
        
        # Energy tips
        st.markdown("### 💡 Energy Saving Tips")
        
        tips = [
            "🌡️ Set AC temperature to 24°C or higher",
            "💡 Use LED bulbs instead of incandescent",
            "🔌 Unplug devices when not in use",
            "🌅 Use natural light during daytime",
            "🧊 Keep refrigerator at optimal temperature",
            "🚿 Use energy-efficient appliances"
        ]
        
        for tip in tips:
            st.markdown(f"- {tip}")
    
    else:
        st.markdown("### 🎯 Why Calculate Energy Consumption?")
        st.markdown("""
        - **💰 Save Money**: Understand your electricity bills
        - **🌍 Environment**: Reduce your carbon footprint
        - **📊 Planning**: Better energy management
        - **⚡ Efficiency**: Identify energy-hungry appliances
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>⚡ Energy Consumption Calculator | Built with Streamlit</p>
    <p>💡 Start saving energy today!</p>
</div>
""", unsafe_allow_html=True)