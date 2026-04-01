from helper.Categorizer import categorizer
from helper.SentimentAnalysis import sentimentAnalysis
from helper.StoreIntoDatabase import storeIntoDatabase
from helper.Summary import summarizer_two


async def process_Text(file_path, username, API_KEY):
    with open(file_path, 'r') as file:
        text = file.read()

    summary = await summarizer_two(text, API_KEY)
    category = await categorizer(summary, API_KEY)
    sentiment = sentimentAnalysis(text)
    await storeIntoDatabase(summary, category, sentiment, username)
