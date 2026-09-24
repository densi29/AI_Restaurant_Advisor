import os
import json
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


# ---------------------------------------------------------
# Gemini setup
# ---------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


preference_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a restaurant preference extraction assistant.

Extract the user's restaurant preferences and return ONLY valid JSON.

Required fields:
- cuisine
- budget
- distance
- rating
- occasion

Allowed values:

budget:
cheap, moderate, expensive

distance:
near, moderate, far

rating:
low, average, excellent

If something is not mentioned, use:
cuisine = any
budget = moderate
distance = moderate
rating = average
occasion = general

Examples:
"cheap" -> budget = cheap
"expensive" -> budget = expensive
"nearby" -> distance = near
"far away" -> distance = far
"good rating" -> rating = excellent
"highly rated" -> rating = excellent
"average rating" -> rating = average

Return only JSON.
"""
    ),
    ("human", "{user_query}")
])

preference_chain = preference_prompt | llm


# ---------------------------------------------------------
# Local fallback parser
# ---------------------------------------------------------
# This is used ONLY when Gemini is unavailable.
# It produces the same preference format as Gemini.
# ---------------------------------------------------------

def local_fallback_preferences(user_query):
    text = user_query.lower()

    # ---------- Cuisine ----------
    cuisine = "any"

    cuisines = [
        "indian",
        "south indian",
        "chinese",
        "italian",
        "mexican",
        "fast food",
        "healthy"
    ]

    for item in cuisines:
        if item in text:
            cuisine = item.title()
            break

    # ---------- Budget ----------
    if any(word in text for word in [
        "cheap",
        "budget",
        "low cost",
        "affordable",
        "inexpensive"
    ]):
        budget = "cheap"

    elif any(word in text for word in [
        "expensive",
        "premium",
        "luxury",
        "high end"
    ]):
        budget = "expensive"

    else:
        budget = "moderate"

    # ---------- Distance ----------
    if any(word in text for word in [
        "near",
        "nearby",
        "close",
        "closest",
        "walking distance"
    ]):
        distance = "near"

    elif any(word in text for word in [
        "far",
        "far away",
        "distant"
    ]):
        distance = "far"

    else:
        distance = "moderate"

    # ---------- Rating ----------
    if any(word in text for word in [
        "excellent",
        "best rated",
        "highly rated",
        "great rating",
        "good rating",
        "good ratings",
        "top rated"
    ]):
        rating = "excellent"

    elif any(word in text for word in [
        "low rating",
        "poor rating",
        "low rated"
    ]):
        rating = "low"

    else:
        rating = "average"

    # ---------- Occasion ----------
    occasion = "general"

    occasion_patterns = {
        "family dinner": [
            "family dinner",
            "family",
            "with family"
        ],
        "date": [
            "date",
            "romantic",
            "couple"
        ],
        "business": [
            "business",
            "meeting",
            "client"
        ],
        "birthday": [
            "birthday",
            "birthday party"
        ],
        "lunch": [
            "lunch"
        ],
        "dinner": [
            "dinner"
        ]
    }

    for occasion_name, patterns in occasion_patterns.items():
        if any(pattern in text for pattern in patterns):
            occasion = occasion_name
            break

    return {
        "cuisine": cuisine,
        "budget": budget,
        "distance": distance,
        "rating": rating,
        "occasion": occasion
    }


# ---------------------------------------------------------
# Extract preferences
# ---------------------------------------------------------

def extract_preferences(user_query):

    try:
        # Primary method: Gemini through LangChain
        response = preference_chain.invoke({
            "user_query": user_query
        })

        content = response.content

        if isinstance(content, list):
            content = "".join(
                item.get("text", str(item))
                if isinstance(item, dict)
                else str(item)
                for item in content
            )

        content = str(content).strip()

        # Remove markdown code fences if Gemini adds them
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        # Extract JSON object
        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("Gemini did not return valid JSON.")

        json_text = content[start:end + 1]

        preferences = json.loads(json_text)

        # Make sure all fields exist
        preferences.setdefault("cuisine", "any")
        preferences.setdefault("budget", "moderate")
        preferences.setdefault("distance", "moderate")
        preferences.setdefault("rating", "average")
        preferences.setdefault("occasion", "general")

        # Mark source for UI/debugging
        preferences["_source"] = "Gemini"

        return json.dumps(preferences)

    except Exception as error:

        # Gemini failed.
        # Use local fallback instead of stopping the application.

        print("\nGemini unavailable.")
        print("Using local fallback preference parser.")
        print("Reason:", error)

        preferences = local_fallback_preferences(user_query)

        preferences["_source"] = "Local Fallback"

        return json.dumps(preferences)


# ---------------------------------------------------------
# AI explanation
# ---------------------------------------------------------

explanation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a restaurant recommendation assistant.

Explain why the displayed restaurants match the user's request.

Use ONLY the information provided in:
- user request
- extracted preferences
- recommendation table

Do not invent restaurant information.

Keep the explanation concise and natural.

Do not claim that one restaurant is objectively the best.
"""
    ),
    (
        "human",
        """
User request:
{user_query}

Extracted preferences:
{preferences}

Recommendations:
{recommendations}
"""
    )
])

explanation_chain = explanation_prompt | llm


def generate_local_explanation(
    user_query,
    preferences,
    recommendations
):
    """
    Fallback explanation when Gemini is unavailable.
    """

    rows = recommendations.to_dict("records")

    if not rows:
        return "No matching restaurants were found."

    top = rows[0]

    cuisine = preferences.get("cuisine", "any")
    budget = preferences.get("budget", "moderate")
    distance = preferences.get("distance", "moderate")
    rating = preferences.get("rating", "average")

    cuisine_text = (
        f"{cuisine} cuisine"
        if cuisine != "any"
        else "the requested cuisine"
    )

    return (
        f"Based on your request, the system looked for {budget}-priced "
        f"{cuisine_text} restaurants that are {distance} in distance "
        f"with an {rating} rating preference. "
        f"The recommendations were ranked using fuzzy matching of "
        f"price, distance, and rating. "
        f"{top['Restaurant']} received a suitability score of "
        f"{top['Suitability Score']}, making it one of the closest "
        f"matches to the requested preferences."
    )


def generate_explanation(
    user_query,
    preferences,
    recommendations
):

    try:

        response = explanation_chain.invoke({
            "user_query": user_query,
            "preferences": json.dumps(preferences),
            "recommendations": recommendations[
                [
                    "Restaurant",
                    "Cuisine",
                    "Price",
                    "Distance",
                    "Rating",
                    "Suitability Score"
                ]
            ].to_string(index=False)
        })

        content = response.content

        if isinstance(content, list):
            content = "".join(
                item.get("text", str(item))
                if isinstance(item, dict)
                else str(item)
                for item in content
            )

        return str(content).strip()

    except Exception as error:

        print("\nGemini explanation unavailable.")
        print("Using local explanation.")
        print("Reason:", error)

        return generate_local_explanation(
            user_query,
            preferences,
            recommendations
        )