from uuid import uuid4

from tests.utils.celery import make_celery

app = make_celery()


@app.task(name="local-bf-wallet-walletrouter.withdrawal")
def withdrawal(data):
    pass

asset_id = uuid4()

w_list = [
    {
        "asset_id": asset_id,
        "userid": uuid4(),
        "withdrawalid": uuid4(),
        "target_address": "tb1qdaexecacvwwkdz6g28gn2rha9zkrl6nx4p6ty5",
        "amount": 0.00001
    }
]

withdrawal_batch = {
    "live_run": True,
    "batch_id": uuid4(),
    "asset": "BTC",
    "asset_id": asset_id,
    "asset_name": "BITCOIN",
    "w_list": w_list
}

#def test_withdrawal():
#    result = withdrawal.apply_async(args=[withdrawal_batch],
#                                       queue="local-bullflag-wallet-connector")
#    print(result.get())
