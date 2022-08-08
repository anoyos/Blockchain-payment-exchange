from app import app
from connectors.v2.wallet import celery_Wallet


def load_wallet_info(basecurrencyid, currencyid):
    wc = celery_Wallet()

    result = wc.c.get_wallet_profile.apply_async(
        args=[{'currencyid': str(basecurrencyid)}], queue=app.config['Q_WALLET_CONN'])
    try:
        basecurrency = result.get(5)
    except Exception as exc:
        print("Failed: {}".format(exc))
        return {"status": "fail", "message": "ERR_WC_UNAVAILABLE"}, 200

    print(basecurrency)
    result = wc.c.is_base_wallet.apply_async(
        args=[{
            'currencyid': basecurrency['currencyid'],
            'fromaddmarket': True
        }], queue=app.config['Q_WALLET_CONN'])
    try:
        is_basecurrency = result.get(5)
        if not is_basecurrency:
            raise Exception("Not a valid basecurrency")
    except Exception as exc:
        print("Failed: {}".format(exc))
        return {"status": "fail", "message": "ERR_WC_UNAVAILABLE"}, 200

    result = wc.c.get_wallet_profile.apply_async(
        args=[{'currencyid': str(currencyid)}], queue=app.config['Q_WALLET_CONN'])
    try:
        currency = result.get(5)
    except Exception as exc:
        print("Failed: {}".format(exc))
        return {"status": "fail", "message": "ERR_WC_UNAVAILABLE"}, 200
    print(currency)
    return basecurrency, currency
