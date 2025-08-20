from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

SESSION_DURATION = os.getenv("SESSION_DURATION")

