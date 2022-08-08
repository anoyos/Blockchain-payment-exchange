from api_contrib.crud.base_mongo import CRUDBaseMongo
from app.models.balance import Balance
from app.models.entry import Entry
from app.models.withdrawal import Withdrawal
from app.models.deposit import Deposit
from .balance import CRUDBalance
from .entry import CRUDEntry


balance = CRUDBalance(Balance)
entry = CRUDEntry(Entry)
withdrawal = CRUDBaseMongo(Withdrawal)
deposit = CRUDBaseMongo(Deposit)


