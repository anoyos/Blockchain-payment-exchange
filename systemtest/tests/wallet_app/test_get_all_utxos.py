from tests.utils.celery import make_celery
from assertpy import assert_that

app = make_celery()


@app.task(name="local-bf-walletrouter.get_all_utxos")
def get_all_utxos(data: dict):
    pass

#def test_get_all_utxos():
#    result = get_all_utxos.apply_async(args=[{'currency_shortname': 'BTC'}],
#                                       queue="local-bullflag-wallet-connector")
#    all_utxos = result.get()
#    print(all_utxos)
#    assert_that(all_utxos).is_length(1)
#    assert_that(all_utxos[0]['address']).is_equal_to("2Mt9HEqTDeymZzEBoxRLNYhVYfvC6zemv1z")
#    assert_that(all_utxos[0]['amount']).is_equal_to(1.00000076)