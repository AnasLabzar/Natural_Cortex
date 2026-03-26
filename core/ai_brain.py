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

    def analyze_market(self, mtf_data):
        """
        L'IA kat-analysi l'marché b stratégie ICT (Inner Circle Trader)
        """
        # N-formatiw data bjouj l'texte
        m15_str = mtf_data["M15"].to_string(index=False)
        m5_str = mtf_data["M5"].to_string(index=False)

        prompt = f"""
        You are 'OpenClaw', an elite institutional quantitative algorithm based on ICT (Inner Circle Trader) and SMC (Smart Money Concepts) methodologies.
        
        Analyze the following Gold (PAXG/USDT) Multi-Timeframe data:
        
        --- MACRO CONTEXT (M15 - 15 Minute Chart) ---
        {m15_str}
        
        --- ENTRY CONFIRMATION (M5 - 5 Minute Chart) ---
        {m5_str}

        YOUR INSTRUCTIONS:
        1. M15 Bias: Identify the overall institutional bias. Look for sweeps of liquidity (BSL/SSL) and Order Blocks.
        2. M5 Trigger: Look for Market Structure Shifts (MSS) and Fair Value Gaps (FVG) aligning with the M15 bias.
        3. REAL-TIME SCANNING: If the M5 timeframe does not show a clear, high-probability FVG or MSS *right now*, you MUST wait (HOLD).

        Respond STRICTLY in valid JSON format with no markdown formatting or extra text:
        {{
            "decision": "BUY" | "SELL" | "HOLD",
            "confidence": <number between 0 and 100>,
            "ict_context": {{
                "m15_bias": "BULLISH" | "BEARISH" | "NEUTRAL",
                "m5_trigger_found": "YES" | "NO",
                "key_levels": "<mention any specific price level acting as FVG or OB>"
            }},
            "reasoning": "<Technical ICT explanation: mention liquidity sweeps, FVG, or MSS>"
        }}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```"):
                response_text = response_text[3:-3].strip()

            return json.loads(response_text)

        except Exception as e:
            print(f"❌ Erreur f l'analyse dyal Gemini: {e}")
            return None 