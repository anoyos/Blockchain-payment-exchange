from api_contrib.crud.base_mongo import CRUDBaseMongo

from app.models.blockchain import LastReadBlock, SystemAccount, UserContracts
from app.models.asset import Asset
from app.models.wallet import (Wallet,
                               ProcessedTransaction,
                               DepositAddresses,
                               Transaction,
                               LastPrices,
                               TxFees,
                               FavoritesAssets)
from .deposit import CRUDDeposit
from .asset import CRUDAsset
from .transactions import CRUDTransaction, CRUDBlocks, CRUDAccount

wallet = CRUDBaseMongo(Wallet)
asset = CRUDAsset(Asset)
processed_tran = CRUDBaseMongo(ProcessedTransaction)
deposit_addresses = CRUDDeposit(DepositAddresses)
transaction = CRUDTransaction(Transaction)
favorites_assets = CRUDBaseMongo(FavoritesAssets)
last_prices = CRUDBaseMongo(LastPrices)
blocks = CRUDBlocks(LastReadBlock)
system_account = CRUDAccount(SystemAccount)
user_contracts = CRUDBaseMongo(UserContracts)
tx_fees = CRUDBaseMongo(TxFees)
