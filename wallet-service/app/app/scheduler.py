from apscheduler.schedulers.blocking import BlockingScheduler
from prometheus_client.exposition import start_http_server

from app.blockchain.handlers.bitcoinlib import background as btc_background
from app.blockchain.handlers.ethereum import background as eth_background
from app.stat import prices, fees

if __name__ == '__main__':
    start_http_server(80)

    scheduler = BlockingScheduler()
    scheduler.add_job(btc_background.send_new_transaction_to_ledger, 'interval', minutes=1, name='process_btc_in')
    scheduler.add_job(eth_background.send_new_transaction_to_ledger,
                      'interval',
                      minutes=1,
                      name='scan ethereum networks')
    scheduler.add_job(prices.update_btc_price, 'interval', minutes=1, name='update_btc_price')
    scheduler.add_job(fees.update_withdrawal_fee, 'interval', minutes=480, name='update_tx_fees')
    scheduler.add_job(eth_background.new_contracts_for_deposit, 'interval', minutes=1, name='new_contracts_for_deposit')

    scheduler.start()
