from helper.Categorizer import categorizer
from helper.SentimentAnalysis import sentimentAnalysis
from helper.StoreIntoDatabase import storeIntoDatabase
from helper.Summary import main_summarizer


async def process_Text(file_path, username, API_KEY):
    with open(file_path, 'r') as file:
        text = file.read()
    summary = await main_summarizer(text, API_KEY)
    category = await categorizer(summary, API_KEY)
    sentiment = sentimentAnalysis(text)
    await storeIntoDatabase(summary, category, sentiment, username)
