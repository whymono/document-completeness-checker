import os
import json
from google import genai
from dotenv import load_dotenv


OUTPUT_SCHEME = """
Return ONLY valid JSON in this exact format:

{
  "result": [
    {
      "index": integer,
      "title": string,
      "confidence": number between 0 and 1,
      "issue": string
    }
  ]
}

Rules:
- No markdown
- No explanations
- No extra keys
"""

load_dotenv()

def sort_document(embedded: list, text: list) -> dict:
    output = {}
    section = []
    for i in range(len(embedded)):
        sec = []
        for j in embedded[i]:
            sec.append(str(str(text[j]).replace("\n", "\\n")).replace("\\n", "\n"))

        section.append({"index":i, "section":sec})
    output["section"] = section
    return output

def analyze_document(embedded: list, text: list) -> dict:

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Could not find API key")

    client = genai.Client(api_key=api_key)

    prompt = f"""
you are evaluating these document sections independently. return every result with the index of the section. the title is what the sections are about.
the confidence is how confident are we in the section. lets say we have a sections about vacation but it isn't complete and is missing many parts, its confidence would be low.
you can return potential issues or incompleteness, if you didn't find any just return it as "none".
do not think of these as sections, do not assume that the reader knows what section 3 is. refer to them as topics like health or finance.

{json.dumps(sort_document(embedded=embedded, text=text), indent=2)}

{OUTPUT_SCHEME}
"""

    response= client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text