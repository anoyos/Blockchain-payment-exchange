from decimal import Decimal
from typing import Dict, Optional

from api_contrib.schemas.base import ResponseFormat
from pydantic import Field, BaseModel

from app.models.balance import Balance


class BalanceLegacy(Balance):
    currency: Optional[str] = Field(description="DEPRECATED, use asset_code instead")
    status: Optional[Dict] = Field(description="DEPRECATED")
    balance_deposit: Optional[Decimal] = Field(description="DEPRECATED", default=Decimal(0.00000000))
    balance_exchange: Optional[Decimal] = Field(description="DEPRECATED", default=Decimal(0.00000000))
    balance_lockbox: Optional[Decimal] = Field(description="DEPRECATED", default=Decimal(0.00000000))
    balance_orders: Optional[Decimal] = Field(description="DEPRECATED", default=Decimal(0.00000000))
    balance_reserved: Optional[Decimal] = Field(description="DEPRECATED", default=Decimal(0.00000000))
    balance_withdrawal: Optional[Decimal] = Field(description="DEPRECATED", default=Decimal(0.00000000))

    def __init__(self, **data):
        super().__init__(**data)
        self.currency = self.asset_code
        self.status = {
            "blockhash": '00000000616d03cb08761002b12c02bd1bf1e092123e6da8800c37b76b68d40a',
            "blocktime": 1595018697,
            "difficulty": '1.00000000',
            "height": 1780975,
            "insync": True,
            "lastblock": 1595018697,
            "maintenance": False,
            "online": True,
            "peers": 10,
            "protocol_version": '70015',
            "revision": 1595018640,
            "version": '190001',
            "wallet_version": '169900',
            "walletmaintenance": True,
        }
        # self.settings = {
        #     "deposit_enabled": True,
        #     "withdrawal_enabled": True,
        #     "confirmations": 3,
        #     "has_withdrawallimit": False,
        #     "is_delisted": False,
        #     "txfee": '0.00001024',
        #     "will_be_delisted": False,
        #   }


class BalanceResponse(ResponseFormat):
    message: Dict[str, BalanceLegacy]

    class Config:
        arbitrary_types_allowed = True


class BalanceInUSDT(BaseModel):
    total_in_usd: Decimal = Field(description="Sum of all user balances quoted in USD")


class BalanceInUSDTResponse(ResponseFormat):
    message: BalanceInUSDT
