# The coingecko API was too expensive.
from flask import Flask
import os
from dotenv import load_dotenv
import requests


load_dotenv()
PROVIDER_PORT = os.getenv('PROVIDER_PORT')
PROVIDER_API_KEY = os.getenv('COINGECKO_API_KEY')
app = Flask(__name__)

@app.route("/")
def conversion_rate():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "x_cg_demo_api_key": PROVIDER_API_KEY,
        "ids": "shyft-network-2",
        "vs_currencies": "eth"
    }

    response = requests.get(url, params=params)
    data = response.json()
    # Extracting the price of Shyft Network in Ethereum
    shyft_price_in_eth = data["shyft-network-2"]["eth"]
    shyft_price_in_eth = str(shyft_price_in_eth)
    print(f"The price of Shyft Network in Ethereum is: {shyft_price_in_eth}")

    return shyft_price_in_eth

    


if __name__ == "__main__":
    app.run(port=PROVIDER_PORT)
