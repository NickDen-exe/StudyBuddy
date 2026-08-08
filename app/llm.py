import os
from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-4o-mini"  # Specify the model you want to use
MAX_TOKENS = 150  # Maximum number of tokens in the response
TEMPERATURE = 0.2
SYSTEM_PROMPT = "You are a helpful assistant that provides concise and informative answers to user queries."

load_dotenv()  # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content.strip()
