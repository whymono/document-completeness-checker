import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
def analyze_document(query: str) -> str:

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return 1

    client = genai.Client(api_key=api_key)

    response= client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query
    )

    return response.text

print(analyze_document("where is the eifill tower"))
