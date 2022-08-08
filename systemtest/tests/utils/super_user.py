import MySQLdb
from MySQLdb import _mysql
from pymongo import MongoClient

mongo_client = MongoClient(
    "mongodb://127.0.0.1:27017,127.0.0.1:27018/?authSource=admin",
    username="root",
    password="root_password123"
)


def make_me_admin(username: str):
    db = _mysql.connect(host="127.0.0.1", port=3306, user="root", passwd="master_root_password", db="auth")
    db.query("""UPDATE user SET is_admin=1 WHERE username='{}' OR email='{}'""".format(username, username))


def get_db():
    return MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="master_root_password", db="auth")


def delete_all_users():
    db = get_db()
    cur = db.cursor()
    cur.execute("""DELETE FROM user""")
    cur.execute("""DELETE FROM user_iplog""")
    cur.execute("""DELETE FROM user_referral_codes""")
    cur.execute("""DELETE FROM user_secrets""")
    cur.execute("""DELETE FROM user_temp""")
    db.commit()
    print("Deleted all users from mysql db")


def delete_user(username_or_email: str):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        """SELECT userid FROM user WHERE username='{}' OR email='{}'""".format(username_or_email, username_or_email)
    )
    try:
        user_id = cur.fetchone()[0]
        cur.execute("""DELETE FROM user WHERE userid=\"{}\"""".format(user_id))
        cur.execute("""DELETE FROM user_iplog WHERE userid='{}'""".format(user_id))
        cur.execute("""DELETE FROM user_referral_codes WHERE userid='{}'""".format(user_id))
        cur.execute("""DELETE FROM user_secrets WHERE userid='{}'""".format(user_id))
        cur.execute("""DELETE FROM user_temp WHERE userid='{}'""".format(user_id))
        db.commit()
    except Exception:
        print(f"delete_user did not manage to delete any user from db, for username/email {username_or_email}")

        return


def get_userid(username_or_email: str):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """select userid FROM user WHERE username='{}' OR email='{}'""".format(username_or_email, username_or_email)
    )
    try:
        userid = cur.fetchone()[0]
        return userid
    except Exception:
        print(f"get_user did not manage to find any user from db for username/email {username_or_email}")


def get_wallets_by_userid_and_asset_id(userid, asset_id: str):
    wallet_ids = list(mongo_client['wallet_db']['deposit_addresses'].find({"user_id": userid, "asset_id": asset_id}))
    return wallet_ids


def delete_all_wallets():
    mongo_client['wallet_db']['deposit_addresses'].delete_many({})
    print(f"Deleted all wallets from mongo db")


def delete_all_ledger():
    mongo_client['balance_db']['ledger'].delete_many({})
    print(f"Deleted all ledger from mongo db")


def delete_all_trollbox():
    mongo_client['trollbox_db']['rooms'].delete_many({})
    mongo_client['trollbox_db']['history'].delete_many({})
    print(f"Deleted all trollbox rooms and history from mongo db")


def delete_all_markets():
    mongo_client['market_db']['markets'].delete_many({})
    print(f"Deleted all markets from mongo db")


def delete_all_blockchain_router_data():
    mongo_client['blockchain_router_db']['known_block'].delete_many({})


def set_base_asset(asset_short_name: str, is_base: bool):
    mongo_client['wallet_db']['wallet_settings'].update_one(
        {'asset_short_name': asset_short_name},
        {
            '$set':
                {'is_base_asset': is_base}
        }
    )


def get_transactions_from_db():
    transactions = mongo_client['balance_db']['ledger'].find()
    return list(transactions)


def delete_all():
    delete_all_users()
    delete_all_markets()
    delete_all_wallets()
    delete_all_ledger()
    delete_all_trollbox()
    print(f"Deleted everything in databases")
