import google.generativeai as genai
from dotenv import load_dotenv
import os 

load_dotenv()
gemini_key=os.getenv('GOOGLE_API_KEY')


genai.configure(api_key = gemini_key)
model = genai.GenerativeModel('gemini-1.5-flash')


def translate(content="Comment tu vas?"):
    template=f"""
    Traduis simplement et directement en yoruba sans rien rajouter
    phrase1: 'Bonjour'
    traduction1:'Bawo ni'
    
    phrase2 :'{content}'
    traduction2:
    """
    translation=model.generate_content(template).text
    return translation

print(translate())