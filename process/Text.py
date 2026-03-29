from helper.Summary import summarizer
from helper.Categorizer import categorizer
from helper.SentimentAnalysis import sentimentAnalysis
from helper.StoreIntoDatabase import storeIntoDatabase

def process_Text(file_path, username, API_KEY):
    with open(file_path, 'r') as file:
        text = file.read()
    summary = summarizer(text, API_KEY)

    category = categorizer(summary, API_KEY)

    sentiment = sentimentAnalysis(text)

    storeIntoDatabase(summary, category, sentiment, username)

