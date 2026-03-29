import os
from google.cloud import vision
from helper.Categorizer import categorizer
from helper.SentimentAnalysis import sentimentAnalysis
from helper.StoreIntoDatabase import storeIntoDatabase
from helper.Summary import summarizer

def process_Image(file_path, username, API_KEY):
    # Google credentials loaded from .env
    client = vision.ImageAnnotatorClient()

    with open(file_path, 'rb') as image:
        content = image.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    text = response.text_annotations[0].description
        
    summary = summarizer(text, API_KEY)

    category = categorizer(summary, API_KEY)

    sentiment = sentimentAnalysis(text)

    storeIntoDatabase(summary, category, sentiment, username)
    
