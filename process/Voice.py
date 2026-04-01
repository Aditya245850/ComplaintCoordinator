from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import RecognitionConfig

from helper.Categorizer import categorizer
from helper.SentimentAnalysis import sentimentAnalysis
from helper.StoreIntoDatabase import storeIntoDatabase
from helper.Summary import main_summarizer


async def process_Voice(file_path, username, API_KEY):
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    client = speech.SpeechAsyncClient()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )

    response = await client.recognize(config=config, audio=audio)

    transcript = " ".join(
        result.alternatives[0].transcript for result in response.results
    ).strip()

    summary = await main_summarizer(transcript, API_KEY)
    category = await categorizer(summary, API_KEY)
    sentiment = sentimentAnalysis(transcript)
    await storeIntoDatabase(summary, category, sentiment, username)
