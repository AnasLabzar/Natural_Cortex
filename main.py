from data.market_data import BinanceTestnetClient
from core.ai_brain import OpenClawBrain
from execution.trader import ExecutionModule

def main():
    print("🚀 Lancement dyal OpenClaw v1.0 (SOC Complet)...")
    
    # Initialisation dyal les modules b 3
    client = BinanceTestnetClient()
    brain = OpenClawBrain()
    executor = ExecutionModule(risk_reward_ratio=2.0)
    
    print("📊 Kan-fetchi data dyal PAXG/USDT (Timeframe: M15)...")
    df = client.get_historical_data(symbol="PAXGUSDT", interval="15m", limit=5)
    
    if df is not None:
        # Njbdo l'prix lekher (Current Price) bach n7sbo 3lih SL w TP
        current_price = df.iloc[-1]['close']
        
        print("✅ Data tchargat. Kan-ssiftha l'Cerveau (Gemini API) y-analysiها...")
        print("-" * 50)
        
        # 1. Analyse
        analysis = brain.analyze_market(df)
        
        if analysis:
            print("🧠 Décision dyal l'Agent OpenClaw:")
            print(f"🔹 Action     : {analysis.get('decision')}")
            print(f"🔹 Confiance  : {analysis.get('confidence')}%")
            print(f"🔹 Raison     : {analysis.get('reasoning')}")
            
            # 2. Exécution & Risque
            executor.execute_order(analysis, current_price)
        else:
            print("⚠️ L'IA ma9dratsh t3ti décision.")
            
        print("-" * 50)
    else:
        print("⚠️ Mochkil f jiban d l'Data.")

if __name__ == "__main__":
    main()