from fastapi import APIRouter
from app.services.crypto_service import get_crypto_price_by_name
from app.models import CryptoPriceResponse

router = APIRouter()


@router.get("/crypto_price/{crypto_name}")
async def get_crypto_price(crypto_name: str) -> CryptoPriceResponse:
    return get_crypto_price_by_name(crypto_name)