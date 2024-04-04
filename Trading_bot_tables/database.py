import datetime
import sqlite3

from models.Exchange import exchange

conn = sqlite3.connect(':memory:')
# conn = sqlite3.connect('database.db')

c = conn.cursor()


def create_tables():
    with conn:
        c.execute(
            """CREATE TABLE IF NOT EXISTS Timeframe (
            ID INTEGER PRIMARY KEY,
            Timeframe TEXT UNIQUE
            )""")
        c.execute(
            """CREATE TABLE IF NOT EXISTS Status (
            ID INTEGER PRIMARY KEY,
            Status TEXT UNIQUE
            )""")
        c.execute(
            """CREATE TABLE IF NOT EXISTS Exchange_Type (
            ID INTEGER PRIMARY KEY,
            Exchange_Type TEXT UNIQUE
            )""")
        c.execute(
            """CREATE TABLE IF NOT EXISTS Strategy_Type (
            ID INTEGER PRIMARY KEY,
            Strategy_Type TEXT UNIQUE
            )""")
        c.execute(
            """CREATE TABLE IF NOT EXISTS Grid_Strategy_Param (
            ID INTEGER PRIMARY KEY,
            Stop_Loss TEXT,
            Take_Profit TEXT,
            Upper TEXT,
            Lower TEXT,
            Number_of_Intervals INTEGER,
            Trade_Size TEXT
            )""")
        c.execute(
            """CREATE TABLE IF NOT EXISTS Strategy_Param_Link (
            ID INTEGER PRIMARY KEY,
            Strategy_Type_ID INTEGER,
            Params_ID INTEGER,
            FOREIGN KEY (Strategy_Type_ID) REFERENCES Strategy_Type(ID)
            )""")
        c.execute(
            """CREATE TABLE IF NOT EXISTS Strategy_Settings (
            ID INTEGER PRIMARY KEY,
            Link_ID INTEGER,
            Growth_Rate TEXT,
            FOREIGN KEY (Link_ID) REFERENCES Strategy_Param_Link(ID)
            )""")
        c.execute(
            """CREATE TABLE IF NOT EXISTS Exchange_Keys (
            ID INTEGER PRIMARY KEY,
            Exchange_Type_ID INTEGER,
            Public_Key TEXT,
            Private_Key TEXT,
            UNIQUE (Public_Key, Private_Key),
            FOREIGN KEY (Exchange_Type_ID) REFERENCES Exchange_Type(ID)
            )""")
        c.execute(
            """CREATE TABLE IF NOT EXISTS Contract (
            ID INTEGER PRIMARY KEY,
            Exchange_Type_ID INTEGER,
            Symbol Text,
            Base_Asset TEXT,
            Quote_Asset TEXT,
            Price_Decimals TEXT,
            Quantity_Decimals TEXT,
            Tick_Size TEXT,
            Lot_Size TEXT,
            Quanto TEXT,
            Inverse TEXT,
            Multiplier TEXT,
            FOREIGN KEY (Exchange_Type_ID) REFERENCES Exchange_Type(ID)
            )""")

        c.execute(
            """CREATE TABLE IF NOT EXISTS Exchange (
            ID INTEGER PRIMARY KEY,
            Exchange_Type_ID INTEGER,
            Status_ID INTEGER,
            Key_ID INTEGER,
            Name TEXT UNIQUE,
            Investment_Amount TEXT,
            Available_Balance TEXT,
            Forgotten_Profit TEXT,
            Available_Profit TEXT,
            Time_Stamp TEXT,
            FOREIGN KEY (Exchange_Type_ID) REFERENCES Exchange_Type(ID),
            FOREIGN KEY (Status_ID) REFERENCES Status(ID),
            FOREIGN KEY (Key_ID) REFERENCES Exchange_Keys(ID)
            )""")

        c.execute(
            """CREATE TABLE IF NOT EXISTS Bot (
            ID INTEGER PRIMARY KEY,
            Exchange_ID INTEGER,
            Status_ID INTEGER,
            Contract_ID INTEGER,
            Strategy_ID INTEGER,
            Settings_ID INTEGER,
            Name TEXT UNIQUE,
            Investment_Amount TEXT,
            Total_Balance TEXT,
            Available_Balance TEXT,
            Total_Crypto TEXT,
            Forgotten_Profit TEXT,
            Available_Profit TEXT,
            TimeStamp TEXT,
            FOREIGN KEY (Exchange_ID) REFERENCES Exchange(ID),
            FOREIGN KEY (Status_ID) REFERENCES Status(ID),
            FOREIGN KEY (Contract_ID) REFERENCES Contract(ID),
            FOREIGN KEY (Strategy_ID) REFERENCES Strategy_Type(ID),
            FOREIGN KEY (Settings_ID) REFERENCES Strategy_Settings(ID)
            )""")
        c.execute(
            """CREATE TABLE IF NOT EXISTS Trade (
            ID INTEGER PRIMARY KEY,
            Associated_ID INTEGER, -- Nullable column
            Exchange_ID INTEGER,
            Contract_ID INTEGER,
            Status_ID INTEGER,
            Bot_ID INTEGER,
            Side TEXT CHECK(Side IN ('Buy', 'Sell')),
            Position_Side TEXT CHECK(Position_Side IN ('long', 'short')),
            USDT TEXT,
            Crypto TEXT,
            Time_Stamp TEXT,
            FOREIGN KEY (Associated_ID) REFERENCES Trade(ID),
            FOREIGN KEY (Exchange_ID) REFERENCES Exchange(ID),
            FOREIGN KEY (Contract_ID) REFERENCES Contract(ID),
            FOREIGN KEY (Status_ID) REFERENCES Status(ID),
            FOREIGN KEY (Bot_ID) REFERENCES Bot(ID)
            )""")
    create_default_data()


def create_default_data():
    with conn:
        c.execute("SELECT EXISTS(SELECT 1 FROM Timeframe)")
        check = c.fetchone()
        if not check[0]:
            __add_time_frame('1m')
            __add_time_frame('5m')
            __add_time_frame('15m')
            __add_time_frame('30m')
            __add_time_frame('1h')
            __add_time_frame('4h')

        c.execute("SELECT EXISTS(SELECT 1 FROM Status)")
        check = c.fetchone()
        if not check[0]:
            __add_status('Pending')
            __add_status('Active')
            __add_status('Closing')
            __add_status('Suspended')
            __add_status('Inactive')
            __add_status('Closed')
            __add_status('Test')
            __add_status('NEW')
            __add_status('PARTIAL')
            __add_status('FILLED')
            __add_status('CANCELLED')
            __add_status('REJECTED')

        c.execute("SELECT EXISTS(SELECT 1 FROM Exchange_Type)")
        check = c.fetchone()
        if not check[0]:
            __add_exchange_type('Testing')
            __add_exchange_type('Binance US')

        c.execute("SELECT EXISTS(SELECT 1 FROM Strategy_Type)")
        check = c.fetchone()
        if not check[0]:
            testing_id = __add_strategy_type('Testing')
            __add_strategy_type('Grid Strategy')


        c.execute("SELECT EXISTS(SELECT 1 FROM Strategy_Settings)")
        check = c.fetchone()
        if not check[0]:
            add_strategy_settings(testing_id, 0)




"""
||||||||||||||||||
|||||  GET   |||||
||||||||||||||||||
||||||||||||||||||
"""


def __get(SELECT: str = "*", FROM: str = None, WHERE: str = None, WHERE_VALUE = None, fetch_all: bool = False):
    if not FROM:
        return
    data: any
    with conn:
        if WHERE and WHERE_VALUE:
            c.execute(f"SELECT {SELECT} FROM {FROM} WHERE {WHERE}", WHERE_VALUE)
            if fetch_all:
                data = c.fetchall()
            else:
                data = c.fetchone()
        else:
            c.execute(f"SELECT {SELECT} FROM {FROM}")
            if fetch_all:
                data = c.fetchall()
            else:
                data = c.fetchone()

    return data


def __get_single_item(SELECT: str = "*", FROM: str = None, WHERE: str = None, WHERE_VALUE = None, fetch_all: bool = False):
    value = __get(SELECT=SELECT, FROM=FROM, WHERE=WHERE, WHERE_VALUE=WHERE_VALUE, fetch_all=fetch_all)
    if value:
        return value[0]
    return None


def __get_single_item_list(SELECT: str = "*", FROM: str = None, WHERE: str = None, WHERE_VALUE = None, fetch_all: bool = False):
    data = []
    value = __get(SELECT=SELECT, FROM=FROM, WHERE=WHERE, WHERE_VALUE=WHERE_VALUE, fetch_all=fetch_all)
    if value:
        for tf in value:
            data.append(tf[0])
        return data
    return data


def get_all_tfs():
    return __get_single_item_list(SELECT="Timeframe", FROM="Timeframe", fetch_all=True)


def get_tf_id(tf):
    return __get_single_item(SELECT="ID", FROM="Timeframe", WHERE="Timeframe=(?)", WHERE_VALUE=(tf,))


def get_tf(ID):
    return __get_single_item(SELECT="Timeframe", FROM="Timeframe", WHERE="ID=(?)", WHERE_VALUE=(ID,))


def get_all_statuses():
    return __get_single_item_list(SELECT="Status", FROM="Status", fetch_all=True)


def get_status_id(status):
    return __get_single_item(SELECT="ID", FROM="Status", WHERE="Status=(?)", WHERE_VALUE=(status,))


def get_status(ID):
    return __get_single_item(SELECT="Status", FROM="Status", WHERE="ID=(?)", WHERE_VALUE=(ID,))


def get_all_exchange_types():
    return __get_single_item_list(SELECT="Exchange_Type", FROM="Exchange_type", fetch_all=True)


def get_exchange_type_id(exchange_type):
    return __get_single_item(SELECT="ID", FROM="Exchange_Type", WHERE="Exchange_Type=(?)", WHERE_VALUE=(exchange_type,))


def get_exchange_type(ID):
    return __get_single_item(SELECT="Exchange_Type", FROM="Exchange_Type", WHERE="ID=(?)", WHERE_VALUE=(ID,))


def get_all_exchange_settings():
    # return __get_single_item_list(SELECT="Exchange_Settings", FROM="Exchange_Settings", fetch_all=True)
    data: []
    with conn:
        c.execute("SELECT Exchange_Settings FROM Exchange_Settings")
        data = c.fetchall()
        
    return data


def get_exchange_setting(ID):
    data: any
    with conn:
        c.execute("SELECT Exchange_Settings FROM Exchange_Settings where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_all_strategy_types():
    return __get_single_item_list(SELECT="Strategy_Type", FROM="Strategy_Type", fetch_all=True)


def get_strategy_type_id(strategy_type):
    return __get_single_item(SELECT="ID", FROM="Strategy_Type", WHERE="Strategy_Type=(?)", WHERE_VALUE=(strategy_type,))

    # data: any
    # with conn:
    #     c.execute("SELECT ID FROM Strategy_Type where Strategy_Type=(?)", (strategy_type,))
    #     data = c.fetchone()
    #     
    # return data


def get_strategy_type(ID):
    return __get_single_item(SELECT="Strategy_Type", FROM="Strategy_Type", WHERE="ID=(?)", WHERE_VALUE=(ID,))

    # data: any
    # with conn:
    #     c.execute("SELECT Strategy_Type FROM Strategy_Type where ID=(?)", (ID,))
    #     data = c.fetchone()
    #     
    # return data


def get_all_grid_strategy_params():
    data: []
    with conn:
        c.execute("SELECT * FROM Grid_Strategy_Param")
        data = c.fetchall()
        
    return data


def get_grid_strategy_param(ID):
    data: any
    with conn:
        c.execute("SELECT * FROM Grid_Strategy_Param where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_all_strategy_param_links():
    data: []
    with conn:
        c.execute("SELECT * FROM Strategy_Param_Link")
        data = c.fetchall()
        
    return data


def get_strategy_param_link(ID):
    data: any
    with conn:
        c.execute("SELECT * FROM Strategy_Param_Link where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_strat_type_id_from_strategy_param_link(ID):
    data: any
    with conn:
        c.execute("SELECT Strategy_Type_ID FROM Strategy_Param_Link where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_param_id_from_strategy_param_link(ID):
    data: any
    with conn:
        c.execute("SELECT Params_ID FROM Strategy_Param_Link where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_all_strategy_settings():
    data: []
    with conn:
        c.execute("SELECT * FROM Strategy_Settings")
        data = c.fetchall()
        
    return data


def get_strategy_setting(ID):
    data: any
    with conn:
        c.execute("SELECT * FROM Strategy_Settings where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_link_id_from_strategy_setting(ID):
    data: any
    with conn:
        c.execute("SELECT Link_ID FROM Strategy_Settings where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_growth_rate_from_strategy_setting(ID):
    data: any
    with conn:
        c.execute("SELECT Growth_Rate FROM Strategy_Settings where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_all_exchange_keys():
    data: []
    with conn:
        c.execute("SELECT * FROM Exchange_Keys")
        data = c.fetchall()
        
    return data


def get_exchange_keys(ID):
    data: any
    with conn:
        c.execute("SELECT * FROM Exchange_Keys where ID=(?)", (ID,))
        data = c.fetchone()
    return data


def get_all_contracts():
    data: []
    with conn:
        c.execute("SELECT * FROM Contract")
        data = c.fetchall()
    return data


def get_contract(ID):
    data: any
    with conn:
        c.execute("SELECT * FROM Contract where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_all_exchanges():
    """
            ID INTEGER PRIMARY KEY,
            Exchange_Type_ID INTEGER,
            Status_ID INTEGER,
            Key_ID INTEGER,
            Name TEXT UNIQUE,
            Investment_Amount TEXT,
            Available_Balance TEXT,
            Forgotten_Profit TEXT,
            Available_Profit TEXT,
            Time_Stamp TEXT,"""
    exchange_list = []
    with conn:
        c.execute("SELECT * FROM Exchange")
        data: [] = c.fetchall()
        for ex_data in data:
            ID = ex_data[0]
            exchange_type = get_exchange_type(ex_data[1])
            status = get_status(ex_data[2])
            exchange_key_id = ex_data[3]
            key_data = get_exchange_keys(ex_data[3])
            public_key: str
            private_key: str
            if key_data:
                public_key = key_data[2]
                private_key = key_data[3]
            name = ex_data[4]
            inv_amount = ex_data[5]
            avail_balance = ex_data[6]
            forgotten_profit = ex_data[7]
            available_profit = ex_data[8]
            timestamp = ex_data[9]
            if exchange_type == "Testing":
                ex = exchange(ID, status, exchange_key_id, name, investment_amount=inv_amount, available_balance=avail_balance, forgotten_profit=forgotten_profit, available_profit=available_profit, timestamp=timestamp)
                exchange_list.append(ex)
            elif exchange_type == "Binance US":
                pass
    return exchange_list


def get_exchange(ID):
    data: any
    with conn:
        c.execute("SELECT * FROM Exchange where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_exchanges_by_exchange_type(exchange_type_id):
    data: []
    with conn:

        c.execute("SELECT * FROM Exchange WHERE Exchange_Type_ID=(?)", (exchange_type_id,))
        data = c.fetchall()
        
    return data


def get_exchanges_by_status(status_id):
    data: []
    with conn:
        c.execute("SELECT * FROM Exchange WHERE Status_ID=(?)", (status_id,))
        data = c.fetchall()
        
    return data


def get_exchange_by_name(name):
    data: []
    with conn:
        c.execute("SELECT * FROM Exchange WHERE Name=(?)", (name,))
        data = c.fetchall()
        
    return data


def get_exchange_id_by_name(name):
    data: []
    with conn:
        c.execute("SELECT ID FROM Exchange WHERE Name=(?)", (name,))
        data = c.fetchone()
        
    return data


def get_all_bots():
    data: []
    with conn:
        c.execute("SELECT * FROM Bot")
        data = c.fetchall()
        
    return data


def get_bot(ID):
    data: any
    with conn:
        c.execute("SELECT * FROM Bot where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_bots_by_strategy_type(strategy_type_id):
    data: []
    with conn:
        c.execute("SELECT * FROM Bot WHERE Strategy_ID=(?)", (strategy_type_id,))
        data = c.fetchall()
        
    return data


def get_bots_by_exchange(exchange_id):
    data: []
    with conn:
        c.execute("SELECT * FROM Bot WHERE Exchange_ID=(?)", (exchange_id,))
        data = c.fetchall()
        
    return data


def get_bots_by_status(status_id):
    data: []
    with conn:
        c.execute("SELECT * FROM Bot WHERE Status_ID=(?)", (status_id,))
        data = c.fetchall()
        
    return data


def get_bot_by_name(name):
    data: []
    with conn:
        c.execute("SELECT * FROM Bot WHERE Name=(?)", (name,))
        data = c.fetchone()
        
    return data


def get_all_trades():
    data: []
    with conn:
        c.execute("SELECT * FROM Trade")
        data = c.fetchall()
        
    return data


def get_trade(ID):
    data: any
    with conn:
        c.execute("SELECT * FROM Trade where ID=(?)", (ID,))
        data = c.fetchone()
        
    return data


def get_associated_trades(ID):
    data: any
    with conn:
        c.execute("SELECT * FROM Trade where Associated_ID=(?)", (ID,))
        data = c.fetchall()
        
    return data


def get_trades_by_exchange(exchange_id):
    data: any
    with conn:
        c.execute("SELECT * FROM Trade where Exchange_ID=(?)", (exchange_id,))
        data = c.fetchall()
        
    return data


def get_trades_by_bot(bot_id):
    data: any
    with conn:
        c.execute("SELECT * FROM Trade where Bot_ID=(?)", (bot_id,))
        data = c.fetchall()
        
    return data


def get_trades_by_status(status_id):
    data: any
    with conn:
        c.execute("SELECT * FROM Trade where Status_ID=(?)", (status_id,))
        data = c.fetchall()
    return data


"""
||||||||||||||||||
|||||  ADD   |||||
||||||||||||||||||
||||||||||||||||||
"""


def __add_time_frame(tf: str):
    with conn:
        c.execute("INSERT INTO Timeframe (Timeframe) VALUES (?)", (tf,))


def __add_status(status: str):
    with conn:
        c.execute("INSERT INTO Status (Status) VALUES (?)", (status,))


def __add_exchange_type(exchange_type: str):
    with conn:
        c.execute("INSERT INTO Exchange_Type (Exchange_Type) VALUES (?)", (exchange_type,))


# def add_exchange_settings():
#     with conn:
#         c.execute("INSERT INTO Exchange_Settings (Exchange_Settings)")


def __add_strategy_type(strategy_type: str) -> int:
    param_id: int
    with conn:
        c.execute("INSERT INTO Strategy_Type (Strategy_Type) VALUES (?)", (strategy_type,))
        param_id = c.lastrowid
    return param_id

# Stop_Loss
# TEXT,
# Take_Profit
# TEXT,
# Upper
# TEXT,
# Lower
# TEXT,
# Number_of_Intervals
# INTEGER,
# Trade_Size
# TEXT
def add_grid_strategy_param(params) -> int:
    """
            ID INTEGER PRIMARY KEY,
            Stop_Loss TEXT,
            Take_Profit TEXT,
            Upper TEXT,
            Lower TEXT,
            Number_of_Intervals INTEGER,
            Trade_Size TEXT
    :param params:
    :return:
    """
    param_id: int
    param_dict = {
        'Stop_loss': str(params['Stop_Loss']),  # TEXT
        'Take_Profit': str(params['Take_Profit']),  # TEXT
        'Upper': str(params['Upper']),  # TEXT
        'Lower': str(params['Lower']),  # TEXT
        'Number_of_Intervals': int(params['Number_of_Intervals']),  # INTEGER
        'Trade_Size': str(params['Trade_Size'])  # TEXT
    }
    with conn:
        c.execute("""
        INSERT INTO Grid_Strategy_Param (Stop_Loss, Take_Profit, Upper, Lower, Number_of_Intervals, Trade_Size) 
        VALUES (:Stop_Loss, :Take_Profit, :Upper, :Lower, :Number_of_Intervals, :Trade_Size)
        """, param_dict)
        param_id = c.lastrowid
    return param_id


def add_strategy_parameter_link(strategy_type_id: int, param_id: int) -> int:
    """
            ID INTEGER PRIMARY KEY,
            Strategy_Type_ID INTEGER,
            Params_ID INTEGER,
    :param strategy_type_id:
    :param param_id:
    :return:
    """
    link_id: int
    with conn:
        c.execute("""
        INSERT INTO Strategy_Param_Link (Strategy_Type_ID, Params_ID) 
        VALUES (?, ?)
        """, (strategy_type_id, param_id))
        link_id = c.lastrowid
    return link_id


def add_strategy_settings(link_id, growth_rate) -> int:
    """
            ID INTEGER PRIMARY KEY,
            Link_ID INTEGER,
            Growth_Rate TEXT,
    :param link_id:
    :param growth_rate:
    :return:
    """
    settings_id: int
    with conn:
        c.execute("""
            INSERT INTO Strategy_Settings (Link_ID, Growth_Rate) 
            VALUES (?, ?)
            """, (link_id, growth_rate))
        settings_id = c.lastrowid
    return settings_id


def add_exchange_keys(exchange_type_id: int, encrypted_public_key: str, encrypted_private_key: str) -> int:
    """
            ID INTEGER PRIMARY KEY,
            Exchange_Type_ID INTEGER,
            Public_Key TEXT,
            Private_Key TEXT,
    :param exchange_type_id:
    :param encrypted_public_key:
    :param encrypted_private_key:
    :return:
    """
    key_id: int
    with conn:
        c.execute("""
        INSERT INTO Strategy_Settings (Exchange_Type_ID, Public_Key, Private_Key) 
        VALUES (?, ?, ?)
        """, (exchange_type_id, encrypted_public_key, encrypted_private_key))
        key_id = c.lastrowid
    return key_id


def add_contract(contract) -> int:
    contract_id: int
    contract_dict = {
        'Exchange_Type_ID': get_exchange_type_id(contract.exchange.exchange_type),
        'Symbol': contract.symbol,
        'Base_Asset': contract.base_asset,
        'Quote_Asset': contract.quote_asset,
        'Price_Decimals': contract.price_decimals,
        'Quantity_Decimals': contract.quantity_decimals,
        'Tick_Size': contract.tick_size,
        'Lot_Size': contract.lot_size,
        'Quanto': contract.quanto,
        'Inverse': contract.inverse,
        'Multiplier': contract.multiplier
    }
    with conn:
        c.execute("INSERT INTO Contract (Contract) VALUES (:Exchange_Type_ID, :Symbol, :Base_Asset, :Quote_Asset, :Price_Decimals, :Quantity_Decimals, :Tick_Size, :Lot_Size, :Quanto, :Inverse, :Multiplier)", contract_dict)
        contract_id = c.lastrowid
    return contract_id


def add_exchange(exchange) -> int:
    """

            CREATE TABLE IF NOT EXISTS Exchange (
            ID INTEGER PRIMARY KEY,
            Exchange_Type_ID INTEGER,
            Status_ID INTEGER,
            Key_ID INTEGER,
            Settings_ID INTEGER,
            Name TEXT UNIQUE,
            Investment_Amount TEXT,
            Available_Balance TEXT,
            Forgotten_Profit TEXT,
            Available_Profit TEXT,
            Time_Stamp TEXT,
            FOREIGN KEY (Exchange_Type_ID) REFERENCES Exchange_Type(ID),
            FOREIGN KEY (Status_ID) REFERENCES Status(ID),
            FOREIGN KEY (Key_ID) REFERENCES Exchange_Keys(ID)
            FOREIGN KEY (Settings_ID) REFERENCES Exchange_Setting(ID)
            )
    :param exchange:
    :return:
    """
    exchange_id: int
    ex_dict = {
        'Exchange_Type_ID': get_exchange_type_id(exchange.exchange_type),
        'Status_ID': get_status_id(exchange.get_status()),
        'Key_ID': exchange.get_key_id(),
        'Name': exchange.get_name(),
        'Investment_Amount': str(exchange.get_investment_amount()),
        'Available_Balance': str(exchange.get_available_balance()),
        'Forgotten_Profit': str(exchange.get_forgotten_profit()),
        'Available_Profit': str(exchange.get_available_profit()),
        'Time_Stamp': str(exchange.get_timestamp())
    }
    with conn:
        c.execute("""
            INSERT INTO Exchange (
                Exchange_Type_ID, Status_ID, Key_ID, Name, 
                Investment_Amount, Available_Balance, 
                Forgotten_Profit, Available_Profit, Time_Stamp
            ) VALUES (
                :Exchange_Type_ID, :Status_ID, :Key_ID, :Name, 
                :Investment_Amount, :Available_Balance, 
                :Forgotten_Profit, :Available_Profit, :Time_Stamp
            )""", ex_dict)
        exchange_id = c.lastrowid
    return exchange_id


def add_bot(bot) -> int:
    bot_id: int
    bot_dict = {
        'Exchange_ID': get_exchange_id_by_name(bot.client.get_name()),
        'Status_ID': get_status_id(bot.get_status()),
        'Contract_ID': bot.contract_id,
        'Strategy_ID': get_strategy_type_id(bot.strategy_type),
        'Settings_ID': bot.settings_id,
        'Name': bot.get_name(),
        'Investment_Amount': str(bot.get_investment_amount()),
        'Total_Balance': str(bot.get_total_balance()),
        'Available_Balance': str(bot.get_available_balance()),
        'Total_Crypto': str(bot.get_total_crypto()),
        'Forgotten_Profit': str(bot.get_forgotten_profit()),
        'Available_Profit': str(bot.get_available_profit()),
        'Time_Stamp': str(bot.get_timestamp())
    }
    with conn:
        c.execute("""
            INSERT INTO Bot (
                Exchange_ID, Status_ID, Contract_ID, Strategy_ID, Settings_ID, 
                Name, Investment_Amount, Total_Balance, Available_Balance, 
                Total_Crypto, Forgotten_Profit, Available_Profit, Time_Stamp
            ) VALUES (
                :Exchange_ID, :Status_ID, :Contract_ID, :Strategy_ID, :Settings_ID, 
                :Name, :Investment_Amount, :Total_Balance, :Available_Balance, 
                :Total_Crypto, :Forgotten_Profit, :Available_Profit, :Time_Stamp
            )""", bot_dict)
        bot_id = c.lastrowid
    return bot_id


def add_trade(trade) -> int:
    """
            Associated_ID INTEGER, -- Nullable column
            Exchange_ID INTEGER,
            Contract_ID INTEGER,
            Status_ID INTEGER,
            Bot_ID INTEGER,
            Side TEXT CHECK(Side IN ('Buy', 'Sell')),
            Position_Side TEXT CHECK(Position_Side IN ('long', 'short')),
            USDT TEXT,
            Crypto TEXT,
            Time_Stamp TEXT,
    :param exchange:
    :return:
    """
    trade_id: int
    trade_dict = {
        'Associated_ID': trade.associated_id,
        'Exchange_ID': trade.exchange_id,
        'Contract_ID': trade.contract_id,
        'Status_ID': get_status_id(trade.status),
        'Bot_ID': trade.bot_id,
        'Side': trade.side,
        'Position_Side': trade.positionSide,
        'USDT': trade.price,
        'Crypto': trade.get_crypto_amount(),
        'Time_Stamp': trade.time
    }
    with conn:
        c.execute("""
            INSERT INTO Trade (
                Associated_ID, Exchange_ID, Contract_ID, Status_ID, Bot_ID, 
                Side, Position_Side, USDT, Crypto, Time_Stamp
            ) VALUES (
                :Associated_ID, :Exchange_ID, :Contract_ID, :Status_ID, :Bot_ID, 
                :Side, :Position_Side, :USDT, :Crypto, :Time_Stamp
            )""", trade_dict)
        trade_id = c.lastrowid
    return trade_id


"""
||||||||||||||||||
|||  UPDATE   ||||
||||||||||||||||||
||||||||||||||||||
"""


# def update_grid_strategy_param(ID, params):
#     pass


def update_strategy_settings(ID, growth_rate):
    with conn:
        settings_dict = {
            'ID': ID,
            'Growth_Rate': growth_rate
        }
        c.execute(
            """
            UPDATE Strategy_Settings 
            SET Growth_Rate = :Growth_Rate 
            WHERE ID = :ID
            """, settings_dict)


def update_exchange(ex: exchange):
    """
           ID INTEGER PRIMARY KEY,
            Exchange_Type_ID INTEGER,
            Status_ID INTEGER,
            Key_ID INTEGER,
            Settings_ID INTEGER,
            Name TEXT UNIQUE,
            Investment_Amount TEXT,
            Total_Balance TEXT,
            Available_Balance TEXT,
            Forgotten_Profit TEXT,
            Available_Profit TEXT,
            Time_Stamp TEXT,
    :param ex:
    :return:
    """
    ex_dict = {
        'ID': ex.get_id(),
        'Status_ID': get_status_id(ex.get_status()),
        'Investment_Amount': str(ex.get_investment_amount()),
        'Available_Balance': str(ex.get_available_balance()),
        'Forgotten_Profit': str(ex.get_forgotten_profit()),
        'Available_Profit': str(ex.get_available_profit())
    }
    
    c.execute(
        """
        UPDATE Exchange 
        SET Status_ID = :Status_ID, 
            Investment_Amount = :Investment_Amount, 
            Available_Balance = :Available_Balance, 
            Forgotten_Profit = :Forgotten_Profit, 
            Available_Profit = :Available_Profit
        WHERE ID = :ID
        """, ex_dict)


def update_bot(bot):
    """
            Exchange_ID INTEGER,
            Status_ID INTEGER,
            Contract_ID INTEGER,
            Strategy_ID INTEGER,
            Settings_ID INTEGER,
            Name TEXT UNIQUE,
            Investment_Amount TEXT,
            Total_Balance TEXT,
            Available_Balance TEXT,
            Total_Crypto TEXT,
            Forgotten_Profit TEXT,
            Available_Profit TEXT,
            TimeStamp TEXT,
    :param bot:
    :return:
    """
    bot_dict = {
        'ID': bot.get_id(),
        'Status_ID': get_status_id(bot.get_status()),
        'Investment_Amount': bot.get_investment_amount(),
        'Total_Balance': bot.get_total_balance(),
        'Available_Balance': bot.get_available_balance(),
        'Total_Crypto': bot.get_total_crypto(),
        'Forgotten_Profit': bot.get_forgotten_profit(),
        'Available_Profit': bot.get_available_profit()
    }
    c.execute(
        """
        UPDATE Bot 
        SET Status_ID = :Status_ID,
            Investment_Amount = :Investment_Amount,
            Total_Balance = :Total_Balance,
            Available_Balance = :Available_Balance,
            Total_Crypto = :Total_Crypto,
            Forgotten_Profit = :Forgotten_Profit,
            Available_Profit = :Available_Profit
        WHERE ID = :ID
        """, bot_dict)


def update_trade(trade):
    """CREATE TABLE IF NOT EXISTS Trade (
    ID INTEGER PRIMARY KEY,
    Associated_ID INTEGER, -- Nullable column
    Exchange_ID INTEGER,
    Contract_ID INTEGER,
    Status_ID INTEGER,
    Bot_ID INTEGER,
    Side TEXT CHECK(Side IN ('Buy', 'Sell')),
    Position_Side TEXT CHECK(Position_Side IN ('long', 'short')),
    USDT TEXT,
    Crypto TEXT,
    Time_Stamp TEXT,
    """
    trade_dict = {
        'ID': trade.entry_id,
        'Status_ID': get_status_id(trade.get_status()),
        'USDT': trade.get_entry_price(),
        'Crypto': trade.get_crypto_amount(),

    }
    c.execute(
        """
        UPDATE Trade 
        SET Status_ID = :Status_ID,
            USDT = :USDT,
            Crypto = :Crypto
        WHERE ID = :ID
        """, trade_dict)


def close():
    conn.close()
