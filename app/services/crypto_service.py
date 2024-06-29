from app.config import settings
from app.models import CryptoPriceResponse
from time import sleep
import requests
import logging
from fastapi import HTTPException


logger = logging.getLogger(__name__)
headers = {"accept": "application/json",
           "x_cg_demo_api_key": settings.coingecko_api_key}


def fetch_crypto_id(crypto_name):
    try:
        url = f"https://api.coingecko.com/api/v3/search?query={crypto_name}"
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        return response
    except requests.exceptions.ConnectionError:
        logger.error("No internet connection available.")
        return HTTPException(status_code=503, detail="Service Unavailable")
    except requests.exceptions.Timeout:
        logger.error("The request timed out.")
        raise HTTPException(status_code=504, detail="Gateway Timeout")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching crypto ID: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logging.error(f"Unexpected error when fetching crypto price for {crypto_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def fetch_crypto_price_by_id(crypto_id,retries=3,delay=1):
    url  = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            logger.warning(f"Rate Limit Exceeded when fetching price. Attempt {attempt+1}/{retries}")
            sleep(delay)
            delay*=2
            continue    
        if response.status_code == 404:
            return CryptoPriceResponse(accept=0,message=f"Coin with ID '{crypto_id}' not found")
        if response.status_code!=200:
            return CryptoPriceResponse(accept=0, message="Failed to fetch crypto price")
        
        crypto_data = response.json()
        try:
            price = crypto_data["market_data"]["current_price"]["usd"]
            return CryptoPriceResponse(accept=1,message="Crypto Price Received Successfully",price_data=price)
        except KeyError:
            return CryptoPriceResponse(accept=0,message="UnExpected response structure from CoinGecko API")
    
    return CryptoPriceResponse(accept=0,message="Exceeded maximum retries for fetching crypto price")


def get_crypto_price_by_name(crypto_name):
    response = fetch_crypto_id(crypto_name)
    
    if response.status_code == 429:
        return CryptoPriceResponse(accept=0,message=f"Due to Rate Limit Exceeded, we cannot fetch data from the API")

    if response.status_code != 200:
        return CryptoPriceResponse(accept=0,message="Failed to fetch crypto ID")
    
    api_data = response.json().get('coins',[])

    # Handling Error when crypto_name is not found
    if not api_data:
        return CryptoPriceResponse(accept=0,message=f"Cryto Name is not Found. Try again with valid crypto name")

    api_id = api_data[0]['id']

    return fetch_crypto_price_by_id(api_id)
