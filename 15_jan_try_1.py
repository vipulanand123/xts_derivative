import logging
import os
import sys
import json
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from concurrent.futures import ProcessPoolExecutor
from functools import partial
from multiprocessing import Manager, get_context, Queue
import socketio
import requests

import pandas as pd

def define_logger():
    # Logging Definitions
    log_lvl = logging.DEBUG
    console_log_lvl = logging.INFO
    _logger = logging.getLogger('arathi')
    # logger.setLevel(log_lvl)
    _logger.setLevel(console_log_lvl)
    console = logging.StreamHandler(stream=sys.stdout)
    console.setLevel(console_log_lvl)
    formatter = logging.Formatter('%(asctime)s %(levelname)s <%(funcName)s> %(message)s')
    console.setFormatter(formatter)
    _logger.addHandler(console)
    # logger.propagate = False  # Removes AWS Level Logging as it tracks root propagation as well
    return _logger
logger = define_logger()

user_id = 'BR052'
host = "https://algozy.rathi.com:3000"
# socket_url = f"wss://algozy.rathi.com:3000/marketdata/socket.io/"
socket_url = f"wss://algozy.rathi.com:3000"
access_token = ''
data_api_key = '9af31b94f3999bd12c6e89'
data_api_secret = 'Evas244$3H'
interactive_api_key = 'dabfe67ee2286b19a7b664'
interactive_api_secret = 'Mbqk087#Y1'

#login
def login():
    url = f"{host}/apimarketdata/auth/login"
    payload = {"appKey": data_api_key, "secretKey": data_api_secret, "source": "WebAPI"}
    response = requests.post(url=url, json=payload)
    # logger.info(response.content)
    data = response.json()
    return data

info = login()
access_token = info['result']['token']
print('\naccess token is ', access_token)

class MdSocketIO(socketio.Client):
    def __init__(self, url, token, userID, reconnection=True, reconnection_attempts=0, reconnection_delay=1,
                 reconnection_delay_max=50000, randomization_factor=0.5, logger=False, binary=False, json=None,
                 **kwargs):
        super().__init__(reconnection, reconnection_attempts, reconnection_delay, reconnection_delay_max,
                         randomization_factor)
        self.sid = socketio.Client(logger=True, engineio_logger=False)
        self.eventlistener = self.sid

        self.sid.on('connect', self.on_connect)
        self.sid.on('message', self.on_message)

        """Similarly implement partial json full and binary json full."""

        self.sid.on('1501-json-full', self.on_message1501_json_full)
        self.sid.on('1501-json-partial', self.on_message1501_json_partial)

        self.sid.on('1502-json-full', self.on_message1502_json_full)
        self.sid.on('1502-json-partial', self.on_message1502_json_partial)

        # self.sid.on('1505-json-full', self.on_message1505_json_full)
        # self.sid.on('1505-json-partial', self.on_message1505_json_partial)
        #
        # self.sid.on('1507-json-full', self.on_message1507_json_full)
        #
        # self.sid.on('1510-json-full', self.on_message1510_json_full)
        # self.sid.on('1510-json-partial', self.on_message1510_json_partial)
        #
        # self.sid.on('1512-json-full', self.on_message1512_json_full)
        # self.sid.on('1512-json-partial', self.on_message1512_json_partial)
        #
        # self.sid.on('1105-json-full', self.on_message1105_json_full)
        # self.sid.on('1105-json-partial', self.on_message1105_json_partial)

        # self.sid.on('disconnect', self.on_disconnect)

        # """Get the root url from config file"""
        # currDirMain = os.getcwd()
        # configParser = configparser.ConfigParser()
        # configFilePath = os.path.join(currDirMain, 'config.ini')
        # configParser.read(configFilePath)

        # self.port = configParser.get('root_url', 'root')
        # self.broadcastMode = configParser.get('root_url', 'broadcastMode')
        self.port = url
        self.broadcastMode = kwargs.get('broadcast_mode', 'Full')
        self.userID = userID
        publish_format = 'JSON'
        self.token = token

        port = f'{self.port}/?token='

        self.connection_url = port + token + '&userID=' + self.userID + '&publishFormat=' + publish_format + '&broadcastMode=' + self.broadcastMode
        print(self.connection_url)

    def connect(self, headers={}, transports='websocket', namespaces=None, socketio_path='/apimarketdata/socket.io',
                verify=False):
        url = self.connection_url
        """Connected to the socket."""
        self.sid.connect(url, headers, transports=transports, namespaces=namespaces, socketio_path=socketio_path)
        self.sid.wait()
        """Disconnected from the socket."""
        # self.sid.disconnect()

    @staticmethod
    def on_connect():
        """Connect from the socket."""
        print('Market Data Socket connected successfully!')

    @staticmethod
    def on_message(data):
        """On receiving message"""
        print('I received a message!' + data)

    @staticmethod
    def on_message1502_json_full(data):
        """On receiving message code 1502 full"""
        print('I received a 1502 Market depth message!' + data)

    @staticmethod
    def on_message1507_json_full(data):
        """On receiving message code 1507 full"""
        print('I received a 1507 MarketStatus message!' + data)

    @staticmethod
    def on_message1512_json_full(data):
        """On receiving message code 1512 full"""
        print('I received a 1512 LTP message!' + data)

    @staticmethod
    def on_message1505_json_full(data):
        """On receiving message code 1505 full"""
        print('I received a 1505 Candle data message!' + data)

    @staticmethod
    def on_message1510_json_full(data):
        """On receiving message code 1510 full"""
        print('I received a 1510 Open interest message!' + data)

    @staticmethod
    def on_message1501_json_full(data):
        """On receiving message code 1501 full"""
        print('I received a 1501 Level1,Touchline message!' + data)

    @staticmethod
    def on_message1502_json_partial(data):
        """On receiving message code 1502 partial"""
        print('I received a 1502 partial message!' + data)

    @staticmethod
    def on_message1512_json_partial(data):
        """On receiving message code 1512 partial"""
        print('I received a 1512 LTP message!' + data)

    @staticmethod
    def on_message1505_json_partial(data):
        """On receiving message code 1505 partial"""
        print('I received a 1505 Candle data message!' + data)

    @staticmethod
    def on_message1510_json_partial(data):
        """On receiving message code 1510 partial"""
        print('I received a 1510 Open interest message!' + data)

    @staticmethod
    def on_message1501_json_partial(data):
        """On receiving message code 1501 partial"""
        now = datetime.now()
        today = now.strftime("%H:%M:%S")
        print(today, 'in main 1501 partial Level1,Touchline message!' + data + ' \n')

    @staticmethod
    def on_message1105_json_partial(data):
        """On receiving message code 1105 partial"""
        now = datetime.now()
        today = now.strftime("%H:%M:%S")
        print(today, 'in main 1105 partial, Instrument Property Change Event!' + data + ' \n')

        print('I received a 1105 Instrument Property Change Event!' + data)

    @staticmethod
    def on_message1105_json_full(data):
        """On receiving message code 1105 full"""
        now = datetime.now()
        today = now.strftime("%H:%M:%S")
        print(today, 'in main 1105 full, Instrument Property Change Event!' + data + ' \n')

        print('I received a 1105 Instrument Property Change Event!' + data)

    @staticmethod
    def on_disconnect():
        """Disconnected from the socket"""
        print('Market Data Socket disconnected!')

    @staticmethod
    def on_error(data):
        """Error from the socket"""
        print('Market Data Error', data)

    def get_emitter(self):
        """For getting the event listener"""
        return self.eventlistener

def subscribe_index():
    url = f"{host}/apimarketdata/instruments/subscription"
    payload = {"instruments": [{"exchangeSegment": 1, "exchangeInstrumentID": "26000"},
                               {"exchangeSegment": 2, "exchangeInstrumentID": "43202"},
                               {"exchangeSegment": 2, "exchangeInstrumentID": "43203"},
                               {"exchangeSegment": 2, "exchangeInstrumentID": "43224"},
                               {"exchangeSegment": 2, "exchangeInstrumentID": "43227"},
                               ],
               "xtsMessageCode": 1502}
    response = requests.post(url=url, headers={'authorization': access_token}, json=payload)
def on_connect():
    print('\nOption Strike price, ideally user choice but here it is 21850(nifty) and 47800(banknifty)\n')
    strike_nifty, strike_banknifty = 21850, 47800
    print('\nExpiry data is hardcoded nifty(18Jan2024) and banknifty(17Jan2024)')
    expiry_nifty, expiry_banknifty = '18Jan2024', '17Jan2024'
    print('\nOption type is hardcoded call and put')
    call_option, put_option = 'CE', 'PE'
    s = expiry_nifty.upper()
    sb = expiry_banknifty.upper()
    disp_nifty_c = 'NIFTY ' + s+ ' ' + call_option + ' ' + str(strike_nifty)
    disp_nifty_p = 'NIFTY ' + s+ ' ' + put_option + ' ' + str(strike_nifty)
    print('\ndescription of nifty call: ' + disp_nifty_c.upper())
    print('\ndescription of nifty put: ' + disp_nifty_p.upper())
    disp_banknifty_c = 'BANKNIFTY ' + sb+ ' ' +call_option + ' ' + str(strike_banknifty)
    disp_banknifty_p = 'BANKNIFTY ' + sb+ ' ' +put_option + ' ' + str(strike_banknifty)
    print('\ndescription of banknifty call: ' + disp_banknifty_c.upper())
    print('\ndescription of banknifty put: ' + disp_banknifty_p.upper())

    df = pd.DataFrame(columns=['desc_nifty_c', 'desc_banknifty_c', 'desc_nifty_p', 'desc_banknifty_p'])
    df.loc[0] = [disp_nifty_c, disp_banknifty_c, disp_nifty_p, disp_banknifty_p]
#     get_inst_str(disp_nifty_c)
    # for i in df.loc[0]:
    #     print('\n sent ARE \n',i)
    df.loc[1] = [get_inst_str(i) for i in df.loc[0]]
    print('\ndf is \n', df)
    # subscribe_index()


def get_inst_str(desc):
    gis_url = f'{host}/apimarketdata/search/instruments'
    if desc.startswith('NIFTY'):
        searchString = 'nifty'
    elif desc.startswith('BANK'):
        searchString = 'banknifty'
    gis_payload = {'searchString': searchString, 'source': 'WEB'}
    gis_header = {'authorization': access_token}
    gis_response = requests.get(url=gis_url, headers=gis_header, params=gis_payload)

    if gis_response.status_code == 200:
        gis_data = gis_response.json()
        ins_list = gis_data.get('result', [])
        for instrument in ins_list:
            # print('\n in 1st for loop')
            de = instrument.get('DisplayName')
            # print(f'\ndisp name = {de} while sent is {desc}')
            if instrument.get('DisplayName') == desc:
                # print('\n inside if statement')
                instrument_id = instrument.get('ExchangeInstrumentID')
                print(f'The instrument ID for {desc} is: {instrument_id}')
                return instrument_id
        # return gis_data

    else:
        # logger.error(f'Error in finding the instrument id. Status code: {gis_response.status_code}')
        return None

def on_message(data, code=None):
    """On receiving message code 1502 full"""
    # logger.info(f'{code} message: {data}')
    if code == 1502:
        msg = json.loads(data)
        ins_id = msg.get('ExchangeInstrumentID')
        ltp = msg.get('Touchline', {}).get('LastTradedPrice')
        #logger.info(f"instrument: {ins_id}, ltp: {ltp}")
def queue_processor(q: Queue):
    while True:
        try:
            msg = q.get()
            logger.info(msg)
        except Exception as q_exc:
            logger.error(f'Error in queue msg: {q_exc}')

on_message1501_json_full = partial(on_message, code=1501)
on_message1502_json_full = partial(on_message, code=1502)
on_message1507_json_full = partial(on_message, code=1507)
on_message1512_json_full = partial(on_message, code=1512)
def main():
    with ProcessPoolExecutor(max_workers=2, mp_context=get_context('spawn')) as executor:
        mp = Manager()
        queue = mp.Queue()
        client = MdSocketIO(url=host, token=access_token, userID=user_id)
        el = client.get_emitter()
        el.on('connect', on_connect)
        el.on('message', on_message)
        el.on('1501-json-full', on_message1501_json_full)
        # el.on('1502-json-full', queue.put)
        el.on('1502-json-full', on_message1502_json_full)
        # el.on('1507-json-full', on_message1507_json_full)
        # el.on('1512-json-full', on_message1512_json_full)
        # el.on('1105-json-full', on_message1105_json_full)

        executor.submit(queue_processor, queue)

        try:
            client.connect()
        except Exception as exc:
            logger.error(f"Error in connection: {exc}")

if __name__ == "__main__":
    main()