import pandas as pd


# Load tourist destination data
def load_data():

    data = pd.read_csv("data/tourist_places.csv")

    data["state"] = data["state"].fillna("Not specified")

    data["budget_per_day"] = pd.to_numeric(
        data["budget_per_day"], errors="coerce"
    )

    data["rating"] = pd.to_numeric(
        data["rating"], errors="coerce"
    )

    return data


places = load_data()


# Get all destinations
def get_all_places():
    return places.copy()


# Get available states
def get_states():

    states = places["state"].dropna().unique()

    return sorted(states)


# Get available categories
def get_categories():

    categories = places["category"].dropna().unique()

    return sorted(categories)


# Personalized recommendation system
def recommend_places(
    state="All India",
    category="All",
    budget=10000,
    min_rating=0
):

    results = places.copy()

    # Filter by state
    if state != "All India":

        results = results[
            results["state"] == state
        ]

    # Filter by category
    if category != "All":

        results = results[
            results["category"] == category
        ]

    # Filter by budget
    results = results[
        results["budget_per_day"].isna()
        |
        (results["budget_per_day"] <= budget)
    ]

    # Filter by minimum rating
    results = results[
        results["rating"].isna()
        |
        (results["rating"] >= min_rating)
    ]

    # Calculate recommendation score
    def calculate_score(row):

        # Rating score (70% weight)
        if pd.notna(row["rating"]):

            rating_score = (
                row["rating"] / 5
            ) * 100

        else:

            rating_score = 0

        # Budget score (30% weight)
        if pd.notna(row["budget_per_day"]):

            budget_score = max(
                0,
                100 - (
                    row["budget_per_day"] / budget
                ) * 100
            )

        else:

            budget_score = 50

        # Final personalized score
        final_score = (
            rating_score * 0.7
            +
            budget_score * 0.3
        )

        return round(final_score, 2)

    results["recommendation_score"] = results.apply(
        calculate_score,
        axis=1
    )

    # Sort by recommendation score
    results = results.sort_values(
        by="recommendation_score",
        ascending=False
    )

    return results


# Search destinations by name
def search_place(name):

    results = places[
        places["name"].str.contains(
            name,
            case=False,
            na=False
        )
    ]

    return results


# Get total number of destinations
def get_total_destinations():

    return len(places)