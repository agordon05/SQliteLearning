
# exchange_types = ["Bitmex (unimplemented)", "Binance Futures (Unimplemented)", "Binance US (Testing)", "Coinbase (unimplemented)", "Testing"]

class contract:
    def __init__(self, contract_info, exchange):

        if exchange == ui_settings.exchange_types[0]:  # Bitmex
            self.symbol = contract_info['symbol']
            self.base_asset = contract_info['rootSymbol']
            self.quote_asset = contract_info['quoteCurrency']
            self.price_decimals = util.tick_todecimals(contract_info['tickSize'])
            self.quantity_decimals = util.tick_todecimals(contract_info['lotSize'])
            self.tick_size = contract_info['tickSize']
            self.lot_size = contract_info['lotSize']

            self.quanto = contract_info['isQuanto']
            self.inverse = contract_info['isInverse']

            self.multiplier = contract_info['multiplier'] * util.BITMEX_MULTIPLIER

            if self.inverse:
                self.multiplier *= -1

        elif exchange == ui_settings.exchange_types[1]:  # Binance Futures
            self.symbol = contract_info['symbol']
            self.base_asset = contract_info['baseAsset']
            self.quote_asset = contract_info['quoteAsset']
            self.price_decimals = contract_info['pricePrecision']
            self.quantity_decimals = contract_info['quantityPrecision']
            self.tick_size = 1 / pow(10, contract_info['pricePrecision'])
            self.lot_size = 1 / pow(10, contract_info['quantityPrecision'])

        elif exchange == ui_settings.exchange_types[2]:  # Binance US
            self.symbol = contract_info['symbol']
            self.base_asset = contract_info['baseAsset']
            self.quote_asset = contract_info['quoteAsset']
            self.price_decimals = contract_info['quoteAssetPrecision']  # ???
            self.quantity_decimals = contract_info['baseAssetPrecision']  # ???


        self.exchange = exchange
