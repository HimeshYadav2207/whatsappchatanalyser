# 📊 WhatsApp Chat Analyzer

A web-based tool that analyzes exported WhatsApp chats (CSV/TXT) and visualizes messaging patterns, user activity, sentiment, and emoji usage — all through an interactive Streamlit dashboard.

## Features
- 📈 Visualizes most active users and message frequency trends
- 😊 Sentiment analysis of chat messages using TextBlob
- 😂 Emoji usage tracking and breakdown
- 📊 Interactive charts and graphs built with Matplotlib and Seaborn
- 🌐 Deployed as a live web app using Streamlit — no coding needed to use it

## Tech Stack
- **Language:** Python
- **Libraries:** Pandas, Matplotlib, Seaborn, TextBlob, Emoji
- **Framework:** Streamlit

## How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/HimeshYadav2207/whatsappchatanalyser.git
cd whatsappchatanalyser
```

2. Install dependencies
```bash
pip install streamlit pandas matplotlib seaborn textblob emoji
```

3. Run the app
```bash
streamlit run app.py
```

4. Export your WhatsApp chat (Settings → Export Chat → Without Media) and upload the file into the app to see the analysis.

## Screenshot
![App Screenshot](screenshot.png)

## Future Improvements
- Word cloud visualization of most-used words
- Support for group chat multi-user comparison
- Downloadable analysis report

---
Built as a personal project to explore data analysis and visualization with Python.
