
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
from pathlib import Path
from urllib.parse import quote_plus

from recommender import places


st.set_page_config(
    page_title="Destination Details | ExploreX",
    page_icon="📍",
    layout="wide"
)

st.title("📍 Explore Destination Details")
st.write("Discover everything about your favourite tourist destination.")
st.divider()


# LOAD IMAGES
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_FILE = BASE_DIR / "data" / "destination_images.json"

try:
    with open(IMAGE_FILE, "r", encoding="utf-8") as file:
        image_catalog = json.load(file)
except Exception:
    image_catalog = {}


# DESTINATION SELECTION
destination_names = sorted(
    places["name"].dropna().unique().tolist()
)

default_destination = st.session_state.pop(
    "selected_destination",
    destination_names[0]
)

if default_destination not in destination_names:
    default_destination = destination_names[0]

selected_destination = st.selectbox(
    "🔎 Search or select a destination",
    destination_names,
    index=destination_names.index(default_destination)
)


# GET DESTINATION DATA
destination = places[
    places["name"] == selected_destination
].iloc[0]


# IMAGE
image_info = image_catalog.get(selected_destination, {})

if isinstance(image_info, str):
    image_url = image_info
else:
    image_url = image_info.get(
        "url",
        image_info.get("image_url", "")
    )


# DESTINATION INFORMATION
col1, col2 = st.columns([1.2, 1])

with col1:
    if image_url:
        st.image(image_url, use_container_width=True)
    else:
        st.info("📸 Image not available for this destination.")

with col2:

    st.subheader(f"🌍 {selected_destination}")

    st.write(f"**State:** {destination['state']}")
    st.write(f"**Category:** {destination['category']}")

    if pd.notna(destination["rating"]):
        st.write(f"⭐ **Rating:** {destination['rating']}/5")
    else:
        st.write("⭐ **Rating:** Not available")

    if pd.notna(destination["budget_per_day"]):
        st.write(
            f"💰 **Estimated Budget:** "
            f"₹{destination['budget_per_day']:,.0f}/day"
        )
    else:
        st.write("💰 **Estimated Budget:** Not available")

    if (
        "recommendation_score" in destination.index
        and pd.notna(destination["recommendation_score"])
    ):
        score = float(destination["recommendation_score"])
        st.write(f"🎯 **Recommendation Score:** {score:.1f}/100")
        st.progress(max(0, min(100, score)) / 100)


# DESCRIPTION
st.divider()
st.subheader("📝 About This Destination")

description = destination.get("description", "")

if pd.notna(description) and str(description).strip():
    st.write(description)
else:
    st.write(
        f"Explore {selected_destination}, "
        "a beautiful tourist destination in India."
    )


# LOCATION MAP
st.divider()
st.subheader("🗺️ Destination Location")

latitude = pd.to_numeric(
    pd.Series([destination["latitude"]]),
    errors="coerce"
).iloc[0]

longitude = pd.to_numeric(
    pd.Series([destination["longitude"]]),
    errors="coerce"
).iloc[0]

if pd.notna(latitude) and pd.notna(longitude):

    destination_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    folium.Marker(
        [latitude, longitude],
        tooltip=selected_destination,
        popup=selected_destination,
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(destination_map)

    st_folium(
        destination_map,
        width=None,
        height=400,
        key="destination_details_map",
        returned_objects=[]
    )

    maps_url = (
        "https://www.google.com/maps/search/?api=1&query="
        + quote_plus(f"{latitude},{longitude}")
    )

    st.link_button(
        "📍 Navigate with Google Maps",
        maps_url
    )

else:
    st.warning("Location coordinates are not available.")


st.divider()
st.caption("🌍 ExploreX | Discover India, One Destination at a Time")
