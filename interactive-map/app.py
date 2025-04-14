import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="🗺️ Interactive Map", layout="wide")

st.title("🗺️ Interactive Map with Streamlit + Folium")

st.markdown("Use the form below to add markers and generate your interactive map.")

# Sidebar input
with st.sidebar:
    st.header("📍 Add Marker Details")
    lat = st.number_input("Latitude", value=24.8607)
    lon = st.number_input("Longitude", value=67.0011)
    popup = st.text_input("Popup Text", value="My Location")
    zoom = st.slider("Zoom Level", 1, 20, 12)
    add_marker = st.button("Add Marker")

# Session state to hold markers
if "markers" not in st.session_state:
    st.session_state.markers = []

# Add marker if button pressed
if add_marker:
    st.session_state.markers.append({
        "lat": lat,
        "lon": lon,
        "popup": popup
    })

# Create folium map
m = folium.Map(location=[lat, lon], zoom_start=zoom)

# Add markers to map
for marker in st.session_state.markers:
    folium.Marker([marker["lat"], marker["lon"]], popup=marker["popup"]).add_to(m)

# Show the map
st_data = st_folium(m, width=800, height=600)

# Reset button
# Reset button
if st.button("🧹 Clear All Markers"):
    st.session_state.markers = []
    st.rerun()
