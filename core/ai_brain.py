import os
import json
from google import genai
from dotenv import load_dotenv

# Nchargiw les clés li f .env
load_dotenv()

class OpenClawBrain:
    def __init__(self):
        # Configuration dyal Gemini API b l'SDK jdid
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("🚨 L'API Key dyal Gemini ma l9ithach f .env!")
        
        # Initialisation dyal l'client jdid
        self.client = genai.Client(api_key=api_key)
        # Nkhdmo b l'modèle jdid
        self.model_id = 'gemini-2.5-flash'

    def analyze_market(self, df):
        """
        Katchd l'Dataframe dyal les prix w katsiftha l'IA bach t'analysiha.
        """
        # Nredou l'Dataframe l'texte (String) bach tfhmo l'IA
        market_data_str = df.to_string(index=False)

        # Hada howa "Le Prompt Magique"
        prompt = f"""
        You are 'OpenClaw', an elite quantitative trading AI agent.
        Your objective is to analyze the following 15-minute candlestick data for PAXG/USDT (a proxy for XAU/USD Gold).
        
        Market Data:
        {market_data_str}

        Analyze the price action, momentum, and volume. 
        Provide a trading decision. You MUST respond strictly in valid JSON format with no markdown formatting or extra text.
        
        Use this exact JSON structure:
        {{
            "decision": "BUY" | "SELL" | "HOLD",
            "confidence": <number between 0 and 100>,
            "reasoning": "<short explanation of your analysis>"
        }}
        """

        try:
            # La nouvelle syntaxe dyal generate_content f google-genai
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            
            # N-nettoyew la réponse
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```"):
                response_text = response_text[3:-3].strip()

            # N-convertiw texte l'objet JSON
            decision_json = json.loads(response_text)
            return decision_json

        except Exception as e:
            print(f"❌ Erreur f l'analyse dyal Gemini: {e}")
            return None