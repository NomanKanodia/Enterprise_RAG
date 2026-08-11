import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is not set in the environment."
    )


client = genai.Client(
    api_key=GOOGLE_API_KEY
)


MODEL_NAME = "gemini-3.6-flash"


def generate_answer(prompt: str) -> str:

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt
    )

    return interaction.output_text