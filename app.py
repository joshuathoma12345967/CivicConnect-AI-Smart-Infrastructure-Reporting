import streamlit as st
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="CivicConnect AI",
    page_icon="📍",
    layout="wide"
)

# Header
st.title("📍 CivicConnect AI")
st.subheader("Smart Infrastructure & Accessibility Reporting")
st.markdown("---")

# Simple jurisdiction classifier logic
def get_jurisdiction(lat, lon):
    # Bounding box for Town of Greenburgh (approximate for demo)
    if 41.00 <= lat <= 41.08 and -73.88 <= lon <= -73.78:
        return "Town of Greenburgh Department of Public Works"
    elif 40.90 <= lat <= 41.15 and -73.95 <= lon <= -73.70:
        return "Westchester County Department of Transportation"
    else:
        return "New York State Department of Transportation (NYSDOT)"

# Create two side-by-side columns: Left for Map, Right for Side Panel Form
col_map, col_form = st.columns([2, 1])

# --- RIGHT COLUMN: REPORT FORM ---
with col_form:
    st.header("📝 Report an Issue")
    
    category = st.selectbox(
        "Issue Category",
        [
            "Pothole",
            "Broken Sidewalk",
            "Flooding",
            "Fallen Tree / Branch",
            "Damaged Sign",
            "Graffiti",
            "Broken Streetlight",
            "♿ Accessibility Barrier (Missing Ramp, Unsafe Crossing, etc.)"
        ]
    )
    
    address = st.text_input("Address / Location Description", "Central Ave & Tarrytown Rd, Greenburgh, NY")
    
    description = st.text_area(
        "Issue Details", 
        placeholder="Describe the issue (e.g. Deep pothole on east lane...)"
    )
    
    st.info("💡 **Tip:** Click anywhere on the map to place an exact pinpoint!")
    
    submit_button = st.button("Submit Report", type="primary", use_container_width=True)

# Default location (Greenburgh, NY)
default_lat, default_lon = 41.033, -73.824

# --- LEFT COLUMN: MAP DISPLAY ---
with col_map:
    st.header("📍 Interactive Location Map")
    
    # Initialize Folium Map
    m = folium.Map(location=[default_lat, default_lon], zoom_start=14)
    
    # Render map and get interactive click event
    map_data = st_folium(m, width="100%", height=500)
    
    # Detect if user clicked on map
    if map_data and map_data.get("last_clicked"):
        selected_lat = map_data["last_clicked"]["lat"]
        selected_lon = map_data["last_clicked"]["lng"]
    else:
        selected_lat, selected_lon = default_lat, default_lon

# Handle Form Submission
if submit_button:
    agency = get_jurisdiction(selected_lat, selected_lon)
    
    st.success("✅ **Report Successfully Submitted!**")
    
    st.markdown("### 🤖 CivicConnect AI Routing Summary")
    st.json({
        "Issue Type": category,
        "Location Address": address,
        "Coordinates": f"{selected_lat:.4f}, {selected_lon:.4f}",
        "Description": description,
        "Assigned Jurisdiction": agency,
        "Status": "Ticket Created & Dispatched"
    })
