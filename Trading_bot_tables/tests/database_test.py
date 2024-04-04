import unittest
from decimal import Decimal

from models.Bot import bot
from models.Exchange import exchange
from models.Contract import contract
from models.Trade import trade
import database


class Test_Database(unittest.TestCase):

    def test_create_database(self):
        """
                ---WHAT IS BEING TESTED ---
        testing to see tables exist as well as initial data
        Tables:
            Timeframe
            Status
            Exchange_Type
            Strategy_Type
            Grid_Strategy_Param
            Strategy_Param_Link
            Strategy_Settings
            Exchange_Keys
            Contract
            Exchange
            Bot
            Trade
        Base Data:
            Timeframe:
                length -> 6
            Status:
                length -> 12
            Exchange_Type:
                length -> 2
            Strategy_Type:
                length -> 2
            Grid_Strategy_Param:
                length -> 0
            Strategy_Param_Link:
                length -> 1
            Strategy_Settings:
                length -> 1
            Exchange_Keys:
                length -> 0
            Contract:
                length -> 0
            Exchange:
                length -> 0
            Bot:
                length -> 0
            Trade:
                length -> 0

        :return:
        """
        database.create_tables()

        num = len(database.get_all_tfs())
        self.assertEqual(num, 6, f"Expected 6 Timeframes but was {num}")
        num = len(database.get_all_statuses())
        self.assertEqual(num, 12, f"Expected 12 Status\' but was {num}")
        num = len(database.get_all_exchange_types())
        self.assertEqual(num, 2, f"Expected 2 exchange types but was {num}")

        num = len(database.get_all_strategy_types())
        self.assertEqual(num, 2, f"Expected 2 strategy types but was {num}")

        num = len(database.get_all_grid_strategy_params())
        self.assertEqual(num, 0, f"Expected 0 strategy params but was {num}")

        num = len(database.get_all_strategy_param_links())
        self.assertEqual(num, 0, f"Expected 0 param links but was {num}")

        num = len(database.get_all_strategy_settings())
        self.assertEqual(num, 1, f"Expected 1 strategy settings but was {num}")

        num = len(database.get_all_exchange_keys())
        self.assertEqual(num, 0, f"Expected 0 exchange keys but was {num}")

        num = len(database.get_all_contracts())
        self.assertEqual(num, 0, f"Expected 0 contracts but was {num}")

        num = len(database.get_all_exchanges())
        self.assertEqual(num, 0, f"Expected 0 exchanges but was {num}")

        num = len(database.get_all_bots())
        self.assertEqual(num, 0, f"Expected 0 bots but was {num}")

        num = len(database.get_all_trades())
        self.assertEqual(num, 0, f"Expected 0 trades but was {num}")

        database.close()

    def test_exchange_db(self):
        """
                ---WHAT IS BEING TESTED ---
        create exchange
        add to database
        edit exchange

        edit should not change any foreign keys, name, ID or timestamp
        get exchange should create a exchange object using exchange type -- "Testing" -- Exchange, "Binance US" -- Binance_Client
        get all should not return a list of tuples
        no foreign keys should be nullable
        :return:
        """
        pass

    def test_bot_db(self):
        """
                ---WHAT IS BEING TESTED ---
        create bot
        add to database
        edit bot

        edit should not change any foreign keys, name, ID or timestamp
        get Bot should create a Bot object using strategy type -- "Testing" -- Bot, "Grid Strategy" -- Grid_Strategy
        get all should not return a list of tuples
        no foreign keys should be nullable
        :return:
        """
        pass

    def test_trade_db(self):
        """
                ---WHAT IS BEING TESTED ---
        create trade
        add to database
        edit trade

        trade should not be able to be edited if trade status is FILLED
        invalid status' include Pending, Active, Closing, Closed, Suspended, Inactive
        get trade should return a trade object
        get all should not return a list of tuples
        no foreign keys should be nullable

        :return:
        """
        pass

    def test_contract_db(self):
        """
                ---WHAT IS BEING TESTED ---
        create contract
        add to database

        contract should not be able to be edited
        contracts can have null values
        information filled in contract object should be related to exchange_type
        no foreign keys should be nullable

        :return:
        """
        pass


