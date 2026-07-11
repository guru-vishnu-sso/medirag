import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def ask_gemini(
        question,
        context,
        language="English"
):

    prompt = f"""
You are MediRAG, an AI Clinical Knowledge Assistant.

Answer in {language}.

Your task is to answer ONLY using the information provided in the hospital document.

Rules:
1. Answer only from the provided context.
2. If information is missing, reply:
   "The uploaded document does not contain this information."
3. Do not make up information.
4. Keep the answer clear and professional.

------------------------
Hospital Guidelines
------------------------

{context}

------------------------
Question
------------------------

{question}

------------------------
Answer
------------------------
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini Error:\n{str(e)}"