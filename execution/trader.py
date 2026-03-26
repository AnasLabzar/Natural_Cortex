class ExecutionModule:
    def __init__(self, risk_reward_ratio=2.0):
        # Risk/Reward Ratio dyal 1:2 (Kankhatro b 1 bach nrb7o 2)
        self.rr_ratio = risk_reward_ratio
        self.mock_capital = 10000  # Capital kdoub l'Paper Trading

    def calculate_sl_tp(self, decision, current_price):
        """
        Kay7seb Stop-Loss w Take-Profit basé 3la l'prix dyal db.
        Ghan-risquew b 0.5% mn l'prix f kol saf9a.
        """
        price_risk = current_price * 0.005  # 0.5% de variation

        if decision == "BUY":
            sl = current_price - price_risk
            tp = current_price + (price_risk * self.rr_ratio)
            return round(sl, 2), round(tp, 2)
            
        elif decision == "SELL":
            sl = current_price + price_risk
            tp = current_price - (price_risk * self.rr_ratio)
            return round(sl, 2), round(tp, 2)
            
        return None, None

    def execute_order(self, analysis, current_price):
        """
        Kay-exécuti l'ordre ila kant l'IA mty9na (Confiance > 50) w ma 9altch HOLD.
        """
        decision = analysis.get('decision')
        confidence = analysis.get('confidence', 0)

        print("\n⚙️ MODULE D'EXÉCUTION & RISQUE:")
        
        # Les filtres de sécurité
        if decision == "HOLD":
            print("⏸️ Action: HOLD. L'Agent kaytsna opportunité 7ssen.")
            return
            
        if confidence < 50:
            print(f"⚠️ Action annulée: L'confiance tay7a ({confidence}%). Risque kbir.")
            return

        # Calcul dyal l'Risk
        sl, tp = self.calculate_sl_tp(decision, current_price)
        
        print(f"⚡ ORDRE APPROUVÉ: {decision} à {current_price}$")
        print(f"🛡️ Stop-Loss (SL)  : {sl}$")
        print(f"🎯 Take-Profit (TP): {tp}$")
        print(f"💰 R/R Ratio       : 1:{self.rr_ratio}")
        
        # Hna f l'avenir ghadi nzidou l'code li kay-connecta m3a Binance API bach ychri d bsse7
        print("\n✅ Ordre Virtuel m-placé b naja7 f l'marché! (Paper Trading Active)")