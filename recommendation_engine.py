import json
import pandas as pd

from llm_handler import extract_preferences
from fuzzy_logic import calculate_suitability


# ---------------------------------------------------------
# LOAD RESTAURANT DATA
# ---------------------------------------------------------

restaurants = pd.read_csv("restaurants.csv")


# ---------------------------------------------------------
# USER PREFERENCE TARGETS
# ---------------------------------------------------------

budget_targets = {
    "cheap": 700,
    "moderate": 1200,
    "expensive": 2000
}

distance_targets = {
    "near": 2,
    "moderate": 5,
    "far": 8
}

rating_targets = {
    "low": 3.0,
    "average": 3.8,
    "excellent": 4.5
}


# ---------------------------------------------------------
# MATCHING FUNCTIONS
# ---------------------------------------------------------

def calculate_match(
    restaurant_value,
    target_value,
    tolerance
):
    """
    Convert the difference between a restaurant value
    and the user's preferred value into a 0-10 match score.

    10 = excellent match
    0 = very poor match
    """

    difference = abs(
        restaurant_value - target_value
    )

    match = 10 - (
        difference / tolerance * 10
    )

    return max(0, min(10, match))


# ---------------------------------------------------------
# RECOMMENDATION ENGINE
# ---------------------------------------------------------

def recommend_restaurants(user_query):

    # LLM understands the user's natural-language request
    preferences_text = extract_preferences(user_query)

    preferences = json.loads(preferences_text)

    cuisine = preferences.get("cuisine", "any")
    budget = preferences.get("budget", "moderate")
    distance = preferences.get("distance", "moderate")
    rating = preferences.get("rating", "average")

    # Convert language preferences into numerical targets
    target_price = budget_targets.get(
        budget,
        budget_targets["moderate"]
    )

    target_distance = distance_targets.get(
        distance,
        distance_targets["moderate"]
    )

    target_rating = rating_targets.get(
        rating,
        rating_targets["average"]
    )

    # -----------------------------------------------------
    # CUISINE FILTER
    # -----------------------------------------------------

    if cuisine.lower() != "any":
        filtered = restaurants[
            restaurants["Cuisine"].str.lower()
            == cuisine.lower()
        ].copy()
    else:
        filtered = restaurants.copy()

    # If no exact cuisine exists, use all restaurants
    if filtered.empty:
        filtered = restaurants.copy()

    # -----------------------------------------------------
    # FUZZY SCORING
    # -----------------------------------------------------

    scores = []

    for _, restaurant in filtered.iterrows():

        price_match = calculate_match(
            restaurant["Price"],
            target_price,
            1000
        )

        distance_match = calculate_match(
            restaurant["Distance"],
            target_distance,
            5
        )

        rating_match = calculate_match(
            restaurant["Rating"],
            target_rating,
            1.5
        )

        score = calculate_suitability(
            price_match,
            distance_match,
            rating_match
        )

        scores.append(score)

    filtered["Suitability Score"] = scores

    # Round the scores for cleaner UI
    filtered["Suitability Score"] = (
        filtered["Suitability Score"]
        .round(2)
    )

    # Highest suitability first
    filtered = filtered.sort_values(
        by="Suitability Score",
        ascending=False
    )

    return filtered.head(5), preferences


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    query = (
        "I want a cheap Chinese restaurant nearby "
        "with a good rating for a family dinner."
    )

    recommendations, preferences = (
        recommend_restaurants(query)
    )

    print("\nExtracted Preferences:")
    print(preferences)

    print("\nTop Restaurant Recommendations:")

    print(
        recommendations[
            [
                "Restaurant",
                "Cuisine",
                "Price",
                "Distance",
                "Rating",
                "Suitability Score"
            ]
        ].to_string(index=False)
    )