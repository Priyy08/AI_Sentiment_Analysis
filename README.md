# AI Sentiment Analysis
It is an AI Powered Sentiment Analysis tool which can give the overall sentiment of your inputted text along with interactive Plots and Charts.

Overview:

This project is a Sentiment Analysis application built using Python's Streamlit framework. It leverages the Hugging Face API to analyze the sentiment of input text, categorizing it as positive, negative, or neutral. The application also visualizes the sentiment scores using various plots.

Features:

Sentiment Analysis: Uses the Hugging Face model cardiffnlp/twitter-roberta-base-sentiment-latest to determine sentiment labels and scores.
Data Visualization: Displays the sentiment analysis results using:
Vertical Bar Chart
Horizontal Bar Chart
Pie Chart
Gauge-like Progress Bar for positive sentiment
SQLite Database: Stores the analysis results for future reference.
Technologies Used
Python
Streamlit
Hugging Face API
SQLite
Matplotlib
Installation
Prerequisites
Make sure you have Python 3.7 or higher installed. You will also need to install the required packages.

# Step 1: Clone the Repository
```bash
git clone https://github.com/your_username/your_repository_name.git
cd your_repository_name
```

# Step 2: Install Required Packages
Create a requirements.txt file (if not already present) with the following content:
```bash
streamlit==1.33.0
requests==2.28.1
matplotlib==3.9.2
sqlite3
```

# Step 3: Set Up Hugging Face API
1.Sign up at Hugging Face.
2.Obtain an API token by navigating to your account settings.
3.Replace the placeholder in the code with your actual token:

```bash
headers = {"Authorization": "Bearer YOUR_HUGGING_FACE_TOKEN"}
```
# Usage
Step 1: Run the Streamlit App
Navigate to the project directory and run the following command:
```bash
streamlit run app.py
```
Step 2: Analyze Sentiment
Open your web browser and go to http://localhost:8501.
Enter a sentence or paragraph in the text area.
Click the "Submit" button to analyze the sentiment.
The results will be displayed along with visualizations.
Step 3: View Stored Results
The results of the sentiment analysis are stored in an SQLite database named sentiment_analysis.db. You can query this database using any SQLite database viewer to see past analyses.

# Code Structure
app.py: The main application file containing the logic for sentiment analysis and visualization.
sentiment_analysis.db: SQLite database to store results.
# Contributing:
If you wish to contribute to this project, feel free to fork the repository and submit a pull request. Make sure to follow the coding style and add comments to your code.

# Acknowledgments
Hugging Face for the sentiment analysis model.
Streamlit for providing an easy way to build interactive web apps.
Matplotlib for visualization.
Feel free to adjust any sections or add more details as needed! Let me know if you need further assistance.
