import requests
import pandas as pd

class BinanceTestnetClient:
    def __init__(self):
        # L'URL officielle dyal Spot Testnet (Gratuit w sans limites)
        self.base_url = "https://testnet.binance.vision/api/v3"

    def get_historical_data(self, symbol="PAXGUSDT", interval="15m", limit=100):
        """
        Ktjib les bougies (OHLCV) mn Binance Testnet w katrdhom DataFrame n9i.
        """
        endpoint = f"{self.base_url}/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        try:
            # 1. Nssifto la requête l'Broker
            response = requests.get(endpoint, params=params)
            response.raise_for_status() # Katw9ef l'code ila kan chi erreur 404 wla 500
            data = response.json()

            # 2. Nformatiw data l'wa7d tableau mnadem (DataFrame)
            columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                       'close_time', 'quote_asset_volume', 'number_of_trades', 
                       'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
            
            df = pd.DataFrame(data, columns=columns)

            # 3. Nn9iw l'Data (Clean-up)
            # Nbadlo l'wa9t mn Milliseconds l'Date ma9rou2a
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Nredou les prix b format a3dad 3achariya (Float) machi texte
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, axis=1)

            # 4. Nkhlliw ghir dakchi li ghadi t7tajo l'IA (Open, High, Low, Close, Volume)
            clean_df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            
            return clean_df

        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur f l'connexion m3a Binance: {e}")
            return None