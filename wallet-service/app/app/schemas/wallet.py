from api_contrib.schemas.base import ResponseFormat, BaseModel


class CurrencyIn(BaseModel):
    currencyid: str


class DepositAddressMessage(BaseModel):
    address: str
    note: str


class DepositAddressResponse(ResponseFormat):
    message: DepositAddressMessage

