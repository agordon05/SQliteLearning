import datetime
import time
from decimal import Decimal
from threading import Timer

from models.Contract import contract as Contract
from models.Trade import trade as Trade

import logging
from typing import *

logger = logging.getLogger()

if TYPE_CHECKING:

    from models.Exchange import exchange


# --- ALSO KNOWN AND ASSOCIATED AS BOT ---
class bot:
    strategy_type = "Testing"  # Testing

    # trade_history: [Trade] = None
    def __init__(self, client: Union["exchange"], contract: Contract,
                 name: str,
                 strategy_type: str,
                 strategy, market: str, trade_history: [Trade] = None,
                 total_crypto: str = "0", investment_amount: str = "0", available_balance: str = "0",
                 forgotten_profit: str = "0", available_profit: str = "0", tf: str = "1h"):
        # Store the BinanceFuturesClient instance used for communication
        self.__ID = 0
        self.contract_id = 0
        self.settings_id = 0

        self.client = client

        # User information
        self.__name = name
        self.__status = "Pending"
        self.__DoB = datetime.datetime(2023, 1, 1)  # time the exchange was created
        # self.__strategy_type = strategy_type
        self.__market = market
        self.tf = tf
        # self.__balance = balance(usdt)
        self.__strategy = strategy

        # balance information
        self.__total_crypto: Decimal = Decimal(total_crypto)
        self.__investment_amount: Decimal = Decimal(
            investment_amount)  # amount is set by user -- how much from exchange was put into the strategy
        # self.__total_balance = usdt  # available_balance + crypto amount's value in USDT
        self.__available_balance: Decimal = Decimal(
            available_balance)  # Portion of the total balance that is currently free for new trades or withdrawals
        self.__forgotten_profit: Decimal = Decimal(forgotten_profit)
        self.__available_profit: Decimal = Decimal(available_profit)

        # Store trades associated with the bot
        # self.__associated_trades: [associated_trades] = []

        # Store contract information, exchange, timeframe, balance percentage, and strategy parameters
        self.contract = contract

        # else:
            # self.trades: [Trade] = []

        self.logs = []

    def get_id(self):
        return self.__ID

    def get_name(self) -> str:
        return self.__name

    def get_status(self) -> str:
        return self.__status

    def set_status(self, status: str):
        self.__status = status

    def set_status_to_testing(self):
        self.__status = "Test"

    def get_tf(self):
        return self.tf

    def get_strategy_type(self):
        return self.strategy_type

    def get_strategy(self):
        return self.__strategy

    def get_market(self):
        return self.__market

    def get_timestamp(self):
        return self.__DoB

    def get_age(self):
        current_date = datetime.datetime.now()
        age = current_date - self.__DoB

        years = age.days // 365
        months = (age.days % 365) // 30
        weeks = ((age.days % 365) % 30) // 7
        days = ((age.days % 365) % 30) % 7
        hours, remainder = divmod(age.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        age_components = {
            'Y': years,
            'M': months,
            'W': weeks,
            'D': days,
            'H': hours,
            'm': minutes,
            's': seconds
        }

        # Define the sorting order
        sorting_order = ['Y', 'M', 'W', 'D', 'H', 'm', 's']

        # Filter out components with value 0
        non_zero_components = {k: v for k, v in age_components.items() if v != 0}

        # Sort the non-zero components based on the defined order
        sorted_components = {k: non_zero_components[k] for k in sorting_order if k in non_zero_components}

        # Choose the top three components
        top_three_components = dict(
            sorted(sorted_components.items(), key=lambda item: sorting_order.index(item[0]))[:3])

        # Convert the result to a string
        output = ' '.join(f"{value}{key}" for key, value in top_three_components.items())

        return output

    def get_total_crypto(self) -> Decimal:
        return self.__total_crypto

    def get_investment_amount(self) -> Decimal:
        return self.__investment_amount

    def get_total_balance(self) -> Decimal:
        return self.get_available_balance() + self.get_current_usdt_value()
        # return add(self.get_available_balance(), self.get_current_usdt_value())  # + self.get_available_profit()

    def get_current_usdt_value(self):
        return self.__total_crypto * Decimal("78")
        # return multiply(self.__total_crypto, 78)

    def get_available_balance(self) -> Decimal:
        return self.__available_balance

    def get_total_profit(self) -> Decimal:
        # total_profit = subtract(self.get_total_balance(), self.get_investment_amount())
        # total_profit = add(total_profit, self.get_forgotten_profit())
        # total_profit = add(total_profit, self.get_available_profit())
        return self.get_total_balance() - self.get_investment_amount() + self.get_forgotten_profit() + self.get_available_profit()
        # return total_profit

    def get_forgotten_profit(self) -> Decimal:
        return self.__forgotten_profit

    def get_available_profit(self) -> Decimal:
        return self.__available_profit

    def calculate_pnl(self) -> float:
        total_balance = float(self.get_total_balance())
        forgotten_profit = float(self.get_forgotten_profit())
        available_profit = float(self.get_available_profit())
        investment_amount = float(self.get_investment_amount())

        if investment_amount == 0:
            return 0

        total_amount = total_balance + forgotten_profit + available_profit
        # total_amount = self.get_total_balance() + self.get_forgotten_profit() + self.get_available_profit()
        # pnl = total_amount / self.get_investment_amount()
        pnl = total_amount / investment_amount
        pnl -= 1
        pnl *= 100
        return pnl

    def withdraw_from_available_balance(self, amount: Decimal):
        print("Withdraw from balance")
        self.__available_balance: Decimal = self.__available_balance - amount
        # self.__available_balance = subtract(self.__available_balance, amount)
        # self.__available_balance -= amount

    def deposit_into_available_balance(self, amount: Decimal):
        self.__available_balance: Decimal = self.__available_balance + amount
        # self.__available_balance += amount

    def add_crypto(self, amount: Decimal):
        self.__total_crypto += amount
        # self.__total_crypto += amount

    def remove_crypto(self, amount: Decimal):
        print("remove crypto")
        self.__total_crypto -= amount

    def add_available_profit(self, amount: Decimal):
        self.__available_profit += amount
        # self.__available_profit += amount

    def add_cash(self, amount: Decimal):
        self.__investment_amount += amount
        self.__available_balance += amount
        # self.__investment_amount += amount
        # self.__available_balance += amount

    def add_forgotten_profit(self, amount: Decimal):
        self.__forgotten_profit += amount
        # self.__forgotten_profit += amount

    def cash_out(self, amount: Decimal):

        # remove amount from available profit
        if amount > self.get_available_profit():
            forgotten_amount: Decimal = self.get_available_profit()
            self.__available_profit = Decimal(0)
            self.__forgotten_profit = self.__forgotten_profit + forgotten_amount
            # self.__forgotten_profit += forgotten_amount
            amount = amount - forgotten_amount
            # amount -= forgotten_amount
        elif amount <= self.get_available_profit():
            self.__available_profit = self.__available_profit - amount
            # self.__available_profit -= amount
            self.__forgotten_profit = self.__forgotten_profit + amount
            # self.__forgotten_profit += amount
            amount = Decimal(0)

        # Remove amount from available balance
        if amount > self.get_available_balance():
            forgotten_amount = self.get_available_balance()
            self.__available_balance = Decimal(0)
            amount = amount - forgotten_amount
            # amount -= forgotten_amount
        elif amount <= self.get_available_balance():
            self.__available_balance = self.__available_balance - amount
            # self.__available_balance -= amount

        if amount != 0:
            raise Exception("Strategy Balance overdrawn")
