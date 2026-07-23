import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="CivicConnect AI",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ CivicConnect AI — Community Issue Reporter")
st.markdown("Pinpoint an infrastructure issue and report it directly to municipal authority.")

# HTML/JS Interactive Map Component
map_component_html = """



  
  
  
  



  
    
    🔍 Search
    📍 Find Me
  

  
  

  
  


"""

# 1. Render Map
components.html(map_component_html, height=500)

st.markdown("---")

# 2. Issue Form Controls
st.subheader("Report Details")

col1, col2 = st.columns(2)
with col1:
    issue_category = st.selectbox(
        "Issue Category",
        ["Pothole / Road Damage", "Broken Streetlight", "Sidewalk / ADA Ramp Access", "Graffiti / Vandalism", "Fallen Tree / Branch", "Other"]
    )
with col2:
    severity = st.select_slider(
        "Estimated Urgency / Severity",
        options=["Low", "Medium", "High", "Critical / Safety Hazard"]
    )

location_text = st.text_input("Selected Location Address", placeholder="e.g. 100 Main St, Greenburgh, NY")
issue_description = st.text_area("Description of Issue", placeholder="Provide details like exact road marker or safety concern...")

if st.button("🚀 Submit Ticket to Jurisdiction", type="primary"):
    if location_text and issue_description:
        st.success(f"✅ Ticket Created! Category: **{issue_category}** | Assigned based on location: **Town of Greenburgh**")
        st.balloons()
    else:
        st.warning("Please enter a location and brief description before submitting.")
