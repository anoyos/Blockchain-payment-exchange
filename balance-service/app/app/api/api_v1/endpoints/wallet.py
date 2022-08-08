from typing import Dict

from api_contrib.core.services import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/ledger/")
async def get_balances(user: Dict = Depends(get_current_user)):
    """
    Load user's transactions
    """
    return {
        "status": 'success',
        "pages": 3,
        "page": 1,
        "items_perpage": 200,
        "items_total": 477,
        "message": [
            {
                "transactionrow": 28876,
                "certificate": '9fe22f81-9de1-43b2-ae50-46e8002ace4b',
                "currencyid": '9036f371-7ab7-48f5-9ba5-5d201c066651',
                "amount": '-0.02000000',
                "date": 1552162164,
                "transaction_type": 13,
            }]
    }


@router.post("/ledgerexport/list/")
def get_load_these(user: Dict = Depends(get_current_user)):
    """
    Load user's transactions
    """
    return {
        "status": 'success',
        "message": [
            {
                "key": '56f09a7d-851b-441a-a5de-a9e0ce8b1803',
                "filename": 'csv.zip',  # Filename will have the export filters to it, so it may change.
                "filesize": '735',  # In bytes
                "created": 1552403028,
            },
            {
                "key": '41cc2bfb-24d4-4d7d-bb63-cff4289db43b',
                "filename": 'csv.zip',  # Filename will have the export filters to it, so it may change.
                "filesize": '735',  # In bytes
                "created": 1552403908,
            },
        ],
    }
