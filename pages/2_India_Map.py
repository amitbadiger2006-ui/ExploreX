import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from recommender import places, get_states, get_categories
import pandas as pd
import html


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="ExploreX | India Map",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Explore India")
st.write("Discover amazing tourist destinations across India.")
st.divider()


# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("🗺️ Map Filters")

state = st.sidebar.selectbox(
    "Select State",
    ["All India"] + get_states()
)

category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + get_categories()
)


# ---------------- FILTER DESTINATIONS ----------------

filtered_places = places.copy()

if state != "All India":
    filtered_places = filtered_places[
        filtered_places["state"] == state
    ]

if category != "All":
    filtered_places = filtered_places[
        filtered_places["category"] == category
    ]

filtered_places["latitude"] = pd.to_numeric(
    filtered_places["latitude"], errors="coerce"
)

filtered_places["longitude"] = pd.to_numeric(
    filtered_places["longitude"], errors="coerce"
)

filtered_places = filtered_places.dropna(
    subset=["latitude", "longitude"]
)


# ---------------- DESTINATION COUNT ----------------

col1, col2, col3 = st.columns(3)

col1.metric("📍 Destinations on Map", len(filtered_places))
col2.metric("🗺️ Selected State", state)
col3.metric("🎯 Selected Category", category)


# ---------------- CREATE MAP ----------------

india_map = folium.Map(
    location=[22.5, 82.0],
    zoom_start=5,
    tiles="OpenStreetMap",
    control_scale=True
)

marker_cluster = MarkerCluster().add_to(india_map)


# ---------------- CATEGORY COLOURS ----------------

category_colors = {
    "Nature": "green",
    "Heritage": "blue",
    "Adventure": "red"
}


# ---------------- ADD MARKERS ----------------

for _, row in filtered_places.iterrows():

    name = html.escape(str(row["name"]))
    state_name = html.escape(str(row["state"]))
    category_name = html.escape(str(row["category"]))

    latitude = float(row["latitude"])
    longitude = float(row["longitude"])

    description = row.get("description", "")

    if pd.isna(description):
        description = "Explore this beautiful destination in India."

    description = html.escape(str(description))

    rating = row.get("rating")

    if pd.notna(rating):
        rating = f"{float(rating):.1f}/5"
    else:
        rating = "Not available"

    budget = row.get("budget_per_day")

    if pd.notna(budget):
        budget = f"₹{float(budget):,.0f}/day"
    else:
        budget = "Not available"

    score = row.get("recommendation_score")

    if pd.notna(score):
        score = f"{float(score):.1f}/100"
    else:
        score = "Not available"

    google_maps_link = (
        f"https://www.google.com/maps/search/?api=1"
        f"&query={latitude},{longitude}"
    )

    marker_color = category_colors.get(
        str(row["category"]),
        "purple"
    )

    popup_html = f"""
    <div style="width:230px;font-family:Arial;line-height:1.6;">

        <h3 style="color:#159b65;">📍 {name}</h3>

        <b>State:</b> {state_name}<br>
        <b>Category:</b> {category_name}<br>
        <b>Rating:</b> ⭐ {rating}<br>
        <b>Daily Budget:</b> {budget}<br>
        <b>Recommendation Score:</b> 🎯 {score}<br>

        <hr>

        <p>{description}</p>

        <a href="{google_maps_link}" target="_blank">
            Open in Google Maps
        </a>

    </div>
    """

    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=name,
        icon=folium.Icon(
            color=marker_color,
            icon="info-sign"
        )
    ).add_to(marker_cluster)


# ---------------- MAP LEGEND ----------------

st.subheader("📍 Tourist Destinations Across India")

st.markdown("""
🟢 **Nature** &nbsp;&nbsp;
🔵 **Heritage** &nbsp;&nbsp;
🔴 **Adventure** &nbsp;&nbsp;
🟣 **Other Categories**
""")

st.write(
    "Click any marker to view destination details "
    "and access its Google Maps location."
)


# ---------------- DISPLAY INTERACTIVE MAP ----------------

if not filtered_places.empty:

    bounds = [
        [float(row["latitude"]), float(row["longitude"])]
        for _, row in filtered_places.iterrows()
    ]

    india_map.fit_bounds(bounds, padding=(30, 30))

    st_folium(
        india_map,
        width=1200,
        height=650,
        key="explorex_map",
        returned_objects=[]
    )

else:
    st.warning("No destinations available for the selected filters.")


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "🌍 ExploreX | Discover India, One Destination at a Time"
)

st.caption(
    "Map data © OpenStreetMap contributors."
)