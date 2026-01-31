
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

with open('models.txt', 'w') as f:
    try:
        f.write("Listing models:\n")
        for m in genai.list_models():
            f.write(f"Model: {m.name}\n")
            f.write(f"Supported methods: {m.supported_generation_methods}\n")
            f.write("-" * 20 + "\n")
    except Exception as e:
        f.write(f"FULL ERROR: {e}\n")
