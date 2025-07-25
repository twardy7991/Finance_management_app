from tenacity import retry, wait_random_exponential
from openai import OpenAI
import json
from google import genai


class Connection:
    
    def __init__(self):
        
        self.OPENAI_API_KEY = "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"
        self.GOOGLE_API_KEY = "AIzaSyBodmtJ0M3FACNavFKov_rfXDDxnNIJWvo"

        self.client = genai.Client(api_key=self.GOOGLE_API_KEY)
        
    def category_definition_openai(self):
        
        client = OpenAI(api_key=self.OPENAI_API_KEY)
        response = client.responses.create(
        model="gpt-3.5-turbo",
        input="Hello."
        )
        
        return response

    @retry(wait=wait_random_exponential(multiplier=1, max=60))
    def category_definition_gemini(self,operation, categories):

        question = f'''wybież jedna z podanych kategorii, - {categories} - dla podanego zakupu - 
                    zakup: "{operation}" - w swojej odpowiedzi podaj tylko i wyłącznie kategorię i nic więcej'''
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=[question]
        )
        
        return response.candidates[0].content.parts[0].text.strip()