import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.environ.get("OPENAI_ASSISTANT_ID")
LIBRETTO_API_KEY = os.environ.get("LIBRETTO_API_KEY")
LIBRETTO_API_NAME = os.environ.get("LIBRETTO_API_NAME", "HUB Assistant")
