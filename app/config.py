import os
from dotenv import load_dotenv

load_dotenv()  # automatycznie ładuje dane z .env, jeśli jest obecny

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SCRAPE_URL= os.environ.get("SCRAPE_URL")
SCRAPE_INTERVAL= int(os.environ.get("SCRAPE_INTERVAL"))

