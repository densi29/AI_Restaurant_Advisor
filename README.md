# 🍴 AI Based Restaurant Selection Advisor

## Student Project

**Project Title:** AI Based Restaurant Selection Advisor

**Student Name:** Densi

**Student ID:** 19007

**Class / Grade:** TYIT

**Subject:** Information Technology

**Academic Year:** 2026

**Project Type:** Artificial Intelligence Mini Project

---

# 📌 Project Overview

The **AI Based Restaurant Selection Advisor** is an intelligent restaurant recommendation system developed using Python, LangChain, Google Gemini and Fuzzy Logic.

The system allows users to describe their restaurant preferences using normal natural language.

For example:

> "I want a cheap Chinese restaurant nearby with a good rating for a family dinner."

The application analyzes the user's request, extracts important preferences, and recommends suitable restaurants from a restaurant dataset.

The system combines two major AI techniques:

1. **Large Language Model (LLM) based preference extraction**
2. **Fuzzy Logic based restaurant suitability scoring**

A fallback mechanism is also included so that the application can continue working when the Gemini API is unavailable or its API quota is exceeded.

---

# 🎯 Project Objectives

The main objectives of this project are:

- To build an AI-based restaurant recommendation system.
- To understand natural-language restaurant preferences.
- To use LangChain for integrating an LLM.
- To use Google Gemini for extracting structured preferences.
- To implement fuzzy logic for restaurant suitability.
- To rank restaurants according to user preferences.
- To provide recommendations through a simple Streamlit interface.
- To create a fallback system when the Gemini API cannot be used.
- To demonstrate the practical use of Artificial Intelligence and Soft Computing.

---

# 🧠 How the System Works

The complete system follows this workflow:

```text
                 User
                  │
                  ▼
        Natural Language Query
                  │
                  ▼
        ┌───────────────────┐
        │ LangChain + Gemini│
        └───────────────────┘
                  │
                  ▼
       Extract User Preferences
                  │
                  ▼
        Structured Preferences
                  │
                  ▼
        Restaurant Dataset
                  │
                  ▼
          Fuzzy Logic System
                  │
          ┌───────┴────────┐
          ▼                ▼
     Fuzzification     Fuzzy Rules
          │                │
          └───────┬────────┘
                  ▼
             Defuzzification
                  │
                  ▼
          Suitability Score
                  │
                  ▼
        Restaurant Ranking
                  │
                  ▼
       Top Recommendations
                  │
                  ▼
          Streamlit Interface