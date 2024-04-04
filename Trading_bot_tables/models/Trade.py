from datetime import datetime
from decimal import Decimal

from models.Contract import contract as Contract


class trade:
    def __init__(self, trade_info):
        # ID, Fake, Exchange ID, Strategy ID, Associated ID, Status, Contract, Type, Side, Position Side, Price, Quantity, Time
        self.entry_id = trade_info['ID']
        self.is_fake = trade_info['Fake']
        self.exchange_id = trade_info['Exchange ID']
        self.bot_id = trade_info['Bot ID']
        self.associated_id = trade_info['Associated ID']

        self.status: str = trade_info['Status']
        self.contract: Contract = trade_info['Contract']
        self.contract_id = trade_info['Contract ID']
        self.orderType = trade_info['Order Type']
        self.side: str = trade_info['Side']
        self.positionSide: str = trade_info['Position Side']
        self.price: Decimal = Decimal(trade_info['Price'])
        self.quantity: Decimal = Decimal(trade_info['Quantity'])
        self.time: datetime = trade_info['Time']

    def get_status(self):
        return self.status

    def get_side(self):
        return self.side

    def get_position_side(self):
        return self.positionSide

    def get_market(self):
        print(f"Trade.get_market() Symbol: {self.contract.symbol}")
        print(f"Trade.get_market() Base Asset: {self.contract.base_asset}")
        print(f"Trade.get_market() Quote Asset: {self.contract.quote_asset}")
        return self.contract.symbol

    def get_entry_price(self):
        return self.price

    def get_crypto_amount(self):
        return self.quantity

    def get_date(self):
        return self.time.strftime("%m/%d/%Y")

    def get_time(self):
        return self.time.strftime("%I:%M:%S %p")

    def update(self, trade):
        self.status: str = trade.get_status()
        self.price: Decimal = trade.get_entry_price()
        self.quantity: Decimal = trade.get_crypto_amount()
        self.time: datetime = trade.get_time()

# ID, Fake, Exchange ID, Strategy ID, Associated ID, Status, Contract, Type, Side, Position Side, Price, Quantity, Time
def to_trade_dict(ID, fake, exchange_id, strategy_id, ass_id, status, contract, order_type, side, pos_side, price, quantity, time):
    trade_info = {
        'ID': ID,
        'Fake': fake,
        'Exchange ID': exchange_id,
        'Strategy ID': strategy_id,
        'Associated ID': ass_id,
        'Status': status,
        'Contract': contract,
        'Order Type': order_type,
        'Side': side,
        'Position Side': pos_side,
        'Price': price,  # USDT
        'Quantity': quantity,  # Crypto
        'Time': time
    }
    return trade_info
