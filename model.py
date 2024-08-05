import os
import cohere
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Cohere API key
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def query_cohere(prompt):
    try:
        response = co.generate(
            model='command-xlarge-nightly',  # You can use different models based on your requirements
            prompt=prompt,
            max_tokens=150
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def read_file(file):
    if file.type == "application/pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.type == "text/csv":
        import pandas as pd
        df = pd.read_csv(file)
        return df.to_string()
    elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        import pandas as pd
        df = pd.read_excel(file)
        return df.to_string()
    elif file.type == "text/plain":
        return str(file.read(), "utf-8")
    else:
        return "Unsupported file type."
