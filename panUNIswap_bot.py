#!python
# cython: language_level=3

import datetime
from itertools import permutations
import time
import uni3
from swap import Uniswap
from web3 import Web3, middleware, _utils
from web3.gas_strategies.time_based import fast_gas_price_strategy, glacial_gas_price_strategy
from pycoingecko import CoinGeckoAPI
import pyetherbalance
import requests
import math
import subprocess
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget, QGraphicsObject
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtTest
import fileinput
import re
import importlib
import os
from time import localtime, strftime
from web3 import types
import traceback

sys.path.insert(0, './')
import configfile
import json
import requests

sys.setrecursionlimit(1500)

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons


def __ne__(self, other):
    return not self.__eq__(other)

 
cg = CoinGeckoAPI()


class Port(object):
    def __init__(self, view):
        self.view = view

    def flush(self):
        pass

    def write(self, text):
        cursor = self.view.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.view.setTextCursor(cursor)
        self.view.ensureCursorVisible()


@pyqtSlot(str)
def trap_exc_during_debug(*args):
    if configfile.debugmode == '1':
        exception_type, exception_object, exception_traceback = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


sys.excepthook = trap_exc_during_debug


@pyqtSlot()
class Worker(QObject):
    sig_step = pyqtSignal(int, str)  # worker id, step description: emitted every step through work() loop
    sig_done = pyqtSignal(int)  # worker id: emitted at end of work()
    sig_msg = pyqtSignal(str)  # message to be shown to user

    def __init__(self, id: int):
        super().__init__()
        self.__id = id
        self.__abort = False

    def work(self):
        while self.__abort != True:
            thread_name = QThread.currentThread().objectName()
            thread_id = int(QThread.currentThreadId())  # cast to int() is necessary
            self.sig_msg.emit('Running worker #{} from thread "{}" (#{})'.format(self.__id, thread_name, thread_id))

            if 'step' not in locals():
                step = 1
            else:
                step = 1
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()
            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))

            importlib.reload(configfile)
            w33 = Web3()
            cg = CoinGeckoAPI()
            maxgwei = int(configfile.maxgwei)
            if configfile.maxgweinumber == '':
                maxgweinumber = 0
            else:
                maxgweinumber = int(configfile.maxgweinumber)
            diffdeposit = float(configfile.diffdeposit)
            diffdepositaddress = str(configfile.diffdepositaddress)
            speed = str(configfile.speed)
            max_slippage = float(configfile.max_slippage)
            incaseofbuyinghowmuch = int(configfile.incaseofbuyinghowmuch)
            ethtokeep = int(configfile.ethtokeep)
            timesleepaftertrade = int(configfile.secondscheckingprice_2)
            timesleep = int(configfile.secondscheckingprice)
            infura_url = str(configfile.infuraurl)
            infuraurl = infura_url
            tokentokennumerator = float(configfile.tokentokennumerator)
            mcotoseeassell = float(configfile.mcotoseeassell)
            debugmode = int(configfile.debugmode)

            ##for token_number,eth_address,high,low,activate,stoploss_value,stoploss_activate,trade_with_ERC,trade_with_ETH,fast_token in all_token_information:
            all_token_information = [
                (1, str(configfile.token1ethaddress), float(configfile.token1high), float(configfile.token1low),
                 float(configfile.activatetoken1), float(configfile.token1stoploss), float(configfile.stoplosstoken1)
                 , float(configfile.tradewithERCtoken1), float(configfile.tradewithETHtoken1), '0',
                 str(configfile.token1name), int(configfile.token1decimals)),
                (2, str(configfile.token2ethaddress), float(configfile.token2high), float(configfile.token2low),
                 float(configfile.activatetoken2), float(configfile.token2stoploss), float(configfile.stoplosstoken2)
                 , float(configfile.tradewithERCtoken2), float(configfile.tradewithETHtoken2), '0',
                 str(configfile.token2name), int(configfile.token2decimals)),
                (3, str(configfile.token3ethaddress), float(configfile.token3high), float(configfile.token3low),
                 float(configfile.activatetoken3), float(configfile.token3stoploss), float(configfile.stoplosstoken3)
                 , float(configfile.tradewithERCtoken3), float(configfile.tradewithETHtoken3), '0',
                 str(configfile.token3name), int(configfile.token3decimals)),
                (4, str(configfile.token4ethaddress), float(configfile.token4high), float(configfile.token4low),
                 float(configfile.activatetoken4), float(configfile.token4stoploss), float(configfile.stoplosstoken4)
                 , float(configfile.tradewithERCtoken4), float(configfile.tradewithETHtoken4), '0',
                 str(configfile.token4name), int(configfile.token4decimals)),
                (5, str(configfile.token5ethaddress), float(configfile.token5high), float(configfile.token5low),
                 float(configfile.activatetoken5), float(configfile.token5stoploss), float(configfile.stoplosstoken5)
                 , float(configfile.tradewithERCtoken5), float(configfile.tradewithETHtoken5), '0',
                 str(configfile.token5name), int(configfile.token5decimals)),
                (6, str(configfile.token6ethaddress), float(configfile.token6high), float(configfile.token6low),
                 float(configfile.activatetoken6), float(configfile.token6stoploss), float(configfile.stoplosstoken6)
                 , float(configfile.tradewithERCtoken6), float(configfile.tradewithETHtoken6), '0',
                 str(configfile.token6name), int(configfile.token6decimals)),
                (7, str(configfile.token7ethaddress), float(configfile.token7high), float(configfile.token7low),
                 float(configfile.activatetoken7), float(configfile.token7stoploss), float(configfile.stoplosstoken7)
                 , float(configfile.tradewithERCtoken7), float(configfile.tradewithETHtoken7), '0',
                 str(configfile.token7name), int(configfile.token7decimals)),
                (8, str(configfile.token8ethaddress), float(configfile.token8high), float(configfile.token8low),
                 float(configfile.activatetoken8), float(configfile.token8stoploss), float(configfile.stoplosstoken8)
                 , float(configfile.tradewithERCtoken8), float(configfile.tradewithETHtoken8), '0',
                 str(configfile.token8name), int(configfile.token8decimals)),
                (9, str(configfile.token9ethaddress), float(configfile.token9high), float(configfile.token9low),
                 float(configfile.activatetoken9), float(configfile.token9stoploss), float(configfile.stoplosstoken9)
                 , float(configfile.tradewithERCtoken9), float(configfile.tradewithETHtoken9), '0',
                 str(configfile.token9name), int(configfile.token9decimals)),
                (10, str(configfile.token10ethaddress), float(configfile.token10high), float(configfile.token10low),
                 float(configfile.activatetoken10), float(configfile.token10stoploss), float(configfile.stoplosstoken10)
                 , float(configfile.tradewithERCtoken10), float(configfile.tradewithETHtoken10), '0',
                 str(configfile.token10name), int(configfile.token10decimals))]

            # its now: for token_number,eth_address,high,low,activate,stoploss_value,stoploss_activate,trade_with_ERC,trade_with_ETH,fast_token,small_case_name,decimals in all_token_information:

            for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals in all_token_information:
                if (high < low):
                    print(
                        'Stop the script, a tokenlow is higher than its tokenhigh')
                    count = 0
                    QCoreApplication.processEvents()
                    while self.__abort != True:
                        QCoreApplication.processEvents()
                        pass
                if (stoploss_value > high):
                    print(
                        'Stop the script, a stoploss is higher than the tokenhigh')
                    count = 0
                    QCoreApplication.processEvents()
                    while self.__abort != True:
                        QCoreApplication.processEvents()
                        pass
                if (ethtokeep > mcotoseeassell):
                    print(
                        'The buy/sell boundary is lower than the $ to keep in BNB after trade')
                    count = 0

            my_address = str(configfile.my_address)
            private_key = str(configfile.private_key)

            pk = private_key
            if configfile.maincoinoption == 'BNB':
                ethaddress = "0x0000000000000000000000000000000000000000"
                maindecimals = 18
            if configfile.maincoinoption == 'DAI':
                ethaddress = "0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3"
                maindecimals = 18
            if configfile.maincoinoption == 'BUSD':
                ethaddress = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
                maindecimals = 18
            if configfile.maincoinoption == 'USDC':
                ethaddress = "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d"
                maindecimals = 18
            if configfile.maincoinoption == 'wBTC':
                ethaddress = "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c"
                maindecimals = 18
            if configfile.maincoinoption == 'ETH':
                ethaddress = "0x2170ed0880ac9a755fd29b2688956bd959f933f8"
                maindecimals = 18
            maincoinname = configfile.maincoinoption
            maincoinoption = ethaddress
            append = QtCore.pyqtSignal(str)

            if 'step' not in locals():
                step = 1
            else:
                step = 1
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()
            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
            totaldollars = 1

            def gettotaltokenbalance(all_token_information, infura_url, ethaddress, maindecimals, my_address,
                                     ethtokeep):
                print('(re)Preparing bot...')
                QCoreApplication.processEvents()
                if 'step' not in locals():
                    step = 1
                else:
                    step = 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                priceeth = int(
                    float((requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())['price']))
                threeeth = 1
                ethereum_address = my_address
                try:  # balances
                    if ethaddress == "0x0000000000000000000000000000000000000000":
                        balance_eth = ethbalance.get_eth_balance(my_address)['balance']
                        dollarbalancemaintoken = priceeth * balance_eth
                    else:
                        details = {'symbol': 'potter', 'address': ethaddress, 'decimals': maindecimals,
                                   'name': 'potter'}
                        erc20tokens = ethbalance.add_token('potter', details)
                        balance_eth = ethbalance.get_token_balance('potter', ethereum_address)['balance']
                        maintokeneth = uniswap_wrapper.get_eth_token_input_price(w33.toChecksumAddress(ethaddress),
                                                                                 100)

                        if maindecimals != 18:
                            mainusd = (priceeth / (maintokeneth)) * 100
                        else:
                            mainusd = (priceeth / (maintokeneth)) * 100
                        dollarbalancemaintoken = mainusd * balance_eth

                    if len(all_token_information[0]) > 15:
                        all_token_information[0] = all_token_information[0][:15]
                        all_token_information[1] = all_token_information[1][:15]
                        all_token_information[2] = all_token_information[2][:15]
                        all_token_information[3] = all_token_information[3][:15]
                        all_token_information[4] = all_token_information[4][:15]
                        all_token_information[5] = all_token_information[5][:15]
                        all_token_information[6] = all_token_information[6][:15]
                        all_token_information[7] = all_token_information[7][:15]
                        all_token_information[8] = all_token_information[8][:15]
                        all_token_information[9] = all_token_information[9][:15]
                    if len(all_token_information[0]) > 14:
                        for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                            if eth_address != '0' or '':
                                erc20tokens = ethbalance.add_token(small_case_name,
                                                                   {'symbol': small_case_name, 'address': eth_address,
                                                                    'decimals': decimals,
                                                                    'name': small_case_name})
                                a = ethbalance.get_token_balance(small_case_name, ethereum_address)['balance']
                                all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                          :12] + (a, all_token_information[
                                    token_number - 1][13], all_token_information[token_number - 1][14])
                            else:
                                a = 0
                                all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                          :12] + (a, all_token_information[
                                    token_number - 1][13], all_token_information[token_number - 1][14])
                    else:
                        for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals in all_token_information:
                            if eth_address != '0' or '':
                                details = {'symbol': small_case_name, 'address': eth_address, 'decimals': decimals,
                                           'name': small_case_name.upper}
                                erc20tokens = ethbalance.add_token(small_case_name.upper, details)
                                a = ethbalance.get_token_balance(small_case_name.upper, ethereum_address)['balance']
                                all_token_information[token_number - 1] = all_token_information[token_number - 1] + (a,)
                            else:
                                a = 0
                                all_token_information[token_number - 1] = all_token_information[token_number - 1] + (a,)
                    # its now: for token_number,eth_address,high,low,activate,stoploss_value,stoploss_activate,trade_with_ERC,trade_with_ETH,fast_token,small_case_name,decimals,balance in all_token_information:
                
                except Exception as e:
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                QCoreApplication.processEvents()
                if 'step' not in locals():
                    step = 1
                else:
                    step = 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                try:  # prices
                    if len(all_token_information[0]) > 15:
                        all_token_information[0] = all_token_information[0][:15]
                        all_token_information[1] = all_token_information[1][:15]
                        all_token_information[2] = all_token_information[2][:15]
                        all_token_information[3] = all_token_information[3][:15]
                        all_token_information[4] = all_token_information[4][:15]
                        all_token_information[5] = all_token_information[5][:15]
                        all_token_information[6] = all_token_information[6][:15]
                        all_token_information[7] = all_token_information[7][:15]
                        all_token_information[8] = all_token_information[8][:15]
                        all_token_information[9] = all_token_information[9][:15]
                    priceeth = int(
                        float((requests.get(
                            'https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                  'price']))

                    if len(all_token_information[0]) > 14: 
                        for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                            if str(eth_address) != '0' or '':
                                token1eth = uniswap_wrapper.get_eth_token_input_price(
                                    w33.toChecksumAddress(eth_address),
                                    10000000000000)
                                if decimals != 18:
                                    pricetoken1usd = (priceeth / (token1eth)) / (10 ** (18 - (decimals)))
                                else:
                                    pricetoken1usd = (priceeth / (token1eth))
                                a = pricetoken1usd
                                all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                          :13] + (a, all_token_information[
                                    token_number - 1][14])
                            else:
                                a = 0
                                all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                          :13] + (a, all_token_information[
                                    token_number - 1][14])
                    else:
                        for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance in all_token_information:
                            if str(eth_address) != '0' or '':
                                try:
                                    token1eth = uniswap_wrapper.get_eth_token_input_price(
                                        w33.toChecksumAddress(eth_address),
                                        10000000000000)
                                    if decimals != 18:
                                        pricetoken1usd = (priceeth / (token1eth)) / (10 ** (18 - (decimals)))
                                    else:
                                        pricetoken1usd = (priceeth / (token1eth))
                                    a = pricetoken1usd
                                    all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                              :13] + (a,)
                                except Exception as e:
                                    exception_type, exception_object, exception_traceback = sys.exc_info()
                                    if configfile.debugmode == '1':
                                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                                        e = (str(e))
                                    if 'Could not decode' in str(e):
                                        try:
                                            kanka = uniconnect.factory_contract.functions.getPair(
                                                w33.toChecksumAddress(eth_address),
                                                token22).call()
                                            kanka2 = uniconnect._load_contract(abi_name="erc20",
                                                                               address=w33.toChecksumAddress(
                                                                                   eth_address)).functions.balanceOf(
                                                kanka).call
                                            if kanka2 < 2:
                                                print(
                                                    'Token ' + str(token_number) + ' has no liquidity on Pancakeswap 2')
                                        except:
                                            print(
                                                'Token ' + str(token_number) + ' has no liquidity on Pancakeswap 2')
                                    b = None
                                    letsgoo = 0

                            else:
                                a = 0
                                all_token_information[token_number - 1] = all_token_information[token_number - 1] + (a,)

                    # its now: for token_number,eth_address,high,low,activate,stoploss_value,stoploss_activate,trade_with_ERC,trade_with_ETH,fast_token,small_case_name,decimals,balance,price in all_token_information:
                except Exception as e:
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                totalbalancedollarscript = 0
                if len(all_token_information[0]) > 15:
                    all_token_information[0] = all_token_information[0][:15]
                    all_token_information[1] = all_token_information[1][:15]
                    all_token_information[2] = all_token_information[2][:15]
                    all_token_information[3] = all_token_information[3][:15]
                    all_token_information[4] = all_token_information[4][:15]
                    all_token_information[5] = all_token_information[5][:15]
                    all_token_information[6] = all_token_information[6][:15]
                    all_token_information[7] = all_token_information[7][:15]
                    all_token_information[8] = all_token_information[8][:15]
                    all_token_information[9] = all_token_information[9][:15]
                if len(all_token_information[0]) > 14:
                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                        if balance != 0:
                            a = price * balance * 100
                            all_token_information[token_number - 1] = all_token_information[token_number - 1][:14] + (
                            a,)
                        else:
                            a = 0
                            all_token_information[token_number - 1] = all_token_information[token_number - 1][:14] + (
                            a,)

                        totalbalancedollarscript += a
                        if token_number == 10:
                            totalbalancedollarscript += dollarbalancemaintoken
                else:
                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price in all_token_information:
                        if balance != 0:
                            a = price * balance * 100
                            all_token_information[token_number - 1] = all_token_information[token_number - 1] + (a,)
                        else:
                            a = 0
                            all_token_information[token_number - 1] = all_token_information[token_number - 1] + (a,)

                        totalbalancedollarscript += a
                        if token_number == 10:
                            totalbalancedollarscript += dollarbalancemaintoken

                # its now: for token_number,eth_address,high,low,activate,stoploss_value,stoploss_activate,trade_with_ERC,
                # trade_with_ETH,fast_token,small_case_name,decimals,balance,price, dollar_balance in all_token_information:

                maintokenbalance = balance_eth
                return {'all_token_information': all_token_information,
                        'totalbalancedollarscript': totalbalancedollarscript,
                        'dollarbalancemaintoken': dollarbalancemaintoken, 'maintokenbalance': maintokenbalance}

                
            QCoreApplication.processEvents()
            if 'step' not in locals():
                step = 1
            else:
                step = 1
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()
            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))

            def checkbalance(all_token_information, infura_url, my_address, maincoinoption, dollarbalancemaintoken,
                             mcotoseeassell):

                ethereum_address = my_address
                cg = CoinGeckoAPI()

                ethbalance = pyetherbalance.PyEtherBalance(infura_url)

                for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                    if (dollarbalancemaintoken > mcotoseeassell):
                        gelukt = "sell"
                    else:
                        lol543 = dollar_balance * 100000000000
                        if lol543 > mcotoseeassell:
                            gelukt = "buy " + small_case_name
                    keer = 0
                    if 'gelukt' not in locals():
                        gelukt = 'nothing'
                QCoreApplication.processEvents()
                if 'step' not in locals():
                    step = 1
                else:
                    step = 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                    if (dollarbalancemaintoken > mcotoseeassell and gelukt != "sell"):
                        gelukt2 = "sell"
                    else:
                        if dollar_balance > mcotoseeassell and gelukt != 'buy ' + small_case_name:
                            gelukt2 = "buy " + small_case_name
                    keer = 0
                    if 'gelukt2' not in locals():
                        gelukt2 = 'nothing'
                try:
                    gelukt3 = gelukt2
                except:
                    gelukt2 = '0'
                return {'keer': keer, 'gelukt': gelukt, 'gelukt2': gelukt2,
                        'all_token_information': all_token_information}

            def getprice(all_token_information, incaseofbuyinghowmuch, uniswap_wrapper, timesleep, gelukt,
                         maintokenbalance, ethaddress, maindecimals, totalbalancedollarscript):
                count = 0
                try:
                    QCoreApplication.processEvents()
                        
                    while count < timesleep:
                        count = count + 1
                        QtTest.QTest.qWait(1000)
                        QCoreApplication.processEvents()
                    QtTest.QTest.qWait(166)
                    if ethaddress == "0x0000000000000000000000000000000000000000" and maintokenbalance > 0.001:
                        priceeth = int(float(
                            (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                'price']))
                        threeeth = int(maintokenbalance * 1000000000000000000)
                    if ethaddress == "0x0000000000000000000000000000000000000000" and maintokenbalance < 0.001:
                        threeeth = 1
                        priceeth = int(float(
                            (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                'price']))
                    if ethaddress != "0x0000000000000000000000000000000000000000":
                        if ethaddress == "0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3":
                            jajaja = (float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BUSDDAI').json())[
                                    'price']))
                            priceeth = int(float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                    'price']))
                            ethtest = (jajaja / priceeth) * maintokenbalance
                            if ethtest < 0.01:
                                threeeth = 1
                            else:
                                threeeth = int((ethtest) * 1000000000000000000)

                        if ethaddress == "0xe9e7cea3dedca5984780bafc599bd69add087d56":
                            jajaja = (float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BUSDUSDT').json())[
                                    'price']))
                            priceeth = int(float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                    'price']))
                            ethtest = (jajaja / priceeth) * maintokenbalance

                            if ethtest < 0.01:
                                threeeth = 1
                            else:
                                threeeth = int((ethtest) * 1000000000000000000)

                        if ethaddress == "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d":
                            jajaja = (float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=USDCBUSD').json())[
                                    'price']))
                            priceeth = int(float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                    'price']))
                            ethtest = (jajaja / priceeth) * maintokenbalance
                            if ethtest < 0.01:
                                threeeth = 1
                            else:
                                threeeth = int((ethtest) * 1000000000000000000)

                        if ethaddress == "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c":
                            jajaja = (float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT').json())[
                                    'price']))
                            priceeth = int(float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                    'price']))
                            ethtest = (jajaja / priceeth) * maintokenbalance
                            if ethtest < 0.01:
                                threeeth = 1
                            else:
                                threeeth = int((ethtest) * 1000000000000000000)
                        if ethaddress == "0x2170ed0880ac9a755fd29b2688956bd959f933f8":
                            jajaja = (float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json())[
                                    'price']))
                            priceeth = int(float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                    'price']))
                            ethtest = (jajaja / priceeth) * maintokenbalance
                            if ethtest < 0.01:
                                threeeth = 1
                            else:
                                threeeth = int((ethtest) * 1000000000000000000)
                    QCoreApplication.processEvents()
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()
                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                    if 'buy' in gelukt:
                        priceright = 'buy'
                        threeeth = int((totalbalancedollarscript / int(float(
                            (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                'price']))) * 1000000000000000000)
                    else:
                        priceright = 'sell'
                    if ethaddress == "0x0000000000000000000000000000000000000000":
                        dollarbalancemaintoken = maintokenbalance * (priceeth)
                    else:
                        token11eth = uniswap_wrapper.get_token_eth_output_price(w33.toChecksumAddress(ethaddress),
                                                                                threeeth)
                        token11eth2 = token11eth / threeeth

                        if maindecimals != 18:
                            dollarbalancemaintoken = float(maintokenbalance) * ((priceeth / (token11eth2)) / (
                                    10 ** (18 - (maindecimals))))
                        else:
                            dollarbalancemaintoken = maintokenbalance * (priceeth / (token11eth2))
                    priceeth = int(float(
                        (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())['price']))
                    QCoreApplication.processEvents()
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()
                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))

                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                        trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                        if eth_address != '0':
                            if priceright == 'sell':
                                token1eth = uniswap_wrapper.get_eth_token_input_price(
                                    w33.toChecksumAddress(eth_address),
                                    threeeth)
                                token1eth2 = token1eth / threeeth
                                if decimals != 18:
                                    pricetoken1usd = (priceeth / (token1eth2)) / (10 ** (18 - (decimals)))
                                    dollarbalancetoken1 = pricetoken1usd * balance
                                    all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                              :13] + (
                                                                              pricetoken1usd, dollarbalancetoken1)
                                else:
                                    pricetoken1usd = (priceeth / (token1eth2))
                                    dollarbalancetoken1 = pricetoken1usd * balance
                                    if eth_address == '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d':
                                        pricetoken1usd = 1.032319
                                    all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                              :13] + (
                                                                              pricetoken1usd, dollarbalancetoken1)
                            else:
                                token1eth = uniswap_wrapper.get_token_eth_output_price(
                                    w33.toChecksumAddress(eth_address),
                                    threeeth)
                                token1eth2 = (token1eth / threeeth)
                                if decimals != 18:
                                    pricetoken1usd = (priceeth / (token1eth2)) / (10 ** (18 - (decimals)))
                                    dollarbalancetoken1 = pricetoken1usd * balance
                                    all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                              :13] + (
                                                                              pricetoken1usd, dollarbalancetoken1)
                                else:
                                    pricetoken1usd = (priceeth / (token1eth2))
                                    dollarbalancetoken1 = pricetoken1usd * balance
                                    if eth_address == '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d':
                                        pricetoken1usd = 1.032319
                                    all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                              :13] + (
                                                                              pricetoken1usd, dollarbalancetoken1)
                        else:
                            pricetoken1usd = 0
                            dollarbalancetoken1 = 0
                            all_token_information[token_number - 1] = all_token_information[token_number - 1][:13] + (
                            pricetoken1usd, dollarbalancetoken1)
                    
                    weergave = ''

                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                        trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                        if eth_address != '0' and activate == 1:
                            weergave += ('   [' + small_case_name + '  ' + str("{:.8f}".format(price)) + ']')
                    QCoreApplication.processEvents()
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()
                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                    return {'all_token_information': all_token_information, 'priceeth': priceeth, 'weergave': weergave,
                            'dollarbalancemaintoken': dollarbalancemaintoken}
                except Exception as e:
                    o = 0
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))

            def letstrade(all_token_information, keer, my_address, pk, max_slippage,
                          infura_url, gelukt,
                          tokentokennumerator,
                          weergave, notyet, priceeth, speed, maxgwei, maxgweinumber, diffdeposit, diffdepositaddress,
                          maindecimals, timesleepaftertrade):
                QCoreApplication.processEvents()
                if 'step' not in locals():
                    step = 1
                else:
                    step = 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                    trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                    QCoreApplication.processEvents()
                    for token_number2, eth_address2, high2, low2, activate2, stoploss_value2, stoploss_activate2, trade_with_ERC2, \
                        trade_with_ETH2, fast_token2, small_case_name2, decimals2, balance2, price2, dollar_balance2 in all_token_information:
                        if eth_address != eth_address2:
                            if eth_address != 0 and eth_address2 != 0:
                                if price > ((high + low) / 2) and price2 < (
                                        (high2 + low2) / 2):
                                    locals()['token%stotoken%s' % (str(token_number), str(token_number2))] = ((
                                                                                                                          price - low) / (
                                                                                                                          high - low)) / (
                                                                                                                     (
                                                                                                                                 price2 - low2) / (
                                                                                                                                 high2 - low2))
                                else:
                                    locals()['token%stotoken%s' % (str(token_number), str(token_number2))] = 0.1
                            else:
                                locals()['token%stotoken%s' % (str(token_number), str(token_number2))] = 0.1

                def makeTrade(buytokenaddress, selltokenaddress, my_address, pk, max_slippage, infura_url,
                              buysmallcasesymbol, sellsmallcasesymbol, ethtokeep, speed, maxgwei, maxgweinumber,
                              diffdeposit, diffdepositaddress, ethaddress):
                    selldecimals = 18
                    try:
                        def api(speed):
                            res = requests.get(
                                'https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key=f2ff6e6755c2123799676dbe8ed3af94574000b4c9b56d1f159510ec91b0')
                            data = int(res.json()[speed] / 10)
                            return data

                        
                        print(
                            'Current gwei chosen for trading:' + configfile.maxgweinumber + '.   Current BNB price:$' + str(
                                int(float(
                                    (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                        'price']))))
                        gwei = types.Wei(Web3.toWei(int(configfile.maxgweinumber), "gwei"))

                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        w33.eth.setGasPriceStrategy(fast_gas_price_strategy)
                    if 1 == 1:

                        try:
                            uniconnect = Uniswap(my_address, pk, web3=Web3(
                                w33.HTTPProvider(infura_url)),
                                                 version=2, max_slippage=max_slippage)
                            eth = Web3.toChecksumAddress(selltokenaddress)
                            token = w33.toChecksumAddress(buytokenaddress)
                            selldecimals = 18
                        except Exception as e:
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            if configfile.debugmode == '1':
                                print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        try:
                            if selltokenaddress == "0x0000000000000000000000000000000000000000":
                                ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                                balance_eth = ethbalance.get_eth_balance(my_address)
                                priceeth = int(float(
                                    (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                        'price']))
                                ethamount2 = (float(balance_eth['balance'])) - (
                                        ethtokeep / (float(priceeth)))
                            else:
                                ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                                balance_eth = ethbalance.get_eth_balance(my_address)['balance']
                                token2 = sellsmallcasesymbol.upper
                                details2 = {'symbol': sellsmallcasesymbol.upper, 'address': selltokenaddress,
                                            'decimals': selldecimals,
                                            'name': sellsmallcasesymbol.upper}
                                erc20tokens2 = ethbalance.add_token(token2, details2)
                                ethamount2 = ethbalance.get_token_balance(token2, ethereum_address)['balance']
                            tradeamount = ethamount2 * 10 ** selldecimals
                            ethamount = tradeamount
                            eth = Web3.toChecksumAddress(selltokenaddress)
                            token = w33.toChecksumAddress(buytokenaddress)
                            contractaddress = token
                        except Exception as e:
                            o = 0
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            if configfile.debugmode == '1':
                                print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        tradeamount = int((ethamount2 / 1.000000001) * 10 ** selldecimals)
                        if len(str(tradeamount)) > 2:
                            tradeamount = int(str(tradeamount)[:-4] + '0000')
                        if tradeamount < 0:
                            tradeamount = int(1)

                        ethamount = ethamount2
                        contractaddress = token
                        if int(diffdeposit) == 0:
                            uniconnect.make_trade(eth, token, tradeamount, gwei, my_address, pk, my_address)
                        if int(diffdeposit) == 1:
                            uniconnect.make_trade(eth, token, tradeamount, gwei, my_address, pk, diffdepositaddress)

                        if buytokenaddress == ethaddress:
                            gelukt = 'sell'
                        if buytokenaddress != ethaddress:
                            gelukt = 'buy ' + buysmallcasesymbol
                        return {'gelukt': gelukt}
                    else:
                        print(
                            'Current gwei chosen for trading:' + configfile.maxgweinumber + '.   Current BNB price:$' + str(
                                int(float(
                                    (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                        'price']))))
                        gelukt = 'mislukt'
                        return {'gelukt': gelukt}

                QCoreApplication.processEvents()
                if 'step' not in locals():
                    step = 1
                else:
                    step = 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))

                try:
                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:  # stop loss
                        if (
                                price < stoploss_value and stoploss_activate == 1 and activate == 1 and trade_with_ETH == 1 and gelukt == "buy " + small_case_name) or (
                                price < stoploss_value and activate == 1 and trade_with_ETH == 1 and gelukt2 == "buy " + small_case_name and stoploss_activate == 1):
                            print("Selling " + str(
                                small_case_name) + ' for Maincoin-option (current price in USD: ' + str(
                                price) + ')')
                            buysmallcasesymbol = 'eth'
                            kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=eth_address,
                                             my_address=my_address,
                                             pk=private_key, max_slippage=max_slippage, infura_url=infura_url,
                                             buysmallcasesymbol=buysmallcasesymbol,
                                             sellsmallcasesymbol=small_case_name, ethtokeep=ethtokeep, speed=speed,
                                             maxgwei=maxgwei, maxgweinumber=maxgweinumber, diffdeposit=diffdeposit,
                                             diffdepositaddress=diffdepositaddress, ethaddress=ethaddress)
                            gelukt = kaka['gelukt']
                            if gelukt != 'mislukt':
                                count = 0
                                while count < timesleepaftertrade:
                                    count += 1
                                    QtTest.QTest.qWait(1000)
                                    QCoreApplication.processEvents()
                                    if self.__abort == True:
                                        count += 100
                            keer = 9999
                            fasttoken1 = 0
                            all_token_information[token_number - 1] = all_token_information[token_number - 1][:9] + (
                            fasttoken1, all_token_information[token_number - 1][10],
                            all_token_information[token_number - 1][11], all_token_information[token_number - 1][12],
                            all_token_information[token_number - 1][13], all_token_information[token_number - 1][14])
                        if (
                                eth_address != 0) and activate == 1 and trade_with_ETH == 1:  # sell alt and buy ETH trades
                            if (price > high and gelukt == "buy " + small_case_name) or (
                                    price > high and gelukt2 == "buy " + small_case_name) or (
                                    activate == 1 and gelukt == 'buy ' + small_case_name and fast_token == 1):
                                print("Selling " + str(
                                    small_case_name) + ' for Maincoin-option (current price in USD: ' + str(
                                    price) + ')')
                                buysmallcasesymbol = 'eth'
                                kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=eth_address,
                                                 my_address=my_address,
                                                 pk=private_key, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=buysmallcasesymbol,
                                                 sellsmallcasesymbol=small_case_name, ethtokeep=ethtokeep, speed=speed,
                                                 maxgwei=maxgwei, maxgweinumber=maxgweinumber, diffdeposit=diffdeposit,
                                                 diffdepositaddress=diffdepositaddress, ethaddress=ethaddress)
                                gelukt = kaka['gelukt']
                                if gelukt != 'mislukt':
                                    count = 0
                                    while count < timesleepaftertrade:
                                        count += 1
                                        QtTest.QTest.qWait(1000)
                                        QCoreApplication.processEvents()
                                        if self.__abort == True:
                                            count += 100
                                        if 'step' not in locals():
                                            step = 1
                                        else:
                                            step = 1
                                        self.sig_step.emit(self.__id, 'step ' + str(step))
                                        QCoreApplication.processEvents()
                                        if self.__abort == True:
                                            # note that "step" value will not necessarily be same for every thread
                                            self.sig_msg.emit(
                                                'Worker #{} aborting work at step {}'.format(self.__id, step))
                                keer = 9999
                                fasttoken1 = 0
                                all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                          :9] + (fasttoken1, all_token_information[
                                    token_number - 1][10], all_token_information[token_number - 1][11],
                                                                                 all_token_information[
                                                                                     token_number - 1][12],
                                                                                 all_token_information[
                                                                                     token_number - 1][13],
                                                                                 all_token_information[
                                                                                     token_number - 1][14])
                        if (eth_address != 0) and activate == 1 and trade_with_ETH == 1:  # sell ETH and buy ALT
                            if (price < low and gelukt == "sell") or (
                                    price < low and gelukt2 == "sell"):
                                print(
                                    "Buying " + str(small_case_name) + ' (Current price: ' + str(
                                        float(price)) + ')')

                                sellsmallcasesymbol = 'eth'
                                kaka = makeTrade(buytokenaddress=eth_address, selltokenaddress=ethaddress,
                                                 my_address=my_address,
                                                 pk=private_key, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=small_case_name,
                                                 sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep,
                                                 speed=speed,
                                                 maxgwei=maxgwei, maxgweinumber=maxgweinumber, diffdeposit=diffdeposit,
                                                 diffdepositaddress=diffdepositaddress, ethaddress=ethaddress)
                                gelukt = kaka['gelukt']
                                if gelukt != 'mislukt':
                                    count = 0
                                    while count < timesleepaftertrade:
                                        count += 1
                                        QtTest.QTest.qWait(1000)
                                        QCoreApplication.processEvents()
                                        if self.__abort == True:
                                            count += 100
                                        if 'step' not in locals():
                                            step = 1
                                        else:
                                            step = 1
                                        self.sig_step.emit(self.__id, 'step ' + str(step))
                                        QCoreApplication.processEvents()
                                        if self.__abort == True:
                                            # note that "step" value will not necessarily be same for every thread
                                            self.sig_msg.emit(
                                                'Worker #{} aborting work at step {}'.format(self.__id, step))
                                keer = 9999
                        QCoreApplication.processEvents()
                        for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                            trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                            QCoreApplication.processEvents()
                            for token_number2, eth_address2, high2, low2, activate2, stoploss_value2, stoploss_activate2, trade_with_ERC2, \
                                trade_with_ETH2, fast_token2, small_case_name2, decimals2, balance2, price2, dollar_balance2 in all_token_information:
                                if eth_address2 != eth_address:
                                    if (eth_address != 0) and (
                                            eth_address2 != 0) and activate == 1 and trade_with_ETH == 1 \
                                            and activate2 == 1 and trade_with_ETH2 == 1 and trade_with_ERC == 1 and trade_with_ERC2 == 1:
                                        if (
                                                locals()['token%stotoken%s' % (str(token_number), str(
                                                    token_number2))] > tokentokennumerator and gelukt == "buy " + small_case_name) or (
                                                locals()['token%stotoken%s' % (str(token_number), str(
                                                    token_number2))] > tokentokennumerator and gelukt2 == "buy " + small_case_name):
                                            print("Trading " + str(small_case_name) + ' ($' + str(
                                                price) + ') for ' + str(small_case_name2) + " ($" + str(
                                                price2) + ")")
                                            
                                            kaka = makeTrade(buytokenaddress=eth_address2, selltokenaddress=eth_address,
                                                             my_address=my_address,
                                                             pk=private_key, max_slippage=max_slippage, infura_url=infura_url,
                                                             buysmallcasesymbol=small_case_name2,
                                                             sellsmallcasesymbol=small_case_name, ethtokeep=ethtokeep,
                                                             speed=speed, maxgwei=maxgwei, maxgweinumber=maxgweinumber,
                                                             diffdeposit=diffdeposit,
                                                             diffdepositaddress=diffdepositaddress,
                                                             ethaddress=ethaddress)
                                            gelukt = kaka['gelukt']
                                            if gelukt != 'mislukt':
                                                count = 1
                                                while count < timesleepaftertrade:
                                                    count += 1
                                                    if self.__abort == True:
                                                        count += 100
                                                    QtTest.QTest.qWait(1000)
                                                    QCoreApplication.processEvents()
                                                    if 'step' not in locals():
                                                        step = 1
                                                    else:
                                                        step = 1
                                                    self.sig_step.emit(self.__id, 'step ' + str(step))
                                                    QCoreApplication.processEvents()
                                                    if self.__abort == True:
                                                        # note that "step" value will not necessarily be same for every thread
                                                        self.sig_msg.emit(
                                                            'Worker #{} aborting work at step {}'.format(self.__id,
                                                                                                         step))
                                            keer = 9999
                        QCoreApplication.processEvents()
                except Exception as e:
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    traceback.print_exc()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                    gelukt = 'mislukt'
                return {'gelukt': gelukt, 'keer': keer, 'all_token_information': all_token_information}

            if 'step' not in locals():
                step = 1
            else:
                step = 1
            QCoreApplication.processEvents()
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()
            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
            # def marketordersell():
            # def marketorderbuy():

            # def preapproval():

            # def recharge():

            # paytokenholding
            if 0 == 1:
                details2 = {'symbol': paytokensmallname, 'address': paytokenaddress,
                            'decimals': paytokendecimals,
                            'name': paytokenname}
                erc20tokens2 = ethbalance.add_token(token2, details2)
                ethamount2 = ethbalance.get_token_balance(paytokenname, my_address)['balance']
                QCoreApplication.processEvents()
                if ethamount2 < paytokenamount:
                    print("You are not holding the required token, the application will now stop")
                    exit()
                    subprocess.call(["taskkill", "/F", "/IM", "bot.exe"])
                    QtTest.QTest.qWait(4294960 * 1000)
            if 'step' not in locals():
                step = 1
            else:
                step = 1
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()

            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
            while self.__abort != True:
                w3 = Web3(Web3.HTTPProvider(infura_url))
                w33 = Web3()
                address = my_address
                private_key = private_key
                QCoreApplication.processEvents()
                uniswap_wrapper = Uniswap(address, private_key, web3=w3, version=2)
                ethereum_address = address
                pieuw = gettotaltokenbalance(all_token_information, infura_url, ethaddress, maindecimals, my_address,
                                             ethtokeep)
                QCoreApplication.processEvents()
                all_token_information = pieuw['all_token_information']
                totalbalancedollarscript = pieuw['totalbalancedollarscript']
                dollarbalancemaintoken = pieuw['dollarbalancemaintoken']
                maintokenbalance = pieuw['maintokenbalance']
                try:
                    w33 = Web3()
                    try:
                        def api(speed):
                            res = requests.get(
                                'https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key=f2ff6e6755c2123799676dbe8ed3af94574000b4c9b56d1f159510ec91b0')
                            data = (res.json()[speed]) / 10
                            return data

                        gwei = int(configfile.maxgweinumber)
                        print(
                            'Current gwei chosen for trading:' + configfile.maxgweinumber + '.   Current BNB price:$' + str(
                                int(float(
                                    (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                        'price']))))

                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        # w33.eth.setGasPriceStrategy(fast_gas_price_strategy)
                    w33.middleware_onion.add(middleware.time_based_cache_middleware)
                    w33.middleware_onion.add(middleware.latest_block_based_cache_middleware)
                    w33.middleware_onion.add(middleware.simple_cache_middleware)
                    w3 = Web3(Web3.HTTPProvider(infura_url))
                    QCoreApplication.processEvents()
                    keer543 = 0
                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                        trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                        if (eth_address == '0' or '') or activate == 0:
                            keer543 += 1
                    
                    if keer543 == 10:
                        print(
                            'Please stop the application and add at least token1, otherwise the application will do nothing. Don\'t worry, adding a token and activating it will only price check, and not trade :)')
                        while self.__abort != True:
                            QCoreApplication.processEvents()
                            pass
                    address = my_address
                    private_key = private_key
                    QCoreApplication.processEvents()
                    uniswap_wrapper = Uniswap(address, private_key, web3=w3, version=2)
                    ethereum_address = address
                    if 'gelukt' not in locals() or gelukt == "mislukt" or gelukt == "mislukt buy" or gelukt == "mislukt sell":
                        if 'step' not in locals():
                            step = 1
                        else:
                            step = step + 1
                        self.sig_step.emit(self.__id, 'step ' + str(step))
                        QCoreApplication.processEvents()

                        if self.__abort == True:
                            # note that "step" value will not necessarily be same for every thread
                            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                        rara = checkbalance(all_token_information, infura_url, my_address, maincoinoption,
                                            dollarbalancemaintoken, mcotoseeassell)
                        all_token_information = rara['all_token_information']
                        gelukt = rara['gelukt']
                        gelukt2 = rara['gelukt2']
                        keer = rara['keer']

                        print('Last thing we did is ' + gelukt + '. Second token available for trading is ' + gelukt2)
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = step + 1
                    QCoreApplication.processEvents()
                    while self.__abort != True:
                        # check if we need to abort the loop; need to process events to receive signals;
                        self.sig_step.emit(self.__id, 'step ' + str(step))
                        QCoreApplication.processEvents()
                        if self.__abort == True:
                            # note that "step" value will not necessarily be same for every thread
                            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                        keer = keer + 1
                        QCoreApplication.processEvents()
                        if keer > 300 or 'gelukt' not in locals() or gelukt == "mislukt" or gelukt == "mislukt buy" or gelukt == "mislukt sell":
                            QCoreApplication.processEvents()
                            pieuw = gettotaltokenbalance(all_token_information, infura_url, ethaddress, maindecimals,
                                                         my_address, ethtokeep)
                            all_token_information = pieuw['all_token_information']
                            totalbalancedollarscript = pieuw['totalbalancedollarscript']
                            dollarbalancemaintoken = pieuw['dollarbalancemaintoken']
                            maintokenbalance = pieuw['maintokenbalance']
                            QCoreApplication.processEvents()
                            rara = checkbalance(all_token_information, infura_url, my_address, maincoinoption,
                                                dollarbalancemaintoken, mcotoseeassell)
                            all_token_information = rara['all_token_information']
                            gelukt = rara['gelukt']
                            gelukt2 = rara['gelukt2']
                            keer = rara['keer']
                            QCoreApplication.processEvents()
                        QCoreApplication.processEvents()
                        try:
                            if "weergave" in locals():
                                weergave1 = weergave
                            if 'step' not in locals():
                                step = 1
                            else:
                                step = step + 1
                            self.sig_step.emit(self.__id, 'step ' + str(step))
                            QCoreApplication.processEvents()

                            if self.__abort == True:
                                # note that "step" value will not necessarily be same for every thread
                                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                            ku = getprice(all_token_information, incaseofbuyinghowmuch, uniswap_wrapper, timesleep,
                                          gelukt, maintokenbalance, ethaddress, maindecimals, totalbalancedollarscript)

                            QCoreApplication.processEvents()
                            weergave12 = ku['weergave']
                            weergave = weergave12
                            priceeth = ku['priceeth']
                            all_token_information = ku['all_token_information']

                            totaldollars = dollarbalancemaintoken + all_token_information[0][14] + \
                                           all_token_information[1][14] + all_token_information[2][14] + \
                                           all_token_information[3][14] + all_token_information[4][14] + \
                                           all_token_information[5][14] + all_token_information[6][14] + \
                                           all_token_information[7][14] + all_token_information[8][14] + \
                                           all_token_information[9][14]

                            QCoreApplication.processEvents()
                            weergavegeld = str(configfile.maincoinoption) + ':$' + str(
                                "{:.2f}".format(dollarbalancemaintoken))
                            for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                                trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                                totaldollars += dollar_balance
                                if dollar_balance > 0:
                                    weergavegeld += '   ' + str(small_case_name) + ':$' + str(
                                        "{:.2f}".format(dollar_balance))
                            if 'nogeenkeer' not in locals():
                                nogeenkeer = 1
                                print('Current balance:  ' + weergavegeld)
                            else:
                                nogeenkeer = nogeenkeer + 1
                                if nogeenkeer > 300:
                                    print('Current balance:  ' + weergavegeld)
                                    nogeenkeer = 1
                            if 'step' not in locals():
                                step = 1
                            else:
                                step = step + 1
                            self.sig_step.emit(self.__id, 'step ' + str(step))
                            QCoreApplication.processEvents()
                            if self.__abort == True:
                                # note that "step" value will not necessarily be same for every thread
                                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                                break

                            if 'pricetoken1usd2' in locals() and 0 == 1:
                                for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                                    trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                                    if price / locals()['pricetoken%susd2' % (
                                    str(token_number))] >= 1.15 and price > low and gelukt == 'buy ' + small_case_name:
                                        all_token_information[token_number - 1] = all_token_information[
                                                                                      token_number - 1][:9] + (1,
                                                                                                               all_token_information[
                                                                                                                   token_number - 1][
                                                                                                                   10],
                                                                                                               all_token_information[
                                                                                                                   token_number - 1][
                                                                                                                   11],
                                                                                                               all_token_information[
                                                                                                                   token_number - 1][
                                                                                                                   12],
                                                                                                               all_token_information[
                                                                                                                   token_number - 1][
                                                                                                                   13],
                                                                                                               all_token_information[
                                                                                                                   token_number - 1][
                                                                                                                   14])
                                        all_token_information[token_number - 1] = all_token_information[
                                                                                      token_number - 1][:2] + (
                                                                                  price / 1.09, all_token_information[
                                                                                      token_number - 1][4],
                                                                                  all_token_information[
                                                                                      token_number - 1][5],
                                                                                  all_token_information[
                                                                                      token_number - 1][6],
                                                                                  all_token_information[
                                                                                      token_number - 1][7],
                                                                                  all_token_information[
                                                                                      token_number - 1][8],
                                                                                  all_token_information[
                                                                                      token_number - 1][9],
                                                                                  all_token_information[
                                                                                      token_number - 1][10],
                                                                                  all_token_information[
                                                                                      token_number - 1][11],
                                                                                  all_token_information[
                                                                                      token_number - 1][12],
                                                                                  all_token_information[
                                                                                      token_number - 1][13],
                                                                                  all_token_information[
                                                                                      token_number - 1][14])
                            if 1 == 1:
                                for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                                    trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                                    locals()['pricetoken%susd2' % (str(token_number))] = \
                                    all_token_information[token_number - 1][13]

                            notyet = 1
                            if 'step' not in locals():
                                step = 1
                            else:
                                step = step + 1
                            self.sig_step.emit(self.__id, 'step ' + str(step))
                            QCoreApplication.processEvents()

                            if self.__abort == True:
                                # note that "step" value will not necessarily be same for every thread
                                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                                break
                            if totaldollars < 0:
                                totaldollars2 = 0
                            else:
                                if (totaldollars * 0.9) > (all_token_information[0][14] + all_token_information[1][14] +
                                                           all_token_information[2][14] + all_token_information[3][14] +
                                                           all_token_information[4][14] + all_token_information[5][14] +
                                                           all_token_information[6][14] + all_token_information[7][14] +
                                                           all_token_information[8][14] + all_token_information[9][14]):
                                    if dollarbalancemaintoken < mcotoseeassell:
                                        totaldollars = totaldollars / 2
                                totaldollars2 = totaldollars
                            if "weergave1" not in locals() and "notyet" in locals():
                                print(str(strftime("%H:%M:%S",
                                                   localtime())) + weergave + "  Current total balance($): $" + str(
                                    "{:.2f}".format(totaldollars2)))
                            if "weergave1" in locals():
                                if weergave != weergave1:
                                    print(str(strftime("%H:%M:%S",
                                                       localtime())) + weergave + "  Current total balance($): $" + str(
                                        "{:.2f}".format(totaldollars2)))
                        
                        except Exception as e:
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            if configfile.debugmode == '1':
                                print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                            if e is not IndexError:
                                o = 0
                                exception_type, exception_object, exception_traceback = sys.exc_info()
                                if configfile.debugmode == '1':
                                    print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                            if 'step' not in locals():
                                step = 1
                            else:
                                step = step + 1
                            self.sig_step.emit(self.__id, 'step ' + str(step))
                            QCoreApplication.processEvents()

                            if self.__abort == True:
                                # note that "step" value will not necessarily be same for every thread
                                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                                break
                            QtTest.QTest.qWait(1000)
                            notyet = 0
                        if 'notyet' not in locals():
                            notyet = 0
                        else:
                            notyet = notyet + 1
                        if notyet > 0:
                            if 'step' not in locals():
                                step = 1
                            else:
                                step = step + 1
                            self.sig_step.emit(self.__id, 'step ' + str(step))
                            QCoreApplication.processEvents()

                            if self.__abort == True:
                                # note that "step" value will not necessarily be same for every thread
                                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                                break
                            oke = letstrade(all_token_information, keer, my_address, pk, max_slippage, infura_url,
                                            gelukt, tokentokennumerator, weergave, notyet, priceeth, speed, maxgwei,
                                            maxgweinumber, diffdeposit, diffdepositaddress, maindecimals,
                                            timesleepaftertrade)
                            all_token_information = oke['all_token_information']
                            gelukt = oke['gelukt']
                            gelukt2 = oke['gelukt']
                            keer = oke['keer']



                except Exception as e:
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = step + 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()

                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                        break
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                    if e is not IndexError:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        # o=0
                    import socket

                    def is_connected():
                        try:
                            # connect to the host -- tells us if the host is actually
                            # reachable
                            socket.create_connection(("1.1.1.1", 53))
                            return True
                        except OSError:
                            pass
                        return False

                    internetcheck = is_connected()
                    if internetcheck is False:
                        try:
                            count = 0
                            while self.__abort != True or count < 5:
                                count += 1
                                QtTest.QTest.qWait(1000)
                                QCoreApplication.processEvents()
                        except:
                            count = 0
                            while self.__abort != True or count < 5:
                                count += 1
                                QtTest.QTest.qWait(1000)
                                QCoreApplication.processEvents()
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = step + 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()
                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
            if 'step' not in locals():
                step = 1
            else:
                step = step + 1
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()

            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
            self.sig_done.emit(self.__id)

    
    def abort(self):
        self.sig_msg.emit('Worker #{} notified to abort'.format(self.__id))
        self.__abort = True


# def funtie voor toevoeging tokens en automaties make trade met elkaar maken --> done alleen testen
# GUI maken en gebruiken mey pyqt desinger
# functie maken voor auto high low
# winst toevoegen tijdens runtime (hiervoor extra configfiletje maken)
# GUI maken mey pyqt desinger

def abort(self):
    self.__abort = True


class Ui_MainWindow(QGraphicsObject):
    NUM_THREADS = 1
    sig_abort_workers = pyqtSignal()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1056, 702)
        form_layout = QVBoxLayout()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startbutton = QtWidgets.QPushButton(self.centralwidget)
        self.startbutton.setGeometry(QtCore.QRect(920, 590, 121, 71))
        self.startbutton.setObjectName("startbutton")
        self.stopbutton = QtWidgets.QPushButton(self.centralwidget)
        self.stopbutton.setGeometry(QtCore.QRect(750, 590, 171, 71))
        self.stopbutton.setObjectName("stopbutton")

        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(0, 0, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.oke = self.startbutton.clicked.connect(self.start_threads)
        self.stopbutton.clicked.connect(self.abort_workers)
        self.activatetoken1 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken1.setGeometry(QtCore.QRect(440, 50, 91, 20))
        form_layout.addWidget(self.stopbutton)
        self.stopbutton.setDisabled(True)

        self.process = QtCore.QProcess(self)
        self.process.setProgram("dirb")
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.maincoinoption = QtWidgets.QComboBox(self.centralwidget)
        self.maincoinoption.setGeometry(QtCore.QRect(130, 0, 81, 21))
        self.maincoinoption.setMaxVisibleItems(6)
        self.maincoinoption.setObjectName("maincoinoption")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(750, 370, 291, 16))
        self.label_17.setObjectName("label_17")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken1.setFont(font)
        self.log = QTextEdit()
        form_layout.addWidget(self.log)
        self.activatetoken1.setObjectName("activatetoken1")
        self.tradewithETHtoken1 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken1.setGeometry(QtCore.QRect(540, 50, 141, 20))
        self.tradewithETHtoken1.setObjectName("tradewithETHtoken1")
        self.tradewithERCtoken1 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken1.setGeometry(QtCore.QRect(690, 50, 151, 20))
        self.tradewithERCtoken1.setObjectName("tradewithERCtoken1")
        self.tradewithETHtoken2 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken2.setGeometry(QtCore.QRect(540, 80, 141, 20))
        self.tradewithETHtoken2.setObjectName("tradewithETHtoken2")
        self.activatetoken2 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken2.setGeometry(QtCore.QRect(440, 80, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken2.setFont(font)
        self.activatetoken2.setObjectName("activatetoken2")
        self.tradewithERCtoken2 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken2.setGeometry(QtCore.QRect(690, 80, 141, 20))
        self.tradewithERCtoken2.setObjectName("tradewithERCtoken2")
        self.tradewithETHtoken3 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken3.setGeometry(QtCore.QRect(540, 110, 141, 20))
        self.tradewithETHtoken3.setObjectName("tradewithETHtoken3")
        self.activatetoken3 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken3.setGeometry(QtCore.QRect(440, 110, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken3.setFont(font)
        self.activatetoken3.setObjectName("activatetoken3")
        self.tradewithERCtoken3 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken3.setGeometry(QtCore.QRect(690, 110, 141, 20))
        self.tradewithERCtoken3.setObjectName("tradewithERCtoken3")
        self.tradewithERCtoken5 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken5.setGeometry(QtCore.QRect(690, 170, 151, 20))
        self.tradewithERCtoken5.setObjectName("tradewithERCtoken5")
        self.tradewithETHtoken4 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken4.setGeometry(QtCore.QRect(540, 140, 141, 20))
        self.tradewithETHtoken4.setObjectName("tradewithETHtoken4")
        self.tradewithERCtoken6 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken6.setGeometry(QtCore.QRect(690, 200, 141, 20))
        self.tradewithERCtoken6.setObjectName("tradewithERCtoken6")
        self.tradewithETHtoken6 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken6.setGeometry(QtCore.QRect(540, 200, 141, 20))
        self.tradewithETHtoken6.setObjectName("tradewithETHtoken6")
        self.activatetoken4 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken4.setGeometry(QtCore.QRect(440, 140, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken4.setFont(font)
        self.activatetoken4.setObjectName("activatetoken4")
        self.activatetoken6 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken6.setGeometry(QtCore.QRect(440, 200, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken6.setFont(font)
        self.activatetoken6.setObjectName("activatetoken6")
        self.tradewithERCtoken4 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken4.setGeometry(QtCore.QRect(690, 140, 151, 20))
        self.tradewithERCtoken4.setObjectName("tradewithERCtoken4")
        self.tradewithETHtoken5 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken5.setGeometry(QtCore.QRect(540, 170, 141, 20))
        self.tradewithETHtoken5.setObjectName("tradewithETHtoken5")
        self.activatetoken5 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken5.setGeometry(QtCore.QRect(440, 170, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken5.setFont(font)
        self.activatetoken5.setObjectName("activatetoken5")
        self.tradewithERCtoken8 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken8.setGeometry(QtCore.QRect(690, 260, 141, 20))
        self.tradewithERCtoken8.setObjectName("tradewithERCtoken8")
        self.tradewithETHtoken7 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken7.setGeometry(QtCore.QRect(540, 230, 141, 20))
        self.tradewithETHtoken7.setObjectName("tradewithETHtoken7")
        self.tradewithERCtoken9 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken9.setGeometry(QtCore.QRect(690, 290, 141, 20))
        self.tradewithERCtoken9.setObjectName("tradewithERCtoken9")
        self.tradewithETHtoken9 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken9.setGeometry(QtCore.QRect(540, 290, 141, 20))
        self.tradewithETHtoken9.setObjectName("tradewithETHtoken9")
        self.activatetoken7 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken7.setGeometry(QtCore.QRect(440, 230, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken7.setFont(font)
        self.activatetoken7.setObjectName("activatetoken7")
        self.activatetoken9 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken9.setGeometry(QtCore.QRect(440, 290, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken9.setFont(font)
        self.activatetoken9.setObjectName("activatetoken9")
        self.tradewithERCtoken7 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken7.setGeometry(QtCore.QRect(690, 230, 141, 20))
        self.tradewithERCtoken7.setObjectName("tradewithERCtoken7")
        self.tradewithETHtoken8 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken8.setGeometry(QtCore.QRect(540, 260, 141, 20))
        self.tradewithETHtoken8.setObjectName("tradewithETHtoken8")
        self.activatetoken8 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken8.setGeometry(QtCore.QRect(440, 260, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken8.setFont(font)
        self.activatetoken8.setObjectName("activatetoken8")
        self.activatetoken10 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken10.setGeometry(QtCore.QRect(440, 320, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken10.setFont(font)
        self.activatetoken10.setObjectName("activatetoken10")
        self.tradewithETHtoken10 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken10.setGeometry(QtCore.QRect(540, 320, 141, 20))
        self.tradewithETHtoken10.setObjectName("tradewithETHtoken10")
        self.tradewithERCtoken10 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken10.setGeometry(QtCore.QRect(690, 320, 141, 20))
        self.tradewithERCtoken10.setObjectName("tradewithERCtoken10")

        try:
            self.stoplosstoken1 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken1.setGeometry(QtCore.QRect(840, 50, 111, 20))
            self.stoplosstoken2 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken2.setGeometry(QtCore.QRect(840, 80, 111, 20))
            self.stoplosstoken3 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken3.setGeometry(QtCore.QRect(840, 110, 111, 20))
            self.stoplosstoken4 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken4.setGeometry(QtCore.QRect(840, 140, 111, 20))
            self.stoplosstoken5 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken5.setGeometry(QtCore.QRect(840, 170, 111, 20))
            self.stoplosstoken6 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken6.setGeometry(QtCore.QRect(840, 200, 111, 20))
            self.stoplosstoken7 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken7.setGeometry(QtCore.QRect(840, 230, 111, 20))
            self.stoplosstoken8 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken8.setGeometry(QtCore.QRect(840, 260, 111, 20))
            self.stoplosstoken9 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken9.setGeometry(QtCore.QRect(840, 290, 111, 20))
            self.stoplosstoken10 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken10.setGeometry(QtCore.QRect(840, 320, 111, 20))

            self.debugmode = QtWidgets.QCheckBox(self.centralwidget)
            self.debugmode.setGeometry(QtCore.QRect(840, 10, 111, 20))

            self.mcotoseeassell = QtWidgets.QLineEdit(self.centralwidget)
            self.mcotoseeassell.setGeometry(QtCore.QRect(400, 0, 81, 21))
            self.label_99 = QtWidgets.QLabel(self.centralwidget)
            self.label_99.setGeometry(QtCore.QRect(230, 0, 180, 21))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            self.label_99.setFont(font)
            self.label_99.setObjectName("label_99")

            self.token1stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token1stoploss.setGeometry(QtCore.QRect(960, 50, 71, 16))
            self.token1stoploss.setObjectName("token1stoploss")
            self.token2stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token2stoploss.setGeometry(QtCore.QRect(960, 80, 71, 16))
            self.token2stoploss.setObjectName("token2stoploss")
            self.token3stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token3stoploss.setGeometry(QtCore.QRect(960, 110, 71, 16))
            self.token3stoploss.setObjectName("token3stoploss")
            self.token4stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token4stoploss.setGeometry(QtCore.QRect(960, 140, 71, 16))
            self.token4stoploss.setObjectName("token4stoploss")
            self.token5stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token5stoploss.setGeometry(QtCore.QRect(960, 170, 71, 16))
            self.token5stoploss.setObjectName("token5stoploss")
            self.token6stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token6stoploss.setGeometry(QtCore.QRect(960, 200, 71, 16))
            self.token6stoploss.setObjectName("token6stoploss")
            self.token7stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token7stoploss.setGeometry(QtCore.QRect(960, 230, 71, 16))
            self.token7stoploss.setObjectName("token7stoploss")
            self.token8stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token8stoploss.setGeometry(QtCore.QRect(960, 260, 71, 16))
            self.token8stoploss.setObjectName("token8stoploss")
            self.token9stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token9stoploss.setGeometry(QtCore.QRect(960, 290, 71, 16))
            self.token9stoploss.setObjectName("token9stoploss")
            self.token10stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token10stoploss.setGeometry(QtCore.QRect(960, 320, 71, 16))
            self.token10stoploss.setObjectName("token10stoploss")
            self.maxgweinumber = QtWidgets.QLineEdit(self.centralwidget)
            self.maxgweinumber.setGeometry(QtCore.QRect(830, 400, 71, 16))
            self.maxgweinumber.setObjectName("maxgweinumber")
            self.diffdeposit = QtWidgets.QCheckBox(self.centralwidget)
            self.diffdeposit.setGeometry(QtCore.QRect(710, 420, 211, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.diffdeposit.setFont(font)
            self.diffdeposit.setObjectName("diffdeposit")
            self.diffdepositaddress = QtWidgets.QLineEdit(self.centralwidget)
            self.diffdepositaddress.setGeometry(QtCore.QRect(930, 420, 111, 20))
            self.diffdepositaddress.setObjectName("diffdepositaddress")

        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            if configfile.debugmode == '1':
                print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))

        if 1 == 1:
            self.token1stoploss.setText(configfile.token1stoploss)
        if 1 == 1:
            self.token2stoploss.setText(configfile.token2stoploss)
        if 1 == 1:
            self.token3stoploss.setText(configfile.token3stoploss)
        if 1 == 1:
            self.token4stoploss.setText(configfile.token4stoploss)
        if 1 == 1:
            self.token5stoploss.setText(configfile.token5stoploss)
        if 1 == 1:
            self.token6stoploss.setText(configfile.token6stoploss)
        if 1 == 1:
            self.token7stoploss.setText(configfile.token7stoploss)
        if 1 == 1:
            self.token8stoploss.setText(configfile.token8stoploss)
        if 1 == 1:
            self.token9stoploss.setText(configfile.token9stoploss)
        if 1 == 1:
            self.token10stoploss.setText(configfile.token10stoploss)

        self.token1low = QtWidgets.QLineEdit(self.centralwidget)
        self.token1low.setGeometry(QtCore.QRect(320, 50, 51, 16))
        self.token1low.setObjectName("token1low")
        if configfile.token1low != '0':
            self.token1low.setText(configfile.token1low)
        self.token1high = QtWidgets.QLineEdit(self.centralwidget)
        self.token1high.setGeometry(QtCore.QRect(380, 50, 51, 16))
        self.token1high.setObjectName("token1high")
        if configfile.token1high != '0':
            self.token1high.setText(configfile.token1high)
        self.token1ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token1ethaddress.setGeometry(QtCore.QRect(70, 50, 121, 16))
        self.token1ethaddress.setObjectName("token1ethaddress")

        if configfile.mcotoseeassell != '':
            self.mcotoseeassell.setText(configfile.mcotoseeassell)

        if configfile.token1ethaddress != '0':
            self.token1ethaddress.setText(configfile.token1ethaddress)
        self.token2low = QtWidgets.QLineEdit(self.centralwidget)
        self.token2low.setGeometry(QtCore.QRect(320, 80, 51, 16))
        self.token2low.setObjectName("token2low")
        if configfile.token2low != '0':
            self.token2low.setText(configfile.token2low)
        self.token2ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token2ethaddress.setGeometry(QtCore.QRect(70, 80, 121, 16))
        self.token2ethaddress.setObjectName("token2ethaddress")
        if configfile.token2ethaddress != '0':
            self.token2ethaddress.setText(configfile.token2ethaddress)
        self.token2high = QtWidgets.QLineEdit(self.centralwidget)
        self.token2high.setGeometry(QtCore.QRect(380, 80, 51, 16))
        self.token2high.setObjectName("token2high")
        if configfile.token2high != '0':
            self.token2high.setText(configfile.token2high)
        self.token3low = QtWidgets.QLineEdit(self.centralwidget)
        self.token3low.setGeometry(QtCore.QRect(320, 110, 51, 16))
        self.token3low.setObjectName("token3low")
        if configfile.token3low != '0':
            self.token3low.setText(configfile.token3low)
        self.token3ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token3ethaddress.setGeometry(QtCore.QRect(70, 110, 121, 16))
        self.token3ethaddress.setObjectName("token3ethaddress")
        if configfile.token3ethaddress != '0':
            self.token3ethaddress.setText(configfile.token3ethaddress)
        self.token3high = QtWidgets.QLineEdit(self.centralwidget)
        self.token3high.setGeometry(QtCore.QRect(380, 110, 51, 16))
        self.token3high.setObjectName("token3high")
        if configfile.token3high != '0':
            self.token3high.setText(configfile.token3high)
        self.token6high = QtWidgets.QLineEdit(self.centralwidget)
        self.token6high.setGeometry(QtCore.QRect(380, 200, 51, 16))
        self.token6high.setObjectName("token6high")
        if configfile.token6high != '0':
            self.token6high.setText(configfile.token6high)
        self.token5high = QtWidgets.QLineEdit(self.centralwidget)
        self.token5high.setGeometry(QtCore.QRect(380, 170, 51, 16))
        self.token5high.setObjectName("token5high")
        if configfile.token5high != '0':
            self.token5high.setText(configfile.token5high)
        self.token4low = QtWidgets.QLineEdit(self.centralwidget)
        self.token4low.setGeometry(QtCore.QRect(320, 140, 51, 16))
        self.token4low.setObjectName("token4low")
        if configfile.token4low != '0':
            self.token4low.setText(configfile.token4low)
        self.token5low = QtWidgets.QLineEdit(self.centralwidget)
        self.token5low.setGeometry(QtCore.QRect(320, 170, 51, 16))
        self.token5low.setObjectName("token5low")
        if configfile.token5low != '0':
            self.token5low.setText(configfile.token5low)
        self.token4high = QtWidgets.QLineEdit(self.centralwidget)
        self.token4high.setGeometry(QtCore.QRect(380, 140, 51, 16))
        self.token4high.setObjectName("token4high")
        if configfile.token4high != '0':
            self.token4high.setText(configfile.token4high)
        self.token4ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token4ethaddress.setGeometry(QtCore.QRect(70, 140, 121, 16))
        self.token4ethaddress.setObjectName("token4ethaddress")
        if configfile.token4ethaddress != '0':
            self.token4ethaddress.setText(configfile.token4ethaddress)
        self.token6low = QtWidgets.QLineEdit(self.centralwidget)
        self.token6low.setGeometry(QtCore.QRect(320, 200, 51, 16))
        self.token6low.setObjectName("token6low")
        if configfile.token6low != '0':
            self.token6low.setText(configfile.token6low)
        self.token5ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token5ethaddress.setGeometry(QtCore.QRect(70, 170, 121, 16))
        self.token5ethaddress.setObjectName("token5ethaddress")
        if configfile.token5ethaddress != '0':
            self.token5ethaddress.setText(configfile.token5ethaddress)
        self.token6ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token6ethaddress.setGeometry(QtCore.QRect(70, 200, 121, 16))
        self.token6ethaddress.setObjectName("token6ethaddress")
        if configfile.token6ethaddress != '0':
            self.token6ethaddress.setText(configfile.token6ethaddress)
        self.token9high = QtWidgets.QLineEdit(self.centralwidget)
        self.token9high.setGeometry(QtCore.QRect(380, 290, 51, 16))
        self.token9high.setObjectName("token9high")
        if configfile.token9high != '0':
            self.token9high.setText(configfile.token9high)
        self.token8high = QtWidgets.QLineEdit(self.centralwidget)
        self.token8high.setGeometry(QtCore.QRect(380, 260, 51, 16))
        self.token8high.setObjectName("token8high")
        if configfile.token8high != '0':
            self.token8high.setText(configfile.token8high)
        self.token7low = QtWidgets.QLineEdit(self.centralwidget)
        self.token7low.setGeometry(QtCore.QRect(320, 230, 51, 16))
        self.token7low.setObjectName("token7low")
        if configfile.token7low != '0':
            self.token7low.setText(configfile.token7low)
        self.token8low = QtWidgets.QLineEdit(self.centralwidget)
        self.token8low.setGeometry(QtCore.QRect(320, 260, 51, 16))
        self.token8low.setObjectName("token8low")
        if configfile.token8low != '0':
            self.token8low.set
