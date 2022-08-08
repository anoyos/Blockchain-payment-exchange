from typing import Dict, Any

from api_contrib.core.services import get_current_user
from api_contrib.core.utils import logger
from api_contrib.tools.qr import create_qr_code
from fastapi import APIRouter, Depends, Response

from app import schemas
from app.blockchain.handlers.factory import blockchain_handlers
from app.core.tools import get_asset_by_id

router = APIRouter()


@router.get("/make_qr/")
def make_qr_code(address: str = ''):
    qr_code_bytes = create_qr_code(address)
    return Response(content=qr_code_bytes, media_type="image/png", headers={
        'Content-Disposition': f'inline; address = "{address}"',
        'Access-Control-Expose-Headers': 'Content-Disposition'
    })


@router.post("/depositaddress/", response_model=schemas.DepositAddressResponse)
def get_deposit_address(
        body: schemas.CurrencyIn,
        user: Dict = Depends(get_current_user)
) -> Any:
    """
    Will provide the user with him/hers deposit address for the selected currency.
    Will always return the same result unless the address is discarded, which must be through the support.
    """
    try:
        # Get Coin info
        currency = get_asset_by_id(body.currencyid)
        asset_code = currency['short_name']

        with blockchain_handlers.get(asset_code) as handler:
            deposit_address = handler.get_address_for_user(user_id=user['id'])

        return {
            "message": {
                "address": deposit_address,
                "note":
                    f"""This is a - {currency["long_name"]} ({asset_code}) address.
                    Depositing any other currency to this deposit address may make your money lost forever.
                    Always doublecheck the deposit address when sending funds."""
            }
        }

    except Exception as e:
        logger.error(e, exc_info=True)
        return {"status": "error", "message": str(e)}


@router.get("/nft/all")
async def get_nft_tokens() -> Any:
    """  Retrieve all owned nft tokens """

    scan_url = 'https://rinkeby.etherscan.io'
    trx = '0x34dc54d4b84ba30d12a3df8ad79473ab5bb9392c48557268bb52735b15b41a96'
    contract_address = '0xf5de760f2e916647fd766b4ad9e85ff943ce3a2b'
    token_id = 503666
    owner = '0x8325898A207cB7DF7579AA3c214D17412d29a9E6'

    return {
        "status": "success",
        'message': [
            {
                'contract_address': contract_address,
                'token_id': token_id,
                'owner': owner,
                'scan_url': scan_url,
                'trn_hash': trx,
                'link_to_deal': f'{scan_url}/tx/{trx}',

            }
        ]
    }
