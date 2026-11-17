
import streamlit as st

st.set_page_config(
    page_title="ExploreX | Tourist Recommender",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

#MainMenu, footer {
    visibility: hidden;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 5px 25px 5px;
}

.logo {
    font-size: 27px;
    font-weight: 800;
    color: #12372a;
}

.logo span {
    color: #16a36a;
}

.tagline {
    color: #64748b;
    font-size: 13px;
    letter-spacing: 2px;
}

/* Hero */
.hero {
    padding: 55px;
    border-radius: 22px;
    min-height: 340px;
    background:
        linear-gradient(90deg, rgba(9,30,25,0.92),
        rgba(9,30,25,0.25)),
        url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1600&q=85");
    background-size: cover;
    background-position: center;
    color: white;
}

.hero-tag {
    color: #b8f3d2;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 3px;
}

.hero h1 {
    color: white;
    font-size: 48px;
    line-height: 1.15;
    max-width: 650px;
}

.hero p {
    color: #e2e8f0;
    font-size: 17px;
    max-width: 570px;
    line-height: 1.7;
}

/* Buttons */
div.st-key-explore_button button,
div.st-key-nature_button button,
div.st-key-heritage_button button,
div.st-key-adventure_button button {
    background-color: #16a36a !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
    padding: 10px 15px !important;
    width: 100%;
}

div.st-key-explore_button button:hover,
div.st-key-nature_button button:hover,
div.st-key-heritage_button button:hover,
div.st-key-adventure_button button:hover {
    background-color: #128653 !important;
    color: white !important;
}

/* Section headings */
.section-title {
    font-size: 29px;
    font-weight: 800;
    color: #12372a;
    margin-top: 38px;
}

.section-subtitle {
    color: #64748b;
    font-size: 15px;
    margin-bottom: 20px;
}

/* Category cards */
.category-card {
    height: 210px;
    border-radius: 16px;
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 20px;
    color: white;
    overflow: hidden;
    box-sizing: border-box;
}

.category-card h3 {
    color: white;
    font-size: 23px;
    margin-bottom: 5px;
}

.category-card p {
    color: #f1f5f9;
    font-size: 13px;
}

/* Information cards */
.info-card {
    background: white;
    padding: 23px;
    border-radius: 15px;
    min-height: 145px;
    border: 1px solid #e8edf1;
}

.info-card h3 {
    color: #12372a;
    font-size: 19px;
}

.info-card p {
    color: #64748b;
    font-size: 14px;
}

/* Footer */
.footer-text {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    padding: 35px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)


# Navigation bar
st.markdown("""
<div class="navbar">
    <div class="logo">Explore<span>X</span> 🌍</div>
    <div class="tagline">TRAVEL • EXPLORE • DISCOVER</div>
</div>
""", unsafe_allow_html=True)


# Hero section
st.markdown("""
<div class="hero">
    <div class="hero-tag">YOUR NEXT ADVENTURE STARTS HERE</div>
    <h1>Discover Places.<br>Experience Life.</h1>
    <p>
        Find amazing tourist destinations based on your interests,
        budget and travel preferences. Let us help you plan your
        next unforgettable journey.
    </p>
</div>
""", unsafe_allow_html=True)

st.button(
    "🌍 Explore Destinations →",
    key="explore_button",
    on_click=lambda: st.switch_page("pages/1_Find_Destinations.py")
)


# Explore section
st.markdown("""
<div class="section-title">Explore Your Interests</div>
<div class="section-subtitle">
    What kind of experience are you looking for?
</div>
""", unsafe_allow_html=True)


# Category cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="category-card" style="
    background-image:
    linear-gradient(0deg, rgba(0,0,0,0.8), transparent),
    url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800');
    ">
    <h3>🌿 Nature</h3>
    <p>Explore mountains, forests and waterfalls.</p>
    </div>
    """, unsafe_allow_html=True)

    st.button(
        "Explore Nature →",
        key="nature_button",
        on_click=lambda: (
            st.session_state.update({"selected_category": "Nature"}),
            st.switch_page("pages/1_Find_Destinations.py")
        )
    )


with col2:
    st.markdown("""
    <div class="category-card" style="
    background-image:
    linear-gradient(0deg, rgba(0,0,0,0.8), transparent),
    url('https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800');
    ">
    <h3>🏛️ Heritage</h3>
    <p>Discover historical places and architecture.</p>
    </div>
    """, unsafe_allow_html=True)

    st.button(
        "Explore Heritage →",
        key="heritage_button",
        on_click=lambda: (
            st.session_state.update({"selected_category": "Heritage"}),
            st.switch_page("pages/1_Find_Destinations.py")
        )
    )


with col3:
    st.markdown("""
    <div class="category-card" style="
    background-image:
    linear-gradient(0deg, rgba(0,0,0,0.8), transparent),
    url('https://images.unsplash.com/photo-1530789253388-582c481c54b0?w=800');
    ">
    <h3>🏕️ Adventure</h3>
    <p>Experience exciting outdoor activities.</p>
    </div>
    """, unsafe_allow_html=True)

    st.button(
        "Explore Adventure →",
        key="adventure_button",
        on_click=lambda: (
            st.session_state.update({"selected_category": "Adventure"}),
            st.switch_page("pages/1_Find_Destinations.py")
        )
    )


# Why choose us section
st.markdown("""
<div class="section-title">Your Journey, Made Easier</div>
<div class="section-subtitle">
    Everything you need to discover your next destination.
</div>
""", unsafe_allow_html=True)


c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="info-card">
    <h3>🎯 Smart Recommendations</h3>
    <p>Discover destinations matching your budget and personal interests.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="info-card">
    <h3>🗺️ Interactive Maps</h3>
    <p>Explore destinations and find their exact geographical locations.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="info-card">
    <h3>💰 Budget Friendly</h3>
    <p>Find amazing places that match your travel budget.</p>
    </div>
    """, unsafe_allow_html=True)


# Footer
st.markdown("""
<div class="footer-text">
© 2026 ExploreX | Tourist Place Recommender System
<br>
Discover more. Travel further. 🌍
</div>
""", unsafe_allow_html=True)
