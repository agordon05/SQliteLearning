import time
from decimal import Decimal

import database
# Press the green button in the gutter to run the script.
from models.Exchange import exchange

if __name__ == '__main__':
    database.create_tables()
    # print(database.get_all_tfs())
    # print(database.get_all_statuses())
    # print(database.get_all_exchange_types())
    # print(database.get_all_strategy_types())
    # # database.get_all_tfs()
    # tf_id = database.get_tf_id('15m')
    # print(tf_id)
    # tf = database.get_tf(tf_id)
    # print(tf)
    # exchange_types = database.get_all_exchange_types()
    statuses = database.get_all_statuses()
    # print(exchange_types)
    print(statuses)
    ex = exchange(0, statuses[0], 0, "Testing Exchange", investment_amount=Decimal("13"), available_balance=Decimal("12.31"), forgotten_profit=Decimal("1.123"), available_profit=Decimal("0.69"))
    print("created exchange")
    ex_id = database.add_exchange(ex)
    print("added exchange")
    ex.set_id(ex_id)
    print(ex_id)
    print("getting exchanges")
    ex_list = database.get_all_exchanges()
    for exchange in ex_list:
        print(exchange)
    ex.add_cash(Decimal("23"))
    print(f"available balance: {ex.get_available_balance()}")
    database.update_exchange(ex)
    ex_list = database.get_all_exchanges()
    for exchange in ex_list:
        print(exchange)

    database.close()