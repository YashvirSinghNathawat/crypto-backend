from pydantic import BaseModel

class CryptoPriceResponse(BaseModel):
    accept: int
    message: str = None
    price_data: float = None