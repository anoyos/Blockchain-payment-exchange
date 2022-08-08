from app import crud
from app.models.balance import BalanceSettings


def add_new_field():
    for bal in crud.balance.find_all_sync({}):
        crud.balance.update_sync(bal, {
            "settings": BalanceSettings().dict()
        })


if __name__ == '__main__':
    add_new_field()
