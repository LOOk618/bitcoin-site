from flask import Flask, render_template_string
import requests
import json

app = Flask(__name__)

# Template HTML com TradingView + preços BTC
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Bitcoin Dashboard</title>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <style>
        body { font-family: Arial; background: #1a1a1a; color: white; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: auto; }
        .header { text-align: center; background: #f7931a; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .chart-container { height: 500px; margin: 20px 0; }
        .price-card { background: #2a2a2a; padding: 20px; border-radius: 10px; margin: 10px; }
        .btc-price { font-size: 36px; font-weight: bold; color: #f7931a; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Bitcoin Trading Dashboard</h1>
            <p>Preços em tempo real + Análise técnica</p>
        </div>
        
        <div class="chart-container">
            <div id="tradingview_chart"></div>
        </div>
        
        <div style="display: flex; justify-content: space-around;">
            <div class="price-card">
                <h3>BTC/USD</h3>
                <div class="btc-price" id="btc-price">{{ btc_price or 'Carregando...' }}</div>
            </div>
            <div class="price-card">
                <h3>USD/BRL</h3>
                <div class="btc-price" id="usd-brl">{{ usd_brl or 'Carregando...' }}</div>
            </div>
        </div>
    </div>

    <script>
        new TradingView.widget({
            "container_id": "tradingview_chart",
            "width": "100%",
            "height": 500,
            "symbol": "BINANCE:BTCUSDT",
            "interval": "1D",
            "timezone": "America/Sao_Paulo",
            "theme": "dark",
            "style": "1",
            "locale": "pt_BR",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": false,
            "save_image": false,
            "backgroundColor": "#1a1a1a"
        });
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    try:
        # API CoinGecko (gratuita)
        btc_data = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,brl').json()
        usd_brl = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=usd-coin&vs_currencies=brl').json()
        
        btc_usd = btc_data['bitcoin']['usd']
        btc_brl = btc_data['bitcoin']['brl']
        usdbrl = usd_brl['usd-coin']['brl']
        
        return render_template_string(HTML_TEMPLATE, 
                                    btc_price=f"${btc_usd:,.0f} | R${btc_brl:,.0f}",
                                    usd_brl=f"R${usdbrl:,.2f}")
    except:
        return render_template_string(HTML_TEMPLATE, btc_price="API offline", usd_brl="R$5,60")

if __name__ == '__main__':
    print("🚀 Bitcoin Dashboard iniciando...")
    app.run(debug=True, port=5001, host='127.0.0.1')
