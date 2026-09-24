import streamlit as st
import pandas as pd

from recommendation_engine import recommend_restaurants
from llm_handler import generate_explanation


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Restaurant Selection Advisor",
    page_icon="🍽️",
    layout="wide"
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🍽️ AI Restaurant Selection Advisor")

st.markdown(
    """
    ### Find restaurants that match your preferences

    This application combines **LangChain + Gemini + Fuzzy Logic**
    to understand your restaurant request and rank suitable restaurants.

    If Gemini is unavailable or its quota is exceeded, the application
    automatically switches to a **local fallback preference parser**,
    so recommendations remain available.
    """
)

st.divider()


# ---------------------------------------------------------
# User Input
# ---------------------------------------------------------

st.subheader("📝 Tell us what you are looking for")

user_query = st.text_area(
    "Restaurant Request",
    placeholder=(
        "Example: I want a cheap Indian restaurant nearby "
        "with a good rating for a family dinner."
    ),
    height=100
)


# ---------------------------------------------------------
# Find Restaurants Button
# ---------------------------------------------------------

if st.button("🔍 Find Restaurants", use_container_width=True):

    if not user_query.strip():

        st.warning(
            "Please enter a restaurant request first."
        )

    else:

        with st.spinner(
            "🤖 AI is analyzing your preferences..."
        ):

            try:

                # -------------------------------------------------
                # Recommendation Engine
                # -------------------------------------------------

                recommendations, preferences = recommend_restaurants(
                    user_query
                )


                # -------------------------------------------------
                # Detect Gemini / Fallback
                # -------------------------------------------------

                source = preferences.get(
                    "_source",
                    "Gemini"
                )


                if source == "Local Fallback":

                    st.warning(
                        "⚠️ Gemini is currently unavailable. "
                        "The application switched to the built-in "
                        "fallback parser. The same fuzzy recommendation "
                        "system is being used."
                    )

                else:

                    st.success(
                        "🤖 Preferences successfully extracted "
                        "using Gemini + LangChain."
                    )


                # -------------------------------------------------
                # Extracted Preferences
                # -------------------------------------------------

                st.subheader("🧠 AI-Extracted Preferences")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Cuisine",
                        preferences.get(
                            "cuisine",
                            "Any"
                        )
                    )

                with col2:
                    st.metric(
                        "Budget",
                        preferences.get(
                            "budget",
                            "Moderate"
                        ).title()
                    )

                with col3:
                    st.metric(
                        "Distance",
                        preferences.get(
                            "distance",
                            "Moderate"
                        ).title()
                    )

                with col4:
                    st.metric(
                        "Rating",
                        preferences.get(
                            "rating",
                            "Average"
                        ).title()
                    )


                # -------------------------------------------------
                # Occasion
                # -------------------------------------------------

                occasion = preferences.get(
                    "occasion",
                    "general"
                )

                st.info(
                    f"🎯 **Occasion:** {occasion.title()}"
                )


                st.divider()


                # -------------------------------------------------
                # Recommendations
                # -------------------------------------------------

                st.subheader(
                    "🏆 Top Restaurant Recommendations"
                )

                if recommendations.empty:

                    st.warning(
                        "No restaurants were found for this request."
                    )

                else:

                    display_columns = [
                        "Restaurant",
                        "Cuisine",
                        "Price",
                        "Distance",
                        "Rating",
                        "Suitability Score"
                    ]

                    display_df = recommendations[
                        display_columns
                    ].copy()


                    # Format values for display

                    display_df["Price"] = display_df[
                        "Price"
                    ].apply(
                        lambda x: f"₹{x:,.0f}"
                    )

                    display_df["Distance"] = display_df[
                        "Distance"
                    ].apply(
                        lambda x: f"{x:.1f} km"
                    )

                    display_df["Rating"] = display_df[
                        "Rating"
                    ].apply(
                        lambda x: f"{x:.1f} ⭐"
                    )

                    display_df["Suitability Score"] = display_df[
                        "Suitability Score"
                    ].apply(
                        lambda x: f"{x:.2f}"
                    )


                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True
                    )


                    # -------------------------------------------------
                    # Restaurant Cards
                    # -------------------------------------------------

                    st.subheader(
                        "🍴 Restaurant Details"
                    )

                    for index, (_, restaurant) in enumerate(
                        recommendations.iterrows()
                    ):

                        with st.container(
                            border=True
                        ):

                            col1, col2 = st.columns(
                                [3, 1]
                            )

                            with col1:

                                st.markdown(
                                    f"### {restaurant['Restaurant']}"
                                )

                                st.write(
                                    f"**Cuisine:** "
                                    f"{restaurant['Cuisine']}"
                                )

                                st.write(
                                    f"**Price:** "
                                    f"₹{restaurant['Price']:,.0f}"
                                )

                                st.write(
                                    f"**Distance:** "
                                    f"{restaurant['Distance']:.1f} km"
                                )

                                st.write(
                                    f"**Rating:** "
                                    f"{restaurant['Rating']:.1f} ⭐"
                                )

                            with col2:

                                st.metric(
                                    "Suitability",
                                    f"{restaurant['Suitability Score']:.2f}"
                                )


                    # -------------------------------------------------
                    # Suitability Chart
                    # -------------------------------------------------

                    st.subheader(
                        "📊 Suitability Scores"
                    )

                    chart_data = recommendations[
                        [
                            "Restaurant",
                            "Suitability Score"
                        ]
                    ].copy()

                    chart_data = chart_data.set_index(
                        "Restaurant"
                    )

                    st.bar_chart(
                        chart_data[
                            "Suitability Score"
                        ]
                    )


                    # -------------------------------------------------
                    # AI Explanation
                    # -------------------------------------------------

                    st.subheader(
                        "💡 Why These Restaurants?"
                    )

                    with st.spinner(
                        "Generating recommendation explanation..."
                    ):

                        try:

                            explanation = generate_explanation(
                                user_query,
                                preferences,
                                recommendations
                            )

                            st.write(
                                explanation
                            )

                        except Exception:

                            # Extra safety fallback.
                            # Recommendations are already available,
                            # so an explanation failure should never
                            # break the application.

                            top_restaurant = recommendations.iloc[0]

                            st.write(
                                f"These restaurants were ranked according "
                                f"to how well their price, distance, and "
                                f"rating match your preferences. "
                                f"{top_restaurant['Restaurant']} has a "
                                f"suitability score of "
                                f"{top_restaurant['Suitability Score']:.2f}."
                            )


                # -------------------------------------------------
                # How the System Works
                # -------------------------------------------------

                st.divider()

                st.subheader(
                    "🧠 How This AI System Works"
                )

                step1, step2, step3, step4, step5 = st.columns(5)


                with step1:

                    st.markdown(
                        """
                        **1️⃣ Natural Language**

                        Your request is analyzed using
                        Gemini through LangChain.
                        """
                    )


                with step2:

                    st.markdown(
                        """
                        **2️⃣ Preference Matching**

                        Price, distance and rating
                        are converted into match
                        values from 0–10.
                        """
                    )


                with step3:

                    st.markdown(
                        """
                        **3️⃣ Fuzzy Inference**

                        Match values are fuzzified
                        into Poor, Average and Good.
                        """
                    )


                with step4:

                    st.markdown(
                        """
                        **4️⃣ Fuzzy Rules**

                        Fuzzy rules evaluate the
                        restaurant preferences.
                        """
                    )


                with step5:

                    st.markdown(
                        """
                        **5️⃣ Final Ranking**

                        Defuzzification produces a
                        0–100 suitability score.
                        """
                    )


                # -------------------------------------------------
                # Fallback Information
                # -------------------------------------------------

                if source == "Local Fallback":

                    st.divider()

                    st.subheader(
                        "🔄 Fallback Mode"
                    )

                    st.markdown(
                        """
                        Gemini was unavailable, so the application used
                        a local rule-based language parser to extract the
                        basic restaurant preferences.

                        The **restaurant ranking itself is still performed
                        by the same fuzzy inference system**, so the
                        recommendation process remains unchanged.
                        """
                    )


            except Exception as error:

                # -------------------------------------------------
                # Final Application-Level Error
                # -------------------------------------------------

                st.error(
                    "Something went wrong while generating "
                    "the recommendations."
                )

                st.exception(error)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "🍽️ AI Restaurant Selection Advisor | "
    "LangChain + Gemini + Fuzzy Logic"
)