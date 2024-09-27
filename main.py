import streamlit as st
import requests
import matplotlib.pyplot as plt
import sqlite3

API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")

# Set Hugging Face API parameters
API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
headers = {"Authorization": "Bearer {API_TOKEN}"}  # Replace with your actual token

# Create or connect to SQLite database
conn = sqlite3.connect('sentiment_analysis.db')
c = conn.cursor()

# Create a table to store results if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS sentiment_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        positive_label TEXT,
        positive_score REAL,
        negative_label TEXT,
        negative_score REAL,
        neutral_label TEXT,
        neutral_score REAL
    )
''')
conn.commit()

# Function to query Hugging Face model for sentiment analysis
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to analyze sentiment and return labels and scores
def analyze_sentiment(text):
    output = query({"inputs": text})
    
    # Initialize variables
    positive_label = negative_label = neutral_label = None
    positive_score = negative_score = neutral_score = 0

    # Process the API output to extract sentiment labels and scores
    if isinstance(output, list) and len(output) > 0 and isinstance(output[0], list):
        for item in output[0]:
            sentiment = item['label']
            score = item['score']

            if sentiment == 'positive':
                positive_label = sentiment
                positive_score = score
            elif sentiment == 'negative':
                negative_label = sentiment
                negative_score = score
            elif sentiment == 'neutral':
                neutral_label = sentiment
                neutral_score = score
                
        st.write(f"**Positive Sentiment Score:** {positive_score}")
        st.write(f"**Negative Sentiment Score:** {negative_score}")
        st.write(f"**Neutral Sentiment Score:** {neutral_score}")

        return positive_label, positive_score, negative_label, negative_score, neutral_label, neutral_score
    else:
        return None, None, None, None, None, None

# Streamlit app layout
st.title("Sentiment Analysis App")

# User input field
text_input = st.text_area("Enter a sentence or paragraph to analyze:", "")

# Submit button
if st.button("Submit"):
    if text_input.strip() == "":
        st.error("Please enter some text for analysis.")
    else:
        # Call sentiment analysis function
        positive_label, positive_score, negative_label, negative_score, neutral_label, neutral_score = analyze_sentiment(text_input)
        
        if positive_label or negative_label or neutral_label:
            st.success("Sentiment Analysis Completed!")

            # Insert the results into the database
            c.execute('''
                INSERT INTO sentiment_results (text, positive_label, positive_score, negative_label, negative_score, neutral_label, neutral_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (text_input, positive_label, positive_score, negative_label, negative_score, neutral_label, neutral_score))
            conn.commit()  # Commit the changes

            # Prepare data for visualization
            labels = []
            scores = []
            
            if positive_label:
                labels.append(positive_label)
                scores.append(positive_score)
            if negative_label:
                labels.append(negative_label)
                scores.append(negative_score)
            if neutral_label:
                labels.append(neutral_label)
                scores.append(neutral_score)

            # Data Visualization
            fig, ax = plt.subplots(2, 2, figsize=(12, 10))  # 2x2 grid of plots

            # 1. Vertical Bar Chart
            ax[0, 0].bar(labels, scores, color=['green', 'red', 'blue'])
            ax[0, 0].set_title("Sentiment Analysis Scores (Bar Chart)")
            ax[0, 0].set_xlabel("Sentiment")
            ax[0, 0].set_ylabel("Score")

            # 2. Horizontal Bar Chart
            ax[0, 1].barh(labels, scores, color=['green', 'red', 'blue'])
            ax[0, 1].set_title("Sentiment Analysis Scores (Horizontal Bar Chart)")
            ax[0, 1].set_xlabel("Score")
            ax[0, 1].set_ylabel("Sentiment")

            # 3. Pie Chart for sentiment score distribution
            ax[1, 0].pie(scores, labels=labels, colors=['green', 'red', 'blue'], autopct='%1.1f%%', startangle=90)
            ax[1, 0].set_title("Sentiment Distribution (Pie Chart)")

            # 4. Gauge-like Progress Bar for Positive Sentiment
            positive_percentage = positive_score * 100 if positive_score else 0
            ax[1, 1].barh(['Positive Sentiment'], [positive_percentage], color='green', height=0.5)
            ax[1, 1].set_xlim(0, 100)
            ax[1, 1].set_title("Positive Sentiment Gauge")
            ax[1, 1].set_xlabel("Percentage (%)")

            # Display the visualizations in Streamlit
            st.pyplot(fig)
        else:
            st.error("Unexpected API response format or unable to fetch sentiment results.")

# Close database connection when done
conn.close()
