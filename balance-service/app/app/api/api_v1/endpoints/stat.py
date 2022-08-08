from typing import Any

from api_contrib.schemas.base import CurrencyFilter, ResponseFormat
from fastapi import APIRouter

from app import crud
from app.models import AccountTypes

router = APIRouter()


@router.post("/summary_report/", response_model=ResponseFormat)
async def get_summary_report(payload: CurrencyFilter,
                             # user: Dict = Depends(check_admin_permission)
                             ) -> Any:
    """
    Return summary from system balances
    """
    system_accounts = await crud.balance.find_all({
        "account_type": {"$in": [AccountTypes.SPEND, AccountTypes.PROFIT]},
        "asset_code": payload.asset_code
    })
    report = await crud.entry.summary_report([
        acc['id'] for acc in system_accounts
    ])
    formatted_report = [
        {
            "date": _date,
            "deposits": stat.get('deposit', 0),
            "withdrawals": stat.get('withdrawal', 0),
            "commissions": stat.get('trade', 0),
        }
        for _date, stat in report.items()
    ]

    return {
        "message": formatted_report
    }
