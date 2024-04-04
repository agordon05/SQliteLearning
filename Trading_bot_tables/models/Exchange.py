import typing

import logging
from decimal import Decimal

from models.Bot import bot as Bot
import datetime
logger = logging.getLogger()

id_count: int = 1


class exchange:
    exchange_type = "Testing"
    def __init__(self,
        ID: int, status: str, exchange_key_id: int, name: str,
        investment_amount: Decimal = Decimal(0),
        available_balance: Decimal = Decimal(0),
        forgotten_profit: Decimal = Decimal(0),
        available_profit: Decimal = Decimal(0),
        timestamp: datetime = None
    ):
        # exchange_type = exchange_t
        self.__ID = ID
        self.__exchange_key_id = exchange_key_id
        # Exchange information
        self.__name = name
        self.__status = status
        if timestamp:
            self.__DoB = timestamp
        else:
            self.__DoB = datetime.datetime.now()  # time the exchange was created

        # balance information
        self.__investment_amount: Decimal = Decimal(investment_amount)  # amount is set by user -- how much from exchange was put into application for use
        self.__available_balance: Decimal = Decimal(available_balance)  # Portion of the total balance that is currently free for new trades or withdrawals -- DOES NOT INCLUDE AVAILABLE BALANCE FROM BOTS--
        self.__forgotten_profit: Decimal = Decimal(forgotten_profit)  # profit no longer in the system or bot's forgotten profit
        self.__available_profit: Decimal = Decimal(available_profit)  # profit that is available to be reinvested or cashed out -- INCLUDES AVAILABLE PROFIT FROM BOTS--

        # Bot information
        self.__bots: [Bot] = []

        self.logs = []

    def get_id(self):
        return self.__ID

    def set_id(self, ID):
        if self.__ID == 0:
            self.__ID = ID

    def set_name(self, name: str):
        self.__name = name

    def set_status(self, status):
        self.__status = status

    def get_name(self) -> str:
        return self.__name

    def get_key_id(self):
        return self.__exchange_key_id

    def get_exchange_type(self) -> str:
        return self.exchange_type

    def get_status(self) -> str:
        return self.__status

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

    def get_investment_amount(self) -> Decimal:
        return self.__investment_amount

    def get_total_balance(self) -> Decimal:
        # Calculate total balance across all bots + exchange's available balance
        amount = self.get_available_balance()
        for bot in self.__bots:
            amount = amount + bot.get_total_balance()
            # amount += bot.get_total_balance()
        return amount

    def get_available_balance(self) -> Decimal:
        # get balance not used by bots
        return self.__available_balance

    def get_total_available_balance(self) -> Decimal:
        amount = self.get_available_balance()
        for bot in self.__bots:
            amount = amount + bot.get_available_balance()
            # amount += bot.get_available_balance()
        return amount

    def get_total_profit(self) -> Decimal:
        # Calculate total profit across all bots
        # amount = self.get_forgotten_profit() + self.get_available_profit()
        amount = self.get_forgotten_profit() + self.get_available_profit()
        for bot in self.__bots:
            amount = amount + bot.get_total_profit()
            # amount += bot.get_total_profit()

        return amount

    def get_total_forgotten_profit(self) -> Decimal:
        amount = self.get_forgotten_profit()
        for bot in self.__bots:
            amount = amount + bot.get_forgotten_profit()
            # amount += bot.get_forgotten_profit()
        return amount

    def get_forgotten_profit(self) -> Decimal:
        return self.__forgotten_profit

    def get_total_available_profit(self) -> Decimal:
        # Calculate available profit across all bots + exchange's available profit
        amount = self.get_available_profit()
        for bot in self.__bots:
            amount = amount + bot.get_available_profit()
            # amount += bot.get_available_profit()
        return amount

    def get_available_profit(self) -> Decimal:
        # get available profit not associated with a bot
        return self.__available_profit

    def get_bot_count(self) -> int:
        count = 0
        for _ in self.__bots:
            count += 1
        return count

    def get_bots(self):
        return self.__bots

    def calculate_pnl(self) -> float:
        total_balance = float(self.get_total_balance())
        forgotten_profit = float(self.get_total_forgotten_profit())
        available_profit = float(self.get_total_available_profit())
        investment_amount = float(self.get_investment_amount())
        if investment_amount == 0:
            return 0

        pnl = ((total_balance + forgotten_profit + available_profit) / investment_amount)
        pnl -= 1
        pnl *= 100

        return pnl

    def add_bot(self, bot: Bot) -> bool:
        if bot.get_investment_amount() <= self.get_available_balance():
            self.__bots.append(bot)
            self.withdraw_from_available_balance(bot.get_investment_amount())
            return True
        return False

    def set_bots(self, bots: [Bot]):
        self.__bots = bots

    def withdraw_from_available_balance(self, amount: Decimal):
        self.__available_balance = self.get_available_balance() - amount
        # self.__available_balance -= amount

    def deposit_into_available_balance(self, amount: Decimal):
        self.__available_balance = self.__available_balance + amount
        # self.__available_balance += amount

    def add_available_profit(self, amount: Decimal):
        self.__available_profit = self.__available_profit + amount
        # self.__available_profit += amount

    def add_cash(self, amount: Decimal):
        self.__investment_amount = self.__investment_amount + amount
        # self.__investment_amount += amount
        self.__available_balance = self.__available_balance + amount
        # self.__available_balance += amount

    def cash_out(self, amount: Decimal):

        # First, drain amount from available profit of exchange
        if amount > self.get_available_profit():
            forgotten_amount = self.__available_profit
            self.__available_profit = Decimal(0)
            self.__forgotten_profit = self.__forgotten_profit + forgotten_amount
            # self.__forgotten_profit += forgotten_amount
            amount = amount - forgotten_amount
            # amount -= forgotten_amount
        else:
            forgotten_amount = amount
            self.__available_profit = self.__available_profit - amount
            # self.__available_profit -= amount
            self.__forgotten_profit = self.__forgotten_profit + forgotten_amount
            # self.__forgotten_profit += forgotten_amount
            amount = Decimal(0)

        # Second, drain amount from available profit of bots
        if amount > 0:
            for bot in self.__bots:
                if amount == 0:
                    break
                elif amount <= bot.get_available_profit():
                    bot.cash_out(amount)
                    amount = Decimal(0)
                elif amount > bot.get_available_profit():
                    forgotten_amount = bot.get_forgotten_profit()
                    bot.cash_out(forgotten_amount)
                    amount = amount - forgotten_amount
                    # amount -= forgotten_amount

        # Third, drain amount from available balance of exchange
        if amount > 0:
            if amount <= self.__available_balance:
                self.__available_balance = self.__available_balance - amount
                # self.__available_balance -= amount
                amount = Decimal(0)
            else:
                forgotten_amount = self.__available_balance
                self.__available_balance = Decimal(0)
                amount = amount - forgotten_amount
                # amount -= forgotten_amount

        # Fourth, drain amount from available balance of bots
        if amount > 0:
            for bot in self.__bots:
                if amount == 0:
                    break
                elif amount <= bot.get_available_balance():
                    bot.cash_out(amount)
                    amount = Decimal(0)
                    break
                elif amount > bot.get_available_balance():
                    forgotten_amount = bot.get_available_balance()
                    bot.cash_out(forgotten_amount)
                    amount = amount - forgotten_amount
                    # amount -= forgotten_amount
        # else:
        #     raise Exception(f"Cash out is greater than available USDT funds -- ${amount}")

        if amount != Decimal(0):
            raise Exception(f"Cash out is greater than available USDT funds -- ${amount}")

    # def place_order(self, contract: Contract, order_type: str, quantity: float, side: str, price=None, tif=None) -> OrderStatus:
    #     pass

    def __str__(self):
        return (f"Exchange(ID={self.get_id()}, status={self.get_status()}, "
                f"exchange_key_id={self.get_key_id()}, "
                f"name={self.__name}, investment_amount={self.get_investment_amount()}, "
                f"available_balance={self.get_available_balance()}, "
                f"forgotten_profit={self.get_forgotten_profit()}, "
                f"available_profit={self.get_available_profit()}, "
                f"timestamp={self.get_timestamp()})")
