import requests
import pandas as pd

class BinanceTestnetClient:
    def __init__(self):
        self.base_url = "https://testnet.binance.vision/api/v3"

    def fetch_ohlcv(self, symbol="PAXGUSDT", interval="15m", limit=15):
        """Fonction basique bach tjib ay timeframe"""
        endpoint = f"{self.base_url}/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                       'close_time', 'qav', 'num_trades', 'tbbav', 'tbqav', 'ignore']
            df = pd.DataFrame(data, columns=columns)
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, axis=1)

            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        except Exception as e:
            print(f"❌ Erreur API: {e}")
            return None

    def get_mtf_data(self, symbol="PAXGUSDT"):
        """
        Ktjib l'Matrix kamla: M15 l'Vison w M5 l'Confirmation
        """
        # Njbdo 10 bougies d M15 (2.5 sa3at dyal l'historique l'tendance)
        m15_data = self.fetch_ohlcv(symbol, interval="15m", limit=10)
        # Njbdo 6 bougies d M5 (Ness sa3a lakhera l'confirmation dkhoul)
        m5_data = self.fetch_ohlcv(symbol, interval="5m", limit=6)
        
        if m15_data is not None and m5_data is not None:
            return {"M15": m15_data, "M5": m5_data}
        return None