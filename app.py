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

# Fixed HTML/JS Interactive Map Component
map_component_html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    * { 
      box-sizing: border-box; 
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
    }
    body { 
      margin: 0; 
      padding: 10px; 
      background-color: #1e293b; /* Dark card background to match Streamlit */
      color: #f8fafc;
      border-radius: 12px;
    }
    
    .location-controls {
      display: flex;
      gap: 10px;
      margin-bottom: 10px;
    }

    input {
      flex: 1;
      padding: 12px 14px;
      border: 1px solid #475569;
      background-color: #0f172a;
      color: #ffffff;
      border-radius: 8px;
      font-size: 14px;
      outline: none;
    }

    input::placeholder {
      color: #94a3b8;
    }

    button {
      padding: 12px 18px;
      border: none;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      font-size: 14px;
      color: white;
      white-space: nowrap;
    }

    .btn-search { 
      background-color: #2563eb; 
    }
    .btn-search:hover {
      background-color: #1d4ed8;
    }

    .btn-locate { 
      background-color: #0d9488; 
    }
    .btn-locate:hover {
      background-color: #0f766e;
    }

    #status {
      font-size: 13px;
      color: #38bdf8;
      min-height: 20px;
      margin-bottom: 8px;
      font-weight: 500;
    }

    #map {
      height: 420px;
      width: 100%;
      border-radius: 8px;
      border: 1px solid #334155;
    }
  </style>
</head>
<body>

  <div class="location-controls">
    <input 
      type="text" 
      id="addressInput" 
      placeholder="Type an address or street name..." 
      onkeypress="if(event.key === 'Enter') searchAddress()"
    />
    <button class="btn-search" onclick="searchAddress()">🔍 Search</button>
    <button id="locateBtn" class="btn-locate" onclick="locateUser()">📍 Find Me</button>
  </div>

  <div id="status"></div>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    // Initialize map default view (Westchester / Greenburgh area)
    const map = L.map('map').setView([41.033, -73.812], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap'
    }).addTo(map);

    let activeMarker = null;

    // Fix Streamlit iframe height rendering bug
    setTimeout(() => {
      map.invalidateSize();
    }, 400);

    function updateMapLocation(lat, lng, label = '') {
      if (activeMarker) map.removeLayer(activeMarker);

      map.flyTo([lat, lng], 16, { animate: true, duration: 1.2 });
      activeMarker = L.marker([lat, lng], { draggable: true }).addTo(map);

      if (label) activeMarker.bindPopup(`<b>Location:</b><br>${label}`).openPopup();

      activeMarker.on('dragend', function(e) {
        const coords = e.target.getLatLng();
        reverseGeocode(coords.lat, coords.lng);
      });
    }

    function locateUser() {
      const status = document.getElementById('status');
      if (!navigator.geolocation) {
        status.textContent = 'Geolocation is not supported by your browser.';
        return;
      }

      status.textContent = '📍 Finding your exact location...';

      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const lat = pos.coords.latitude;
          const lng = pos.coords.longitude;
          updateMapLocation(lat, lng, 'Your Current Location');
          reverseGeocode(lat, lng);
          status.textContent = '✓ Location updated!';
        },
        (err) => {
          status.textContent = 'Unable to access browser location permissions.';
        },
        { enableHighAccuracy: true }
      );
    }

    async function searchAddress() {
      const addressInput = document.getElementById('addressInput');
      const status = document.getElementById('status');
      const query = addressInput.value.trim();

      if (!query) return;

      status.textContent = '🔍 Searching for address...';

      try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`);
        const data = await res.json();

        if (data && data.length > 0) {
          const lat = parseFloat(data[0].lat);
          const lng = parseFloat(data[0].lon);
          addressInput.value = data[0].display_name;
          updateMapLocation(lat, lng, data[0].display_name);
          status.textContent = '✓ Address pinpointed!';
        } else {
          status.textContent = '❌ Address not found. Try adding city/state.';
        }
      } catch (err) {
        status.textContent = 'Error connecting to geocoding service.';
      }
    }

    async function reverseGeocode(lat, lng) {
      try {
        const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`);
        const data = await res.json();
        if (data && data.display_name) {
          document.getElementById('addressInput').value = data.display_name;
        }
      } catch (err) {}
    }
  </script>
</body>
</html>
"""

# Render map component with explicit height
components.html(map_component_html, height=530)

st.markdown("---")

# Issue Form Controls
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
