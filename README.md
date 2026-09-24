AI Based Restaurant Selection Advisor
An AI-powered restaurant recommendation mini project that combines LangChain + Gemini for natural-language preference extraction with a Fuzzy Logic Inference System for restaurant ranking.
Overview
The application allows a user to enter a request such as:
I want a cheap Chinese restaurant near me with excellent rating for a family dinner.
The system:
Understands the natural-language request using Gemini through LangChain.
Extracts structured preferences such as cuisine, budget, distance, rating and occasion.
Uses fuzzy logic to evaluate how well each restaurant matches the preferences.
Calculates a suitability score for each restaurant.
Displays the top restaurant recommendations through a Streamlit web interface.
If Gemini is unavailable or its API quota is exceeded, the application automatically uses a local fallback preference parser so that recommendations can still be generated.
Technologies Used
Python
Streamlit
LangChain
Google Gemini
scikit-fuzzy
Pandas
NumPy
Git & GitHub
Streamlit Community Cloud
Project Structure
AI_Restaurant_Advisor/
│
├── app.py
├── fuzzy_logic.py
├── llm_handler.py
├── recommendation_engine.py
├── restaurants.csv
├── requirements.txt
├── .gitignore
└── .env
File Description
File
Purpose
app.py
Streamlit user interface and application flow
llm_handler.py
Gemini/LangChain preference extraction and fallback parser
fuzzy_logic.py
Fuzzy membership functions, inference and suitability scoring
recommendation_engine.py
Combines preferences, restaurant data and fuzzy scores to rank restaurants
restaurants.csv
Restaurant dataset
requirements.txt
Python dependencies
.env
Local API-key configuration; not committed to GitHub
How the AI Works
1. Natural-Language Understanding
The user does not need to fill separate forms for every preference. They can describe what they want in normal language.
Example:
I want a cheap Chinese restaurant near me with excellent rating for a family dinner.
The LLM extracts structured information similar to:
{
  "cuisine": "Chinese",
  "budget": "cheap",
  "distance": "near",
  "rating": "excellent",
  "occasion": "family dinner"
}
This is a genuine language-understanding task performed by the LLM rather than simply displaying an LLM response.
2. Fuzzy Logic
Restaurant selection involves vague concepts such as:
cheap
near
good/excellent rating
These concepts are represented using fuzzy membership functions instead of only rigid yes/no conditions.
The fuzzy inference system performs:
Crisp restaurant data
        ↓
Fuzzification
        ↓
Fuzzy rule evaluation
        ↓
Fuzzy inference
        ↓
Defuzzification
        ↓
Suitability score
        ↓
Restaurant ranking
The final suitability score is used to rank restaurants.
Dataset
The project uses restaurants.csv containing 20 restaurant records.
The main fields are:
Restaurant
Cuisine
Price
Distance
Rating
Vegetarian
The dataset contains examples from Indian, South Indian, Chinese, Italian, Mexican, Fast Food and Healthy categories.
Example Result
For a Chinese, cheap, near and excellent-rated family-dinner request, one test run produced:
Restaurant
Cuisine
Price
Distance
Rating
Suitability
Wok Express
Chinese
800
2.0
4.0
79.64
China Bowl
Chinese
1100
3.5
4.3
69.88
Golden Dragon
Chinese
1800
7.0
4.6
17.98
The ranking demonstrates that the system considers multiple preferences rather than selecting a restaurant using rating alone.
Fallback Mechanism
Gemini's free API has request/quota limits. To make the application more robust, the project includes a local fallback parser.
When Gemini cannot be used, the application:
User request
     ↓
Gemini/LangChain
     ↓
If unavailable/quota exceeded
     ↓
Local fallback preference parser
     ↓
Same fuzzy recommendation system
Therefore, the recommendation pipeline can continue even when the LLM service is temporarily unavailable.
Running Locally
1. Clone the repository
git clone https://github.com/densi29/AI_Restaurant_Advisor.git
cd AI_Restaurant_Advisor
2. Create and activate a virtual environment
Windows CMD:
python -m venv venv
venv\Scripts\activate
3. Install dependencies
python -m pip install -r requirements.txt
4. Configure the Gemini API key
Create a .env file:
GEMINI_API_KEY=YOUR_API_KEY_HERE
Do not commit the .env file to GitHub.
5. Run the Streamlit application
streamlit run app.py
The application will open in your browser.
Deployment
The application is designed to run on Streamlit Community Cloud.
For deployment:
Push the project to GitHub.
Create a Streamlit Community Cloud application.
Select this repository and the main branch.
Set the main file to:
app.py
Add the Gemini API key through the deployment platform's Secrets settings.
Deploy the application.
The API key should never be placed directly in the GitHub repository.
GitHub
Repository:
https://github.com/densi29/AI_Restaurant_Advisor
Limitations
The current dataset is static and contains 20 restaurants.
The application does not provide live restaurant availability or booking.
It does not use live traffic or real-time travel time.
LLM usage is subject to the available API quota.
Recommendations depend on the quality of the restaurant dataset.
Future Scope
Possible improvements include:
Live restaurant data
Real-time location and travel time
Dietary and allergy preferences
More fuzzy variables
User-adjustable preference weights
Explanation of individual recommendation scores
Restaurant availability and booking integration
Project Objective
The main objective is to demonstrate how LLM-based natural-language understanding and fuzzy inference can be combined in a practical decision-support application.
License
This project was created as an academic mini project.