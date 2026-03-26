import time
from datetime import datetime
from data.market_data import BinanceTestnetClient
from core.ai_brain import OpenClawBrain
from execution.trader import ExecutionModule
from core.notifier import TelegramNotifier

def run_realtime_scanner(client, brain, executor, notifier):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"\n[{timestamp}] 📡 Scan MTF en cours (M15 & M5)...")
    
    # 1. Njibou l'Data Multi-Timeframe (Vison + Confirmation)
    mtf_data = client.get_mtf_data(symbol="PAXGUSDT")
    
    if mtf_data is not None:
        # L'prix dyal db howa l'kher f M5
        current_price = mtf_data["M5"].iloc[-1]['close']
        
        # 2. L'Analyse b l'ICT Cerveau
        analysis = brain.analyze_market(mtf_data)
        
        if analysis:
            decision = analysis.get('decision')
            confidence = analysis.get('confidence')
            reasoning = analysis.get('reasoning')
            
            # Njibou l'contexte ICT li zedna f l'Prompt
            ict_ctx = analysis.get('ict_context', {})
            bias_m15 = ict_ctx.get('m15_bias', 'UNKNOWN')
            trigger_m5 = ict_ctx.get('m5_trigger_found', 'NO')
            
            print(f"🧠 [ICT Cerveau] Décision: {decision} ({confidence}%) | Bias M15: {bias_m15} | M5 Trigger: {trigger_m5}")
            print(f"📝 Raison: {reasoning}")
            
            # 3. Exécution & Notification (GHIR ILA KANAT OPPORTUNITÉ)
            if decision in ["BUY", "SELL"]:
                print(f"⚡ OPPORTUNITÉ DÉTECTÉE ! Exécution de l'ordre...")
                executor.execute_order(analysis, current_price)
                notifier.send_signal(current_price, analysis)
            else:
                print("⏸️ Action: HOLD. L'Agent kay-scanni l'liquidity w kaytsna setup n9i.")
                
        else:
            print("⚠️ L'IA ma9dratsh t-générer l'analyse f had l'itération.")
            
    else:
        print("⚠️ Mochkil f jiban d l'Data mn Binance (Rate limit wla Network).")

def main():
    print("🚀 Lancement dyal OpenClaw v2.0 (ICT/SMC Real-Time Scanner)...")
    
    # Initialisation
    client = BinanceTestnetClient()
    brain = OpenClawBrain()
    executor = ExecutionModule(risk_reward_ratio=2.0)
    notifier = TelegramNotifier()
    
    # Scanner kol 10 secondes (bach manakloch ban mn l'API dyal Binance)
    scan_interval_seconds = 10 
    
    print("⚠️ Attention: L'bot db khddam f mode HFT (High-Frequency Tracking).")
    print("📲 Telegram notifications homa m-réglin ghir 3la les signaux BUY/SELL bach may-spamikch.")
    print("-" * 60)
    
    while True:
        try:
            run_realtime_scanner(client, brain, executor, notifier)
            time.sleep(scan_interval_seconds)
        except KeyboardInterrupt:
            print("\n🛑 L'Agent OpenClaw t-7bess b naja7.")
            break
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}")
            time.sleep(scan_interval_seconds) # Yrtah chwiya ila w9e3 mochkil

if __name__ == "__main__":
    main()