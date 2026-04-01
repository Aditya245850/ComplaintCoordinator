from google.cloud import vision

from helper.Categorizer import categorizer
from helper.SentimentAnalysis import sentimentAnalysis
from helper.StoreIntoDatabase import storeIntoDatabase
from helper.Summary import summarizer_two


async def process_Image(file_path, username, API_KEY):
    with open(file_path, 'rb') as image_file:
        content = image_file.read()

    client = vision.ImageAnnotatorAsyncClient()
    image = vision.Image(content=content)
    response = await client.text_detection(image=image)

    text = response.text_annotations[0].description if response.text_annotations else ""

    summary = await summarizer_two(text, API_KEY)
    category = await categorizer(summary, API_KEY)
    sentiment = sentimentAnalysis(text)
    await storeIntoDatabase(summary, category, sentiment, username)
