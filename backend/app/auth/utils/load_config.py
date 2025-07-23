from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM_TYPE")