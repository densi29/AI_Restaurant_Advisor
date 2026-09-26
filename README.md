# 🍽️ AI Based Restaurant Selection Advisor

An AI-powered restaurant recommendation system that combines **Natural Language Processing, LangChain, Google Gemini, and Fuzzy Logic** to understand user preferences and recommend suitable restaurants.

---

## 📌 Project Overview

The **AI Based Restaurant Selection Advisor** is a decision-support application designed to help users find restaurants based on natural-language preferences.

Instead of selecting options manually, users can simply type a request such as:

> "I want a cheap Chinese restaurant nearby with a good rating for a family dinner."

The system analyzes the request, extracts important preferences, evaluates restaurants using a **Fuzzy Logic Inference System**, and displays the most suitable restaurants.

The application also includes a **fallback mechanism** so that recommendations can still be generated when the Gemini API is unavailable or its quota has been exceeded.

---

## ✨ Features

- 🤖 Natural-language restaurant search
- 🧠 Google Gemini AI integration
- 🔗 LangChain-based LLM processing
- 🧩 Automatic preference extraction
- 📊 Fuzzy Logic-based restaurant scoring
- 🍴 Cuisine filtering
- 💰 Budget consideration
- 📍 Distance consideration
- ⭐ Rating consideration
- 👨‍👩‍👧 Occasion consideration
- 🔄 Gemini fallback mechanism
- 📈 Suitability score visualization
- 🌐 Streamlit web interface
- 📁 CSV-based restaurant dataset
- 🔐 Environment-variable API key configuration

---

## 🏗️ System Architecture

```text
                    USER
                      │
                      ▼
             ┌─────────────────┐
             │ Streamlit App   │
             │    app.py       │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ User Query      │
             │ Natural Language│
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────────────┐
             │ LangChain + Gemini     │
             │ Preference Extraction  │
             └────────────┬────────────┘
                          │
                ┌─────────┴─────────┐
                │                   │
          Gemini Available     Gemini Fails
                │                   │
                ▼                   ▼
       Extract Preferences    Local Fallback
                │                   │
                └─────────┬─────────┘
                          │
                          ▼
                ┌─────────────────┐
                │ Structured      │
                │ Preferences     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Restaurant CSV  │
                │ Dataset         │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Fuzzy Logic     │
                │ Inference       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Suitability     │
                │ Score           │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Ranked Restaurant│
                │ Recommendations │
                └─────────────────┘