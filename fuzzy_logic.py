import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ---------------------------------------------------------
# FUZZY INPUTS
# ---------------------------------------------------------

# Price match: 0 = poor match, 10 = perfect match
price_match = ctrl.Antecedent(np.arange(0, 10.1, 0.1), "price_match")

# Distance match: 0 = poor match, 10 = perfect match
distance_match = ctrl.Antecedent(
    np.arange(0, 10.1, 0.1),
    "distance_match"
)

# Rating match: 0 = poor match, 10 = perfect match
rating_match = ctrl.Antecedent(
    np.arange(0, 10.1, 0.1),
    "rating_match"
)

# Final suitability score
suitability = ctrl.Consequent(
    np.arange(0, 101, 1),
    "suitability"
)


# ---------------------------------------------------------
# MEMBERSHIP FUNCTIONS
# ---------------------------------------------------------

# Price match
price_match["poor"] = fuzz.trapmf(
    price_match.universe,
    [0, 0, 2, 4]
)

price_match["average"] = fuzz.trimf(
    price_match.universe,
    [2, 5, 8]
)

price_match["good"] = fuzz.trapmf(
    price_match.universe,
    [6, 8, 10, 10]
)


# Distance match
distance_match["poor"] = fuzz.trapmf(
    distance_match.universe,
    [0, 0, 2, 4]
)

distance_match["average"] = fuzz.trimf(
    distance_match.universe,
    [2, 5, 8]
)

distance_match["good"] = fuzz.trapmf(
    distance_match.universe,
    [6, 8, 10, 10]
)


# Rating match
rating_match["poor"] = fuzz.trapmf(
    rating_match.universe,
    [0, 0, 2, 4]
)

rating_match["average"] = fuzz.trimf(
    rating_match.universe,
    [2, 5, 8]
)

rating_match["good"] = fuzz.trapmf(
    rating_match.universe,
    [6, 8, 10, 10]
)


# Output suitability
suitability["low"] = fuzz.trapmf(
    suitability.universe,
    [0, 0, 25, 45]
)

suitability["medium"] = fuzz.trimf(
    suitability.universe,
    [30, 50, 70]
)

suitability["high"] = fuzz.trapmf(
    suitability.universe,
    [55, 75, 100, 100]
)


# ---------------------------------------------------------
# FUZZY RULES
# ---------------------------------------------------------

rule1 = ctrl.Rule(
    price_match["good"] &
    distance_match["good"] &
    rating_match["good"],
    suitability["high"]
)

rule2 = ctrl.Rule(
    price_match["good"] &
    distance_match["good"] &
    rating_match["average"],
    suitability["high"]
)

rule3 = ctrl.Rule(
    price_match["good"] &
    distance_match["average"] &
    rating_match["good"],
    suitability["high"]
)

rule4 = ctrl.Rule(
    price_match["average"] &
    distance_match["good"] &
    rating_match["good"],
    suitability["high"]
)

rule5 = ctrl.Rule(
    price_match["good"] &
    distance_match["average"] &
    rating_match["average"],
    suitability["medium"]
)

rule6 = ctrl.Rule(
    price_match["average"] &
    distance_match["average"] &
    rating_match["good"],
    suitability["medium"]
)

rule7 = ctrl.Rule(
    price_match["average"] &
    distance_match["good"] &
    rating_match["average"],
    suitability["medium"]
)

rule8 = ctrl.Rule(
    price_match["poor"] |
    distance_match["poor"] |
    rating_match["poor"],
    suitability["low"]
)

rule9 = ctrl.Rule(
    price_match["poor"] &
    distance_match["average"],
    suitability["low"]
)

rule10 = ctrl.Rule(
    price_match["average"] &
    distance_match["poor"],
    suitability["low"]
)

rule11 = ctrl.Rule(
    price_match["good"] &
    distance_match["poor"],
    suitability["medium"]
)


# ---------------------------------------------------------
# CONTROL SYSTEM
# ---------------------------------------------------------

restaurant_control_system = ctrl.ControlSystem([
    rule1,
    rule2,
    rule3,
    rule4,
    rule5,
    rule6,
    rule7,
    rule8,
    rule9,
    rule10,
    rule11
])


# ---------------------------------------------------------
# FUZZY CALCULATION
# ---------------------------------------------------------

def calculate_suitability(
    price_match_value,
    distance_match_value,
    rating_match_value
):
    """
    Calculate restaurant suitability using fuzzy inference.

    Inputs are preference-match scores from 0 to 10.
    The fuzzy system performs:
    1. Fuzzification
    2. Rule evaluation
    3. Rule aggregation
    4. Defuzzification
    """

    simulation = ctrl.ControlSystemSimulation(
        restaurant_control_system
    )

    simulation.input["price_match"] = np.clip(
        price_match_value, 0, 10
    )

    simulation.input["distance_match"] = np.clip(
        distance_match_value, 0, 10
    )

    simulation.input["rating_match"] = np.clip(
        rating_match_value, 0, 10
    )

    simulation.compute()

    return simulation.output["suitability"]