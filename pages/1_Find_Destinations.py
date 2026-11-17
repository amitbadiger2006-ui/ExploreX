
import streamlit as st
import pandas as pd
import json
import math
from pathlib import Path
from urllib.parse import quote_plus

from recommender import places, recommend_places, get_states, get_categories


st.set_page_config(
    page_title="Explore Destinations | ExploreX",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Discover India")
st.write("Find your perfect destination with ExploreX!")
st.divider()


# LOAD DESTINATION IMAGES
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_FILE = BASE_DIR / "data" / "destination_images.json"

try:
    with open(IMAGE_FILE, "r", encoding="utf-8") as file:
        image_catalog = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    image_catalog = {}


# SIDEBAR FILTERS
st.sidebar.title("🔎 Find Your Destination")

search = st.sidebar.text_input(
    "Search destination",
    placeholder="Enter place name..."
)

available_states = ["All India"] + get_states()
available_categories = ["All"] + get_categories()

state = st.sidebar.selectbox(
    "Select State",
    available_states
)

selected_category = st.session_state.pop(
    "selected_category", "All"
)

if selected_category not in available_categories:
    selected_category = "All"

category = st.sidebar.selectbox(
    "Choose Category",
    available_categories,
    index=available_categories.index(selected_category)
)

budget = st.sidebar.slider(
    "Maximum Budget per Day (₹)",
    500, 10000, 3000, 500
)

rating = st.sidebar.slider(
    "Minimum Rating",
    0.0, 5.0, 4.0, 0.5
)


# RECOMMENDATIONS
results = recommend_places(
    state=state,
    category=category,
    budget=budget,
    min_rating=rating
)

if search:
    results = results[
        results["name"].str.contains(
            search,
            case=False,
            na=False,
            regex=False
        )
    ]

results = results.reset_index(drop=True)


# RESULTS
st.subheader("✨ Recommended Destinations")

st.write(f"Found **{len(results)} destinations** matching your preferences.")

if results.empty:
    st.warning("No destinations found. Try changing your filters.")

else:

    items_per_page = 12
    total_pages = math.ceil(len(results) / items_per_page)

    if "destination_page" not in st.session_state:
        st.session_state.destination_page = 1

    if st.session_state.destination_page > total_pages:
        st.session_state.destination_page = 1

    current_page = st.session_state.destination_page

    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page

    page_results = results.iloc[start_index:end_index]


    # DESTINATION CARDS
    for card_index, (_, row) in enumerate(page_results.iterrows()):

        name = str(row["name"])

        image_info = image_catalog.get(name, {})

        if isinstance(image_info, str):
            image_url = image_info
            image_source = ""
        else:
            image_url = image_info.get(
                "url",
                image_info.get("image_url", "")
            )
            image_source = image_info.get(
                "source",
                image_info.get("source_url", "")
            )

        with st.container(border=True):

            col1, col2 = st.columns([1, 2])

            with col1:

                if image_url:
                    st.image(image_url, use_container_width=True)
                else:
                    st.info("📍 Destination image unavailable")

                if image_source:
                    st.caption(f"Image source: {image_source}")

            with col2:

                st.subheader(f"📍 {name}")

                destination_state = row.get("state", "Not specified")
                destination_category = row.get("category", "Not specified")
                destination_rating = row.get("rating")
                destination_budget = row.get("budget_per_day")
                description = row.get(
                    "description",
                    "Explore this beautiful destination in India."
                )

                st.write(f"**State:** {destination_state}")
                st.write(f"**Category:** {destination_category}")

                if pd.notna(destination_rating):
                    st.write(f"⭐ **Rating:** {destination_rating}/5")
                else:
                    st.write("⭐ **Rating:** Not available")

                if pd.notna(destination_budget):
                    st.write(
                        f"💰 **Estimated Budget:** ₹{destination_budget:.0f}/day"
                    )
                else:
                    st.write("💰 **Estimated Budget:** Not available")

                st.write(f"📝 {description}")

                # RECOMMENDATION SCORE
                if (
                    "recommendation_score" in row.index
                    and pd.notna(row["recommendation_score"])
                ):
                    score = float(row["recommendation_score"])
                    score = max(0, min(100, score))

                    st.write(
                        f"🎯 **Recommendation Score: {score:.1f}/100**"
                    )
                    st.progress(score / 100)

                # GOOGLE MAPS
                maps_url = (
                    "https://www.google.com/maps/search/?api=1&query="
                    + quote_plus(
                        f"{name}, {destination_state}, India"
                    )
                )

                st.link_button(
                    "📍 View on Google Maps",
                    maps_url
                )

                # VIEW DETAILS BUTTON
                if st.button(
                    "🔍 View Destination Details",
                    key=f"details_{start_index + card_index}",
                    use_container_width=True
                ):
                    st.session_state["selected_destination"] = name
                    st.switch_page("pages/3_Destination_Details.py")


    # PAGINATION
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_page > 1:
            if st.button("⬅ Previous"):
                st.session_state.destination_page -= 1
                st.rerun()

    with col2:
        st.markdown(
            f"<center>Page <b>{current_page}</b> of <b>{total_pages}</b></center>",
            unsafe_allow_html=True
        )

    with col3:
        if current_page < total_pages:
            if st.button("Next ➡"):
                st.session_state.destination_page += 1
                st.rerun()


st.divider()
st.caption("🌍 ExploreX | Discover India, One Destination at a Time")
