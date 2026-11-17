import streamlit as st
import pandas as pd
from recommender import places, recommend_places, get_states, get_categories


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Trip Planner | ExploreX",
    page_icon="🧳",
    layout="wide"
)

st.title("🧳 Smart Trip Planner")
st.write("Plan your perfect Indian trip according to your budget and interests.")
st.divider()


# SIDEBAR INPUTS
st.sidebar.header("✈️ Plan Your Trip")

state = st.sidebar.selectbox(
    "Choose Destination State",
    ["All India"] + get_states()
)

category = st.sidebar.selectbox(
    "Choose Your Interest",
    ["All"] + get_categories()
)

total_budget = st.sidebar.slider(
    "Total Trip Budget (₹)",
    min_value=1000,
    max_value=100000,
    value=10000,
    step=1000
)

days = st.sidebar.slider(
    "Number of Travel Days",
    min_value=1,
    max_value=14,
    value=3
)

minimum_rating = st.sidebar.slider(
    "Minimum Destination Rating",
    min_value=0.0,
    max_value=5.0,
    value=3.5,
    step=0.5
)


# CALCULATE DAILY BUDGET
daily_budget = total_budget / days

st.subheader("📊 Your Trip Overview")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Budget", f"₹{total_budget:,}")
col2.metric("📅 Travel Days", days)
col3.metric("💵 Daily Budget", f"₹{daily_budget:,.0f}")


# GENERATE ITINERARY
if st.button("✨ Generate My Trip Plan", use_container_width=True):

    recommendations = recommend_places(
        state=state,
        category=category,
        budget=daily_budget,
        min_rating=minimum_rating
    )

    recommendations = recommendations.copy()

    if recommendations.empty:

        st.warning(
            "No destinations found for these preferences. "
            "Try increasing your budget or lowering your minimum rating."
        )

    else:

        # Select destinations for each day
        itinerary = recommendations.head(days).reset_index(drop=True)

        st.session_state["trip_itinerary"] = itinerary
        st.session_state["trip_days"] = days
        st.session_state["trip_budget"] = total_budget


# DISPLAY ITINERARY
if "trip_itinerary" in st.session_state:

    itinerary = st.session_state["trip_itinerary"]

    st.divider()
    st.success("🎉 Your trip itinerary is ready!")

    estimated_total = 0

    for index, row in itinerary.iterrows():

        day_number = index + 1

        destination_name = row["name"]
        destination_state = row["state"]
        destination_category = row["category"]

        rating = row.get("rating")
        budget = row.get("budget_per_day")

        st.markdown(f"### 📅 Day {day_number}")

        with st.container(border=True):

            st.subheader(f"📍 {destination_name}")

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**State:** {destination_state}")
                st.write(f"**Category:** {destination_category}")

                if pd.notna(rating):
                    st.write(f"⭐ **Rating:** {rating}/5")
                else:
                    st.write("⭐ **Rating:** Not available")

            with col2:

                if pd.notna(budget):
                    daily_cost = float(budget)
                    estimated_total += daily_cost

                    st.write(
                        f"💰 **Estimated Daily Cost:** ₹{daily_cost:,.0f}"
                    )
                else:
                    st.write("💰 **Estimated Daily Cost:** Not available")

                score = row.get("recommendation_score")

                if pd.notna(score):
                    st.write(f"🎯 **Recommendation Score:** {score:.1f}/100")

            if st.button(
                "🔍 View Destination Details",
                key=f"trip_details_{index}"
            ):
                st.session_state["selected_destination"] = destination_name
                st.switch_page("pages/3_Destination_Details.py")

        st.write("")


    # TRIP SUMMARY
    st.divider()

    st.subheader("💰 Estimated Trip Summary")

    col1, col2 = st.columns(2)

    col1.metric(
        "Estimated Destination Costs",
        f"₹{estimated_total:,.0f}"
    )

    col2.metric(
        "Your Total Budget",
        f"₹{st.session_state['trip_budget']:,}"
    )

    st.caption(
        "Note: These are approximate destination budget estimates. "
        "Actual travel, accommodation and food costs may vary."
    )

    if estimated_total > st.session_state["trip_budget"]:
        st.warning(
            "The estimated destination costs exceed your selected budget."
        )
    else:
        st.success("Your estimated destination costs are within your budget!")


# FOOTER
st.divider()

st.caption("🌍 ExploreX | Discover India, One Destination at a Time")