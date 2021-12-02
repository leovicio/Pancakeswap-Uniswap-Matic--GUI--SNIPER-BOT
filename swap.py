import os #line:1
import json #line:2
import time #line:3
import logging #line:4
import functools #line:5
from typing import List ,Any ,Optional ,Callable ,Union ,Tuple ,Dict #line:6
from web3 import Web3 #line:8
from web3 .eth import Contract #line:9
from web3 .contract import ContractFunction #line:10
from web3 .types import (TxParams ,Wei ,Address ,ChecksumAddress ,ENS ,Nonce ,HexBytes ,)#line:19
from eth_utils import is_same_address #line:20
from eth_typing import AnyAddress #line:21
ETH_ADDRESS ="0x0000000000000000000000000000000000000000"#line:23
logger =logging .getLogger (__name__ )#line:25
AddressLike =Union [Address ,ChecksumAddress ,ENS ]#line:29
try :#line:31
    class InvalidToken (Exception ):#line:32
        def __init__ (O000O00000000OOOO ,O0O0OO00OO00000OO :Any )->None :#line:33
            Exception .__init__ (O000O00000000OOOO ,f"Invalid token address: {O0O0OO00OO00000OO}")#line:34
    class InsufficientBalance (Exception ):#line:37
        def __init__ (OO0O0O0O0000O00OO ,O00OO0OO0OO000OO0 :int ,OOOO0OO0O0OOO0O0O :int )->None :#line:38
            Exception .__init__ (OO0O0O0O0000O00OO ,f"Insufficient balance. Had {O00OO0OO0OO000OO0}, needed {OOOO0OO0O0OOO0O0O}")#line:39
    def _O0OOO00OO000O0OO0 (O000O00O00O0OOO00 :str )->str :#line:42
        O0OOOOOOO0O0O00O0 =f"{os.path.dirname(os.path.abspath(__file__))}/assets/"#line:43
        with open (os .path .abspath (O0OOOOOOO0O0O00O0 +f"{O000O00O00O0OOO00}.abi"))as O0O00O00OOO0O0O00 :#line:44
            OOOOO0O00OOOOO00O :str =json .load (O0O00O00OOO0O0O00 )#line:45
        return OOOOO0O00OOOOO00O #line:46
    def check_approval (OO000OOO0O0O0OOOO :Callable )->Callable :#line:49
        ""#line:51
        @functools .wraps (OO000OOO0O0O0OOOO )#line:53
        def OO0O0000OOO0O0000 (OOOO0O0OOOOOO0OO0 :Any ,*O00O000000O00O0OO :Any ,**O0O00000O00000000 :Any )->Any :#line:54
            O0O00000O00OO0000 =O00O000000O00O0OO [0 ]if O00O000000O00O0OO [0 ]!=ETH_ADDRESS else None #line:56
            O0O0O0O0O00O00OO0 =None #line:57
            if OO000OOO0O0O0OOOO .__name__ =="make_trade"or OO000OOO0O0O0OOOO .__name__ =="make_trade_output":#line:60
                O0O0O0O0O00O00OO0 =O00O000000O00O0OO [1 ]if O00O000000O00O0OO [1 ]!=ETH_ADDRESS else None #line:61
            if O0O00000O00OO0000 :#line:64
                O00O0000OOOO0O0O0 =OOOO0O0OOOOOO0OO0 ._is_approved (O0O00000O00OO0000 )#line:65
                if not O00O0000OOOO0O0O0 :#line:66
                    OOOO0O0OOOOOO0OO0 .approve (O0O00000O00OO0000 )#line:67
            if O0O0O0O0O00O00OO0 :#line:68
                O00O0000OOOO0O0O0 =OOOO0O0OOOOOO0OO0 ._is_approved (O0O0O0O0O00O00OO0 )#line:69
                if not O00O0000OOOO0O0O0 :#line:70
                    OOOO0O0OOOOOO0OO0 .approve (O0O0O0O0O00O00OO0 )#line:71
            return OO000OOO0O0O0OOOO (OOOO0O0OOOOOO0OO0 ,*O00O000000O00O0OO ,**O0O00000O00000000 )#line:72
        return OO0O0000OOO0O0000 #line:74
    def supports (OO00000OO00O000OO :List [int ])->Callable :#line:77
        def O0O00000OO00O0O0O (O0OOO0OO0O000OO0O :Callable )->Callable :#line:78
            @functools .wraps (O0OOO0OO0O000OO0O )#line:79
            def OOOOOOOOO00000OO0 (OO000OO00OO0O00OO :"Uniswap",*O0O00OO00O00OO000 :List ,**O0OO00O0O00OO0O0O :Dict )->Any :#line:80
                if OO000OO00OO0O00OO .version not in OO00000OO00O000OO :#line:81
                    raise Exception ("Function does not support version of Uniswap passed to constructor")#line:84
                return O0OOO0OO0O000OO0O (OO000OO00OO0O00OO ,*O0O00OO00O00OO000 ,**O0OO00O0O00OO0O0O )#line:85
            return OOOOOOOOO00000OO0 #line:87
        return O0O00000OO00O0O0O #line:89
    def _OOO000000OOO0OO00 (O000OO000OOO0O0O0 :str )->AddressLike :#line:92
        if O000OO000OOO0O0O0 .startswith ("0x"):#line:93
            return Address (bytes .fromhex (O000OO000OOO0O0O0 [2 :]))#line:94
        elif O000OO000OOO0O0O0 .endswith (".eth"):#line:95
            return ENS (O000OO000OOO0O0O0 )#line:96
        else :#line:97
            raise Exception ("Could't convert string {s} to AddressLike")#line:98
    def _O0OOO00OO0O0000O0 (OOO0O00O000OOOO0O :AddressLike )->str :#line:101
        if isinstance (OOO0O00O000OOOO0O ,bytes ):#line:102
            OO0O0O0OOOOOO000O :str =Web3 .toChecksumAddress ("0x"+bytes (OOO0O00O000OOOO0O ).hex ())#line:104
            return OO0O0O0OOOOOO000O #line:105
        elif isinstance (OOO0O00O000OOOO0O ,str ):#line:106
            if OOO0O00O000OOOO0O .endswith (".eth"):#line:107
                raise Exception ("ENS not supported for this operation")#line:109
            elif OOO0O00O000OOOO0O .startswith ("0x"):#line:110
                OO0O0O0OOOOOO000O =Web3 .toChecksumAddress (OOO0O00O000OOOO0O )#line:111
                return OO0O0O0OOOOOO000O #line:112
            else :#line:113
                raise InvalidToken (OOO0O00O000OOOO0O )#line:114
    def _OOO00OOOOO0OO0000 (O0000O0OO0OO00OO0 :AddressLike )->None :#line:117
        assert _O0OOO00OO0O0000O0 (O0000O0OO0OO00OO0 )#line:118
    _OO00OO0OOO0O0OO00 ={56 :"mainnet"}#line:121
    class Uniswap :#line:124
        def __init__ (O00OOOOOO00O0OO00 ,OOOOOOOOO0O0OOO0O :Union [str ,AddressLike ],O000OO0OOO0O00OOO :str ,O0OOOO00OO0OO0000 :str =None ,O0O00OO000OO00OO0 :Web3 =None ,OO000OOOOOOOOOOO0 :int =1 ,OO0O0OOOO00OO00O0 :float =0.1 ,)->None :#line:133
            O00OOOOOO00O0OO00 .address :AddressLike =_OOO000000OOO0OO00 (OOOOOOOOO0O0OOO0O )if isinstance (OOOOOOOOO0O0OOO0O ,str )else OOOOOOOOO0O0OOO0O #line:136
            O00OOOOOO00O0OO00 .private_key =O000OO0OOO0O00OOO #line:137
            O00OOOOOO00O0OO00 .version =OO000OOOOOOOOOOO0 #line:138
            O00OOOOOO00O0OO00 .max_slippage =OO0O0OOOO00OO00O0 #line:141
            if O0O00OO000OO00OO0 :#line:143
                O00OOOOOO00O0OO00 .w3 =O0O00OO000OO00OO0 #line:144
            else :#line:145
                O00OOOOOO00O0OO00 .provider =O0OOOO00OO0OO0000 or os .environ ["PROVIDER"]#line:147
                O00OOOOOO00O0OO00 .w3 =Web3 (Web3 .HTTPProvider (O00OOOOOO00O0OO00 .provider ,request_kwargs ={"timeout":60 }))#line:150
            O0OOO00000O0O00OO =int (O00OOOOOO00O0OO00 .w3 .net .version )#line:152
            if O0OOO00000O0O00OO in _OO00OO0OOO0O0OO00 :#line:153
                O00OOOOOO00O0OO00 .network =_OO00OO0OOO0O0OO00 [O0OOO00000O0O00OO ]#line:154
            else :#line:155
                raise Exception (f"Unknown netid: {O0OOO00000O0O00OO}")#line:156
            logger .info (f"Using {O00OOOOOO00O0OO00.w3} ('{O00OOOOOO00O0OO00.network}')")#line:157
            O00OOOOOO00O0OO00 .last_nonce :Nonce =O00OOOOOO00O0OO00 .w3 .eth .getTransactionCount (O00OOOOOO00O0OO00 .address )#line:159
            O00OOOOOO00O0OO00 .max_approval_hex =f"0x{64 * 'f'}"#line:166
            O00OOOOOO00O0OO00 .max_approval_int =int (O00OOOOOO00O0OO00 .max_approval_hex ,16 )#line:167
            O00OOOOOO00O0OO00 .max_approval_check_hex =f"0x{15 * '0'}{49 * 'f'}"#line:168
            O00OOOOOO00O0OO00 .max_approval_check_int =int (O00OOOOOO00O0OO00 .max_approval_check_hex ,16 )#line:169
            if O00OOOOOO00O0OO00 .version ==1 :#line:171
                O0OOOOOO00OOO00OO ={"mainnet":"0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95","ropsten":"0x9c83dCE8CA20E9aAF9D3efc003b2ea62aBC08351","rinkeby":"0xf5D915570BC477f9B8D6C0E980aA81757A3AaC36","kovan":"0xD3E51Ef092B2845f10401a0159B2B96e8B6c3D30","görli":"0x6Ce570d02D73d4c384b46135E87f8C592A8c86dA",}#line:178
                O00OOOOOO00O0OO00 .factory_contract =O00OOOOOO00O0OO00 ._load_contract (abi_name ="uniswap-v1/factory",address =_OOO000000OOO0OO00 (O0OOOOOO00OOO00OO [O00OOOOOO00O0OO00 .network ]),)#line:183
            elif O00OOOOOO00O0OO00 .version ==2 :#line:184
                OOOO000O0O00O00OO =_OOO000000OOO0OO00 ("0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73")#line:189
                O00OOOOOO00O0OO00 .factory_contract =O00OOOOOO00O0OO00 ._load_contract (abi_name ="uniswap-v2/factory",address =OOOO000O0O00O00OO ,)#line:192
                O00OOOOOO00O0OO00 .router_address :AddressLike =_OOO000000OOO0OO00 ("0x5609737142df7C1F873A6FA985D03bc61761D35c")#line:195
                """Documented here: https://uniswap.org/docs/v2/smart-contracts/router02/"""#line:196
                O00OOOOOO00O0OO00 .router =O00OOOOOO00O0OO00 ._load_contract (abi_name ="uniswap-v2/router02",address =O00OOOOOO00O0OO00 .router_address ,)#line:199
            else :#line:200
                raise Exception ("Invalid version, only 1 or 2 supported")#line:201
            logger .info (f"Using factory contract: {O00OOOOOO00O0OO00.factory_contract}")#line:203
        @supports ([1 ])#line:205
        def get_all_tokens (OOOO0OO0OO0O00O0O )->List [dict ]:#line:206
            OO0O0O000O00000OO =OOOO0OO0OO0O00O0O .factory_contract .functions .tokenCount ().call ()#line:208
            OOO000OO00O00O00O =[]#line:209
            for OOOOOOOO0O00O0OOO in range (OO0O0O000O00000OO ):#line:210
                O0OO000000O00OO0O =OOOO0OO0OO0O00O0O .factory_contract .functions .getTokenWithId (OOOOOOOO0O00O0OOO ).call ()#line:211
                if O0OO000000O00OO0O =="0x0000000000000000000000000000000000000000":#line:212
                    continue #line:214
                O0OOO0O000OO0OOOO =OOOO0OO0OO0O00O0O .get_token (O0OO000000O00OO0O )#line:215
                OOO000OO00O00O00O .append (O0OOO0O000OO0OOOO )#line:216
            return OOO000OO00O00O00O #line:217
        @supports ([1 ])#line:219
        def get_token (OOO0O000000000000 ,O000O0OO0OO00OOOO :AddressLike )->dict :#line:220
            OO000O0OO000000O0 =OOO0O000000000000 ._load_contract (abi_name ="erc20",address =O000O0OO0OO00OOOO )#line:223
            try :#line:224
                OOO00OOO000OO000O =OO000O0OO000000O0 .functions .symbol ().call ()#line:225
                OO00O0OO0000OOOOO =OO000O0OO000000O0 .functions .name ().call ()#line:226
            except Exception as OOOO0OOOOOOOO00O0 :#line:227
                logger .warning (f"Exception occurred while trying to get token {_O0OOO00OO0O0000O0(O000O0OO0OO00OOOO)}: {OOOO0OOOOOOOO00O0}")#line:230
                raise InvalidToken (O000O0OO0OO00OOOO )#line:231
            return {"name":OO00O0OO0000OOOOO ,"symbol":OOO00OOO000OO000O }#line:232
        @supports ([1 ])#line:234
        def exchange_address_from_token (O0OO000OOOO00O00O ,OOOO0000O0O0O00OO :AddressLike )->AddressLike :#line:235
            O0OOO00OOOO0OOOO0 :AddressLike =O0OO000OOOO00O00O .factory_contract .functions .getExchange (OOOO0000O0O0O00OO ).call ()#line:238
            return O0OOO00OOOO0OOOO0 #line:240
        @supports ([1 ])#line:242
        def token_address_from_exchange (O000O000OO00OOOO0 ,OO0OOO000O0OOO0O0 :AddressLike )->Address :#line:243
            OOOO000OO0OO0O000 :Address =(O000O000OO00OOOO0 .exchange_contract (ex_addr =OO0OOO000O0OOO0O0 ).functions .tokenAddress (OO0OOO000O0OOO0O0 ).call ())#line:248
            return OOOO000OO0OO0O000 #line:249
        @functools .lru_cache ()#line:251
        @supports ([1 ])#line:252
        def exchange_contract (OOO0O00O00OO00OOO ,O0O0000O0OO00O000 :AddressLike =None ,OO00O0O0OO00OO00O :AddressLike =None )->Contract :#line:255
            if not OO00O0O0OO00OO00O and O0O0000O0OO00O000 :#line:256
                OO00O0O0OO00OO00O =OOO0O00O00OO00OOO .exchange_address_from_token (O0O0000O0OO00O000 )#line:257
            if OO00O0O0OO00OO00O is None :#line:258
                raise InvalidToken (O0O0000O0OO00O000 )#line:259
            OO0O000O0OO00OOO0 ="uniswap-v1/exchange"#line:260
            O000O0O0OO000OOO0 =OOO0O00O00OO00OOO ._load_contract (abi_name =OO0O000O0OO00OOO0 ,address =OO00O0O0OO00OO00O )#line:261
            logger .info (f"Loaded exchange contract {O000O0O0OO000OOO0} at {O000O0O0OO000OOO0.address}")#line:262
            return O000O0O0OO000OOO0 #line:263
        @functools .lru_cache ()#line:265
        def erc20_contract (OO0OOO0OO0OO0OO00 ,O00OO00OOOOO0OO00 :AddressLike )->Contract :#line:266
            return OO0OOO0OO0OO0OO00 ._load_contract (abi_name ="erc20",address =O00OO00OOOOO0OO00 )#line:267
        @functools .lru_cache ()#line:269
        @supports ([2 ])#line:270
        def get_weth_address (O0OOO0OO0000OOO0O )->ChecksumAddress :#line:271
            O0O0O0OOO00OOO000 =Web3 .toChecksumAddress ('0x5609737142df7C1F873A6FA985D03bc61761D35c')#line:273
            return O0O0O0OOO00OOO000 #line:274
        def _load_contract (OO00OOO0OOO00OOOO ,OOO00O0000OO00OO0 :str ,O0OOOOO0000OO000O :AddressLike )->Contract :#line:276
            return OO00OOO0OOO00OOOO .w3 .eth .contract (address =O0OOOOO0000OO000O ,abi =_O0OOO00OO000O0OO0 (OOO00O0000OO00OO0 ))#line:277
        @supports ([1 ,2 ])#line:280
        def get_fee_maker (OO000OO00O0OO0000 )->float :#line:281
            ""#line:282
            return 0 #line:283
        @supports ([1 ,2 ])#line:285
        def get_fee_taker (O000OOO000OO00O00 )->float :#line:286
            ""#line:287
            return 0.003 #line:288
        @supports ([1 ,2 ])#line:291
        def get_eth_token_input_price (O0O0O00OO0OOO0OO0 ,O0OO0OOOOOO0OO0O0 :AddressLike ,O00O0OO000O0O0OOO :Wei )->Wei :#line:292
            ""#line:293
            if O0O0O00OO0OOO0OO0 .version ==1 :#line:294
                OOOOO00OOOOOO00OO =O0O0O00OO0OOO0OO0 .exchange_contract (O0OO0OOOOOO0OO0O0 )#line:295
                O000O000OO0OOO00O :Wei =OOOOO00OOOOOO00OO .functions .getEthToTokenInputPrice (O00O0OO000O0O0OOO ).call ()#line:296
            elif O0O0O00OO0OOO0OO0 .version ==2 :#line:297
                O000O000OO0OOO00O =O0O0O00OO0OOO0OO0 .router .functions .getAmountsOut (O00O0OO000O0O0OOO ,[O0O0O00OO0OOO0OO0 .get_weth_address (),O0OO0OOOOOO0OO0O0 ]).call ()[-1 ]#line:300
            return O000O000OO0OOO00O #line:301
        @supports ([1 ,2 ])#line:303
        def get_token_eth_input_price (O00O000O0O000O000 ,O00OO0O0O000O000O :AddressLike ,O0O0O0OO0O0000000 :int )->int :#line:304
            ""#line:305
            if O00O000O0O000O000 .version ==1 :#line:306
                O000O0O00O0OO0O0O =O00O000O0O000O000 .exchange_contract (O00OO0O0O000O000O )#line:307
                OOO000O0OOO00O00O :int =O000O0O00O0OO0O0O .functions .getTokenToEthInputPrice (O0O0O0OO0O0000000 ).call ()#line:308
            else :#line:309
                OOO000O0OOO00O00O =O00O000O0O000O000 .router .functions .getAmountsOut (O0O0O0OO0O0000000 ,[O00OO0O0O000O000O ,O00O000O0O000O000 .get_weth_address ()]).call ()[-1 ]#line:312
            return OOO000O0OOO00O00O #line:313
        @supports ([2 ])#line:315
        def get_token_token_input_price (OO000OOO00O000OOO ,OO0O0O0OOO00000O0 :AnyAddress ,OO00O0OOOOOO0O0OO :AnyAddress ,O0OO000OOO0OO00OO :int )->int :#line:318
            ""#line:319
            if is_same_address (OO0O0O0OOO00000O0 ,OO000OOO00O000OOO .get_weth_address ()):#line:322
                return int (OO000OOO00O000OOO .get_eth_token_input_price (OO00O0OOOOOO0O0OO ,O0OO000OOO0OO00OO ))#line:323
            elif is_same_address (OO00O0OOOOOO0O0OO ,OO000OOO00O000OOO .get_weth_address ()):#line:324
                return int (OO000OOO00O000OOO .get_token_eth_input_price (OO0O0O0OOO00000O0 ,O0OO000OOO0OO00OO ))#line:325
            OO00OO000O0OO0000 :int =OO000OOO00O000OOO .router .functions .getAmountsOut (O0OO000OOO0OO00OO ,[OO0O0O0OOO00000O0 ,OO000OOO00O000OOO .get_weth_address (),OO00O0OOOOOO0O0OO ]).call ()[-1 ]#line:329
            return OO00OO000O0OO0000 #line:330
        @supports ([1 ,2 ])#line:332
        def get_eth_token_output_price (O00O00OO0O00OO00O ,OO0O00OOO000O0OO0 :AddressLike ,OOOO0000000O0OO0O :int )->Wei :#line:333
            ""#line:334
            if O00O00OO0O00OO00O .version ==1 :#line:335
                OO0OOOO0O0O0OO0OO =O00O00OO0O00OO00O .exchange_contract (OO0O00OOO000O0OO0 )#line:336
                OOO000OOOOOOO000O :Wei =OO0OOOO0O0O0OO0OO .functions .getEthToTokenOutputPrice (OOOO0000000O0OO0O ).call ()#line:337
            else :#line:338
                OOO000OOOOOOO000O =O00O00OO0O00OO00O .router .functions .getAmountsIn (OOOO0000000O0OO0O ,[O00O00OO0O00OO00O .get_weth_address (),OO0O00OOO000O0OO0 ]).call ()[0 ]#line:341
            return OOO000OOOOOOO000O #line:342
        @supports ([1 ,2 ])#line:344
        def get_token_eth_output_price (O0000OOO0O0O00O0O ,OO00O000O000OOOOO :AddressLike ,OO00OOOO00OOO0000 :Wei )->int :#line:345
            ""#line:346
            if O0000OOO0O0O00O0O .version ==1 :#line:347
                OO0OOOOO0OO0OO0O0 =O0000OOO0O0O00O0O .exchange_contract (OO00O000O000OOOOO )#line:348
                OO00OO0OOOOO0O0O0 :int =OO0OOOOO0OO0OO0O0 .functions .getTokenToEthOutputPrice (OO00OOOO00OOO0000 ).call ()#line:349
            else :#line:350
                OO00OO0OOOOO0O0O0 =O0000OOO0O0O00O0O .router .functions .getAmountsIn (OO00OOOO00OOO0000 ,[OO00O000O000OOOOO ,O0000OOO0O0O00O0O .get_weth_address ()]).call ()[0 ]#line:353
            return OO00OO0OOOOO0O0O0 #line:354
        @supports ([2 ])#line:356
        def get_token_token_output_price (O00000O00OO0O000O ,O0000O0OO0O0OO00O :AnyAddress ,OOOO0O0OO0O000O00 :AnyAddress ,OOOO00OOOO000OOOO :int )->int :#line:359
            ""#line:360
            if is_same_address (O0000O0OO0O0OO00O ,O00000O00OO0O000O .get_weth_address ()):#line:364
                return int (O00000O00OO0O000O .get_eth_token_output_price (OOOO0O0OO0O000O00 ,OOOO00OOOO000OOOO ))#line:365
            elif is_same_address (OOOO0O0OO0O000O00 ,O00000O00OO0O000O .get_weth_address ()):#line:366
                return int (O00000O00OO0O000O .get_token_eth_output_price (O0000O0OO0O0OO00O ,OOOO00OOOO000OOOO ))#line:367
            O000OO0OO00OOO00O :int =O00000O00OO0O000O .router .functions .getAmountsIn (OOOO00OOOO000OOOO ,[O0000O0OO0O0OO00O ,O00000O00OO0O000O .get_weth_address (),OOOO0O0OO0O000O00 ]).call ()[0 ]#line:371
            return O000OO0OO00OOO00O #line:372
        def get_eth_balance (O0OOOOOO000O0OO0O )->Wei :#line:375
            ""#line:376
            return O0OOOOOO000O0OO0O .w3 .eth .getBalance (O0OOOOOO000O0OO0O .address )#line:377
        def get_token_balance (O0OO000OO00OOOOOO ,O000OO000000OOOOO :AddressLike )->int :#line:379
            ""#line:380
            _OOO00OOOOO0OO0000 (O000OO000000OOOOO )#line:381
            if _O0OOO00OO0O0000O0 (O000OO000000OOOOO )==ETH_ADDRESS :#line:382
                return O0OO000OO00OOOOOO .get_eth_balance ()#line:383
            O0OOOO0O000OOOOO0 =O0OO000OO00OOOOOO .erc20_contract (O000OO000000OOOOO )#line:384
            OOO0O00OOO0OOOO0O :int =O0OOOO0O000OOOOO0 .functions .balanceOf (O0OO000OO00OOOOOO .address ).call ()#line:385
            return OOO0O00OOO0OOOO0O #line:386
        @supports ([1 ])#line:389
        def get_ex_eth_balance (OOOO000OOO0OO0O0O ,O0OOO0OOOO0O0O0O0 :AddressLike )->int :#line:390
            ""#line:391
            OOOO0000OOOOO0OOO :AddressLike =OOOO000OOO0OO0O0O .exchange_address_from_token (O0OOO0OOOO0O0O0O0 )#line:392
            return OOOO000OOO0OO0O0O .w3 .eth .getBalance (OOOO0000OOOOO0OOO )#line:393
        @supports ([1 ])#line:395
        def get_ex_token_balance (OO00000000O0O00OO ,O00O0OO000OOOO000 :AddressLike )->int :#line:396
            ""#line:397
            OOO0O0OOO0O0OO000 =OO00000000O0O00OO .erc20_contract (O00O0OO000OOOO000 )#line:398
            OOOOOOO0O00000OOO :int =OOO0O0OOO0O0OO000 .functions .balanceOf (OO00000000O0O00OO .exchange_address_from_token (O00O0OO000OOOO000 )).call ()#line:401
            return OOOOOOO0O00000OOO #line:402
        @supports ([1 ])#line:405
        def get_exchange_rate (OO0OOOO0O0OOOO0OO ,O0OOO000OOO00O000 :AddressLike )->float :#line:406
            ""#line:407
            OO00000O000O0O0O0 =OO0OOOO0O0OOOO0OO .get_ex_eth_balance (O0OOO000OOO00O000 )#line:408
            O00OOO00OO00OOOOO =OO0OOOO0O0OOOO0OO .get_ex_token_balance (O0OOO000OOO00O000 )#line:409
            return float (O00OOO00OO00OOOOO /OO00000O000O0O0O0 )#line:410
        @supports ([1 ])#line:413
        @check_approval #line:414
        def add_liquidity (OOO0OOO0OO00O0OOO ,OOOOO0O00OO00O00O ,O00OOO000OOOO0OO0 ,O00000O0000O00OO0 ,OOOOOOOO000O0OO00 :AddressLike ,O0000OOOOO0OO0OO0 :Wei ,OOO0O000OO0OO00O0 :int =1 )->HexBytes :#line:417
            ""#line:418
            OOOOO00O0OOO00OO0 =OOO0OOO0OO00O0OOO ._get_tx_params (value =O0000OOOOO0OO0OO0 ,gwei =OOOOO0O00OO00O00O )#line:419
            O0OOOO0OO000O000O =int (O0000OOOOO0OO0OO0 *OOO0OOO0OO00O0OOO .get_exchange_rate (OOOOOOOO000O0OO00 ))+10 #line:422
            O00O00OOOO0OOO0O0 =[OOO0O000OO0OO00O0 ,O0OOOO0OO000O000O ,OOO0OOO0OO00O0OOO ._deadline ()]#line:423
            O00O0OO0OO0O0O00O =OOO0OOO0OO00O0OOO .exchange_contract (OOOOOOOO000O0OO00 ).functions .addLiquidity (*O00O00OOOO0OOO0O0 )#line:424
            return OOO0OOO0OO00O0OOO ._build_and_send_tx (OOOOO0O00OO00O00O ,O00OOO000OOOO0OO0 ,O00000O0000O00OO0 ,O00O0OO0OO0O0O00O ,OOOOO00O0OOO00OO0 )#line:425
        @supports ([1 ])#line:427
        @check_approval #line:428
        def remove_liquidity (OO0O0OOOOOO0OOOOO ,OO0O00OO0OOO00OOO ,OOO0OO00O0O00000O :str ,OO000OOOOOO0OO0O0 :int )->HexBytes :#line:429
            ""#line:430
            O0O000O0O00OO00OO =[int (OO000OOOOOO0OO0O0 ),1 ,1 ,OO0O0OOOOOO0OOOOO ._deadline ()]#line:431
            O00OO0000000OOO00 =OO0O0OOOOOO0OOOOO .exchange_contract (OOO0OO00O0O00000O ).functions .removeLiquidity (*O0O000O0O00OO00OO )#line:432
            return OO0O0OOOOOO0OOOOO ._build_and_send_tx (OO0O00OO0OOO00OOO ,my_address ,my_pk ,my_address ,my_pk ,O00OO0000000OOO00 )#line:433
        @check_approval #line:436
        def make_trade (O00OOO0OO000OO0O0 ,OOOO0O00OO0OOOOOO :AddressLike ,OO00000O000O0O00O :AddressLike ,O0O00O0000OOO000O :Union [int ,Wei ],OO000OO00O0000O0O ,O0O0O00O00OOOOO00 ,O0O000OO0O0OO00OO ,O0O000O00OOOOOO00 :AddressLike =None ,)->HexBytes :#line:446
            ""#line:447
            if OOOO0O00OO0OOOOOO ==ETH_ADDRESS :#line:448
                return O00OOO0OO000OO0O0 ._eth_to_token_swap_input (OO000OO00O0000O0O ,O0O0O00O00OOOOO00 ,O0O000OO0O0OO00OO ,OO00000O000O0O00O ,Wei (O0O00O0000OOO000O ),O0O000O00OOOOOO00 )#line:449
            else :#line:450
                OO0000O00O0OOO000 =O00OOO0OO000OO0O0 .get_token_balance (OOOO0O00OO0OOOOOO )#line:451
                if OO0000O00O0OOO000 <O0O00O0000OOO000O :#line:452
                    raise InsufficientBalance (OO0000O00O0OOO000 ,O0O00O0000OOO000O )#line:453
                if OO00000O000O0O00O ==ETH_ADDRESS :#line:454
                    return O00OOO0OO000OO0O0 ._token_to_eth_swap_input (OO000OO00O0000O0O ,O0O0O00O00OOOOO00 ,O0O000OO0O0OO00OO ,OOOO0O00OO0OOOOOO ,O0O00O0000OOO000O ,O0O000O00OOOOOO00 )#line:455
                else :#line:456
                    return O00OOO0OO000OO0O0 ._token_to_token_swap_input (OO000OO00O0000O0O ,O0O0O00O00OOOOO00 ,O0O000OO0O0OO00OO ,OOOO0O00OO0OOOOOO ,O0O00O0000OOO000O ,OO00000O000O0O00O ,O0O000O00OOOOOO00 )#line:459
        @check_approval #line:461
        def make_trade_output (O0O0OO0OOO00OOO00 ,O000OO0O00OOOO0O0 :AddressLike ,OO0OO00O0OO000OO0 :AddressLike ,OO0OO0O00OO000OOO :Union [int ,Wei ],O0O00OO0O00000OO0 :AddressLike =None ,)->HexBytes :#line:468
            ""#line:469
            if O000OO0O00OOOO0O0 ==ETH_ADDRESS :#line:470
                OO0O000OO000O00OO =O0O0OO0OOO00OOO00 .get_eth_balance ()#line:471
                O0000O0O0OOO000OO =O0O0OO0OOO00OOO00 .get_eth_token_output_price (OO0OO00O0OO000OO0 ,OO0OO0O00OO000OOO )#line:472
                if OO0O000OO000O00OO <O0000O0O0OOO000OO :#line:473
                    raise InsufficientBalance (OO0O000OO000O00OO ,O0000O0O0OOO000OO )#line:474
                return O0O0OO0OOO00OOO00 ._eth_to_token_swap_output (OO0OO00O0OO000OO0 ,OO0OO0O00OO000OOO ,O0O00OO0O00000OO0 )#line:475
            else :#line:476
                if OO0OO00O0OO000OO0 ==ETH_ADDRESS :#line:477
                    OO0OO0O00OO000OOO =Wei (OO0OO0O00OO000OOO )#line:478
                    return O0O0OO0OOO00OOO00 ._token_to_eth_swap_output (O000OO0O00OOOO0O0 ,OO0OO0O00OO000OOO ,O0O00OO0O00000OO0 )#line:479
                else :#line:480
                    return O0O0OO0OOO00OOO00 ._token_to_token_swap_output (O000OO0O00OOOO0O0 ,OO0OO0O00OO000OOO ,OO0OO00O0OO000OO0 ,O0O00OO0O00000OO0 )#line:483
        def _eth_to_token_swap_input (O0OO0O0O0000OOOO0 ,O00O0OO000OOOO0O0 ,OOO0OO00OO000OO00 ,OOOO0OOOOOOOO0O0O ,O0OOOOOOOO0000OO0 :AddressLike ,OOO00000000O00OO0 :Wei ,O00OOO000O000O000 :Optional [AddressLike ])->HexBytes :#line:489
            ""#line:490
            OO0O00OOO000O000O =O0OO0O0O0000OOOO0 .get_eth_balance ()#line:491
            if OOO00000000O00OO0 >OO0O00OOO000O000O :#line:492
                raise InsufficientBalance (OO0O00OOO000O000O ,OOO00000000O00OO0 )#line:493
            if O0OO0O0O0000OOOO0 .version ==1 :#line:495
                O00O0O00000O0O00O =O0OO0O0O0000OOOO0 .exchange_contract (O0OOOOOOOO0000OO0 ).functions #line:496
                O0OOOO0O000O000OO =O0OO0O0O0000OOOO0 ._get_tx_params (value =OOO00000000O00OO0 ,gwei =O00O0OO000OOOO0O0 )#line:497
                OOOOOOOO00OOO00O0 :List [Any ]=[OOO00000000O00OO0 ,O0OO0O0O0000OOOO0 ._deadline ()]#line:498
                if not O00OOO000O000O000 :#line:499
                    OOOO0OOO0O0O000OO =O00O0O00000O0O00O .ethToTokenSwapInput (*OOOOOOOO00OOO00O0 )#line:500
                else :#line:501
                    OOOOOOOO00OOO00O0 .append (O00OOO000O000O000 )#line:502
                    OOOO0OOO0O0O000OO =O00O0O00000O0O00O .ethToTokenTransferInput (*OOOOOOOO00OOO00O0 )#line:503
                return O0OO0O0O0000OOOO0 ._build_and_send_tx (O00O0OO000OOOO0O0 ,OOO0OO00OO000OO00 ,OOOO0OOOOOOOO0O0O ,OOOO0OOO0O0O000OO ,O0OOOO0O000O000OO )#line:504
            else :#line:505
                if O00OOO000O000O000 is None :#line:506
                    O00OOO000O000O000 =O0OO0O0O0000OOOO0 .address #line:507
                OOOOO0OOO00OO0OO0 =int ((1 -O0OO0O0O0000OOOO0 .max_slippage )*O0OO0O0O0000OOOO0 .get_eth_token_input_price (O0OOOOOOOO0000OO0 ,OOO00000000O00OO0 ))#line:511
                return O0OO0O0O0000OOOO0 ._build_and_send_tx (O00O0OO000OOOO0O0 ,OOO0OO00OO000OO00 ,OOOO0OOOOOOOO0O0O ,O0OO0O0O0000OOOO0 .router .functions .swapExactETHForTokens (OOOOO0OOO00OO0OO0 ,[O0OO0O0O0000OOOO0 .get_weth_address (),O0OOOOOOOO0000OO0 ],O00OOO000O000O000 ,O0OO0O0O0000OOOO0 ._deadline (),),O0OO0O0O0000OOOO0 ._get_tx_params (value =OOO00000000O00OO0 ,gwei =O00O0OO000OOOO0O0 ,my_address =OOO0OO00OO000OO00 ),)#line:520
        def _token_to_eth_swap_input (O000OOO0O00O0OO00 ,O0OOO00O00O0OO0OO ,OOO0O000O0O0O0OOO ,O0OO00O0O0OO0O000 ,O0OOOO0O0O000O000 :AddressLike ,O00000O0O0O0OO0OO :int ,OO0OOOOOO00OOO0OO :Optional [AddressLike ])->HexBytes :#line:524
            ""#line:525
            O00OO00O0O0OOO00O =O000OOO0O00O0OO00 .get_token_balance (O0OOOO0O0O000O000 )#line:527
            if O00000O0O0O0OO0OO >O00OO00O0O0OOO00O :#line:528
                raise InsufficientBalance (O00OO00O0O0OOO00O ,O00000O0O0O0OO0OO )#line:529
            if O000OOO0O00O0OO00 .version ==1 :#line:531
                O0O0000O00OO0O0O0 =O000OOO0O00O0OO00 .exchange_contract (O0OOOO0O0O000O000 ).functions #line:532
                O0OO0000OO000000O :List [Any ]=[O00000O0O0O0OO0OO ,1 ,O000OOO0O00O0OO00 ._deadline ()]#line:533
                if not OO0OOOOOO00OOO0OO :#line:534
                    OO0OOO0OO0000OOO0 =O0O0000O00OO0O0O0 .tokenToEthSwapInput (*O0OO0000OO000000O )#line:535
                else :#line:536
                    O0OO0000OO000000O .append (OO0OOOOOO00OOO0OO )#line:537
                    OO0OOO0OO0000OOO0 =O0O0000O00OO0O0O0 .tokenToEthTransferInput (*O0OO0000OO000000O )#line:538
                return O000OOO0O00O0OO00 ._build_and_send_tx (O0OOO00O00O0OO0OO ,OOO0O000O0O0O0OOO ,O0OO00O0O0OO0O000 ,OO0OOO0OO0000OOO0 )#line:539
            else :#line:540
                if OO0OOOOOO00OOO0OO is None :#line:541
                    OO0OOOOOO00OOO0OO =O000OOO0O00O0OO00 .address #line:542
                O0O00000O0O0OO0OO =int ((1 -O000OOO0O00O0OO00 .max_slippage )*O000OOO0O00O0OO00 .get_token_eth_input_price (O0OOOO0O0O000O000 ,O00000O0O0O0OO0OO ))#line:546
                return O000OOO0O00O0OO00 ._build_and_send_tx (O0OOO00O00O0OO0OO ,OOO0O000O0O0O0OOO ,O0OO00O0O0OO0O000 ,O000OOO0O00O0OO00 .router .functions .swapExactTokensForETH (O00000O0O0O0OO0OO ,O0O00000O0O0OO0OO ,[O0OOOO0O0O000O000 ,O000OOO0O00O0OO00 .get_weth_address ()],OO0OOOOOO00OOO0OO ,O000OOO0O00O0OO00 ._deadline (),),)#line:555
        def _token_to_token_swap_input (OO00OO0O0OO0O00O0 ,OO00OO00OOO00O00O ,O0000O00OOOOOOOO0 ,O00OOO0OOOOO0000O ,OO00OOOO0000OOOO0 :AddressLike ,OOO0O0OOOOO000OO0 :int ,OOO00OOO0O0O000O0 :AddressLike ,OO00O0OO0OO00OOO0 :Optional [AddressLike ],)->HexBytes :#line:563
            ""#line:564
            if OO00OO0O0OO0O00O0 .version ==1 :#line:565
                OO0OO00OOOO000OO0 =OO00OO0O0OO0O00O0 .exchange_contract (OO00OOOO0000OOOO0 ).functions #line:566
                OO0O0OOOOO0OO0O0O ,O0000OO00O0OOOOOO =OO00OO0O0OO0O00O0 ._calculate_max_input_token (OO00OOOO0000OOOO0 ,OOO0O0OOOOO000OO0 ,OOO00OOO0O0O000O0 )#line:570
                OOOO00000OO00OO0O =[OOO0O0OOOOO000OO0 ,OO0O0OOOOO0OO0O0O ,O0000OO00O0OOOOOO ,OO00OO0O0OO0O00O0 ._deadline (),OOO00OOO0O0O000O0 ,]#line:577
                if not OO00O0OO0OO00OOO0 :#line:578
                    OO0O0O00OO0OO0OOO =OO0OO00OOOO000OO0 .tokenToTokenSwapInput (*OOOO00000OO00OO0O )#line:579
                else :#line:580
                    OOOO00000OO00OO0O .insert (len (OOOO00000OO00OO0O )-1 ,OO00O0OO0OO00OOO0 )#line:581
                    OO0O0O00OO0OO0OOO =OO0OO00OOOO000OO0 .tokenToTokenTransferInput (*OOOO00000OO00OO0O )#line:582
                return OO00OO0O0OO0O00O0 ._build_and_send_tx (OO00OO00OOO00O00O ,O0000O00OOOOOOOO0 ,O00OOO0OOOOO0000O ,OO0O0O00OO0OO0OOO )#line:583
            else :#line:584
                if OO00O0OO0OO00OOO0 is None :#line:585
                    OO00O0OO0OO00OOO0 =OO00OO0O0OO0O00O0 .address #line:586
                OO0O0OOOOO0OO0O0O =int ((1 -OO00OO0O0OO0O00O0 .max_slippage )*OO00OO0O0OO0O00O0 .get_token_token_input_price (OO00OOOO0000OOOO0 ,OOO00OOO0O0O000O0 ,OOO0O0OOOOO000OO0 ))#line:590
                return OO00OO0O0OO0O00O0 ._build_and_send_tx (OO00OO00OOO00O00O ,O0000O00OOOOOOOO0 ,O00OOO0OOOOO0000O ,OO00OO0O0OO0O00O0 .router .functions .swapExactTokensForTokens (OOO0O0OOOOO000OO0 ,OO0O0OOOOO0OO0O0O ,[OO00OOOO0000OOOO0 ,OO00OO0O0OO0O00O0 .get_weth_address (),OOO00OOO0O0O000O0 ],OO00O0OO0OO00OOO0 ,OO00OO0O0OO0O00O0 ._deadline (),),)#line:599
        def _eth_to_token_swap_output (O00O00O0O0000OOO0 ,OOOOO000O00000O0O ,O000OOOOOO00OO0OO ,OOO00O0000000OO0O ,OOOOOOO00OOOO0000 :AddressLike ,OOO00OOO0000OO0OO :int ,OOO0O0O00000OOOO0 :Optional [AddressLike ])->HexBytes :#line:603
            ""#line:604
            print ("ethto"+OOOOO000O00000O0O )#line:605
            if O00O00O0O0000OOO0 .version ==1 :#line:606
                OOOOO0O000OOO000O =O00O00O0O0000OOO0 .exchange_contract (OOOOOOO00OOOO0000 ).functions #line:607
                O0O0O000OOO000OO0 =O00O00O0O0000OOO0 .get_eth_token_output_price (OOOOOOO00OOOO0000 ,OOO00OOO0000OO0OO )#line:608
                OO0OO0O0O0O00000O =O00O00O0O0000OOO0 ._get_tx_params (value =O0O0O000OOO000OO0 ,gwei =OOOOO000O00000O0O )#line:609
                O00O00O00O0000OOO :List [Any ]=[OOO00OOO0000OO0OO ,O00O00O0O0000OOO0 ._deadline ()]#line:610
                if not OOO0O0O00000OOOO0 :#line:611
                    O000000O0000OOO0O =OOOOO0O000OOO000O .ethToTokenSwapOutput (*O00O00O00O0000OOO )#line:612
                else :#line:613
                    O00O00O00O0000OOO .append (OOO0O0O00000OOOO0 )#line:614
                    O000000O0000OOO0O =OOOOO0O000OOO000O .ethToTokenTransferOutput (*O00O00O00O0000OOO )#line:615
                return O00O00O0O0000OOO0 ._build_and_send_tx (OOOOO000O00000O0O ,O000OOOOOO00OO0OO ,OOO00O0000000OO0O ,O000000O0000OOO0O ,OO0OO0O0O0O00000O )#line:616
            else :#line:617
                if OOO0O0O00000OOOO0 is None :#line:618
                    OOO0O0O00000OOOO0 =O00O00O0O0000OOO0 .address #line:619
                O0O0O000OOO000OO0 =O00O00O0O0000OOO0 .get_eth_token_output_price (OOOOOOO00OOOO0000 ,OOO00OOO0000OO0OO )#line:620
                return O00O00O0O0000OOO0 ._build_and_send_tx (OOOOO000O00000O0O ,O000OOOOOO00OO0OO ,OOO00O0000000OO0O ,O00O00O0O0000OOO0 .router .functions .swapETHForExactTokens (OOO00OOO0000OO0OO ,[O00O00O0O0000OOO0 .get_weth_address (),OOOOOOO00OOOO0000 ],OOO0O0O00000OOOO0 ,O00O00O0O0000OOO0 ._deadline (),),O00O00O0O0000OOO0 ._get_tx_params (value =O0O0O000OOO000OO0 ,gwei =OOOOO000O00000O0O ),)#line:629
        def _token_to_eth_swap_output (O0000O0OO000O0000 ,O0O000OO0O0OOOOO0 ,OOO000OOOO0OO0000 ,O0OO00O0OOO000000 ,O0000OO0O000OOO0O :AddressLike ,OO00O0O00OO0O0O0O :Wei ,OOO0O0OO0O0O00OO0 :Optional [AddressLike ])->HexBytes :#line:633
            ""#line:634
            O0O00OO00O0OO0OO0 =O0000O0OO000O0000 .get_token_balance (O0000OO0O000OOO0O )#line:636
            O000O00O000OOOO00 =O0000O0OO000O0000 .get_token_eth_output_price (O0000OO0O000OOO0O ,OO00O0O00OO0O0O0O )#line:637
            if O000O00O000OOOO00 >O0O00OO00O0OO0OO0 :#line:638
                raise InsufficientBalance (O0O00OO00O0OO0OO0 ,O000O00O000OOOO00 )#line:639
            if O0000O0OO000O0000 .version ==1 :#line:641
                OO00OOO00O000O0OO =O0000O0OO000O0000 .exchange_contract (O0000OO0O000OOO0O ).functions #line:642
                O0OOO0OOOO00OO0O0 =OO00O0O00OO0O0O0O #line:646
                O0OO0OO000O0O00OO =O0000O0OO000O0000 .get_ex_token_balance (O0000OO0O000OOO0O )#line:647
                OO000O00O0OOO0O0O =O0000O0OO000O0000 .get_ex_eth_balance (O0000OO0O000OOO0O )#line:648
                O0OOOOOO0OO0O0O00 =O0OOO0OOOO00OO0O0 *O0OO0OO000O0O00OO *1000 #line:650
                O00OOO0O0O0OO0OOO =(OO000O00O0OOO0O0O -O0OOO0OOOO00OO0O0 )*997 #line:651
                O0O000O0O0OOOO00O =O0OOOOOO0OO0O0O00 /O00OOO0O0O0OO0OOO +1 #line:652
                O0OO000OO00OOO0O0 =int ((1 +O0000O0OO000O0000 .max_slippage )*O0O000O0O0OOOO00O )#line:654
                O0O000OO0OOO0OOO0 :List [Any ]=[OO00O0O00OO0O0O0O ,O0OO000OO00OOO0O0 ,O0000O0OO000O0000 ._deadline ()]#line:656
                if not OOO0O0OO0O0O00OO0 :#line:657
                    OOOOO00O00OOOO000 =OO00OOO00O000O0OO .tokenToEthSwapOutput (*O0O000OO0OOO0OOO0 )#line:658
                else :#line:659
                    O0O000OO0OOO0OOO0 .append (OOO0O0OO0O0O00OO0 )#line:660
                    OOOOO00O00OOOO000 =OO00OOO00O000O0OO .tokenToEthTransferOutput (*O0O000OO0OOO0OOO0 )#line:661
                return O0000O0OO000O0000 ._build_and_send_tx (O0O000OO0O0OOOOO0 ,OOO000OOOO0OO0000 ,O0OO00O0OOO000000 ,OOOOO00O00OOOO000 )#line:662
            else :#line:663
                O0OO000OO00OOO0O0 =int ((1 +O0000O0OO000O0000 .max_slippage )*O000O00O000OOOO00 )#line:664
                return O0000O0OO000O0000 ._build_and_send_tx (O0O000OO0O0OOOOO0 ,OOO000OOOO0OO0000 ,O0OO00O0OOO000000 ,O0000O0OO000O0000 .router .functions .swapTokensForExactETH (OO00O0O00OO0O0O0O ,O0OO000OO00OOO0O0 ,[O0000OO0O000OOO0O ,O0000O0OO000O0000 .get_weth_address ()],O0000O0OO000O0000 .address ,O0000O0OO000O0000 ._deadline (),),)#line:673
        def _token_to_token_swap_output (O00OOOO0000000000 ,OO0OOO0000O00OOOO ,OO00O0O00O0000O0O ,OOO00OOO0O00O00OO ,OO0O00OOOOOO0O00O :AddressLike ,O000O000O0000O00O :int ,OO0O0OO000O0O0OO0 :AddressLike ,OOO00OOOO0O0O0000 :Optional [AddressLike ],)->HexBytes :#line:681
            ""#line:682
            if O00OOOO0000000000 .version ==1 :#line:683
                O0OOOOO00OOO0O000 =O00OOOO0000000000 .exchange_contract (OO0O00OOOOOO0O00O ).functions #line:684
                O00O00O0OO00O0OO0 ,OO0O0O000O00O0000 =O00OOOO0000000000 ._calculate_max_input_token (OO0O00OOOOOO0O00O ,O000O000O0000O00O ,OO0O0OO000O0O0OO0 )#line:687
                O0000000OO00OO000 =O00OOOO0000000000 ._get_tx_params (gwei =OO0OOO0000O00OOOO )#line:688
                OO0O0OO0O0O0O000O =[O000O000O0000O00O ,O00O00O0OO00O0OO0 ,OO0O0O000O00O0000 ,O00OOOO0000000000 ._deadline (),OO0O0OO000O0O0OO0 ,]#line:695
                if not OOO00OOOO0O0O0000 :#line:696
                    OO0OO000O00O0OOOO =O0OOOOO00OOO0O000 .tokenToTokenSwapOutput (*OO0O0OO0O0O0O000O )#line:697
                else :#line:698
                    OO0O0OO0O0O0O000O .insert (len (OO0O0OO0O0O0O000O )-1 ,OOO00OOOO0O0O0000 )#line:699
                    OO0OO000O00O0OOOO =O0OOOOO00OOO0O000 .tokenToTokenTransferOutput (*OO0O0OO0O0O0O000O )#line:700
                return O00OOOO0000000000 ._build_and_send_tx (OO0OOO0000O00OOOO ,OO00O0O00O0000O0O ,OOO00OOO0O00O00OO ,OO0OO000O00O0OOOO ,O0000000OO00OO000 )#line:701
            else :#line:702
                OOOOOOOOO0OOOOO0O =O00OOOO0000000000 .get_token_token_output_price (OO0O00OOOOOO0O00O ,OO0O0OO000O0O0OO0 ,O000O000O0000O00O )#line:703
                O00O0O00OOOO0O00O =int ((1 +O00OOOO0000000000 .max_slippage )*OOOOOOOOO0OOOOO0O )#line:704
                return O00OOOO0000000000 ._build_and_send_tx (OO0OOO0000O00OOOO ,OO00O0O00O0000O0O ,OOO00OOO0O00O00OO ,O00OOOO0000000000 .router .functions .swapTokensForExactTokens (O000O000O0000O00O ,O00O0O00OOOO0O00O ,[OO0O00OOOOOO0O00O ,O00OOOO0000000000 .get_weth_address (),OO0O0OO000O0O0OO0 ],O00OOOO0000000000 .address ,O00OOOO0000000000 ._deadline (),),)#line:713
        def _get_tx_params2 (O0O0OOO0OOOOOOO00 ,O000OO00OOOOO0OO0 :Wei =Wei (0 ),OOO000OOOOO0OO0O0 :Wei =Wei (250000 ))->TxParams :#line:716
            ""#line:717
            return {"from":_O0OOO00OO0O0000O0 (O0O0OOO0OOOOOOO00 .address ),"value":O000OO00OOOOO0OO0 ,"gas":OOO000OOOOO0OO0O0 ,"nonce":max (O0O0OOO0OOOOOOO00 .last_nonce ,O0O0OOO0OOOOOOO00 .w3 .eth .getTransactionCount (O0O0OOO0OOOOOOO00 .address )),}#line:725
        def _build_and_send_tx2 (OO0O0OO0O0O0OOOOO ,O0000O00O0OOO00O0 :ContractFunction ,OOO0000O0OOO0O0OO :Optional [TxParams ]=None )->HexBytes :#line:729
            ""#line:730
            if not OOO0000O0OOO0O0OO :#line:731
                OOO0000O0OOO0O0OO =OO0O0OO0O0O0OOOOO ._get_tx_params2 ()#line:732
            O0000OOOO0O0OOOO0 =O0000O00O0OOO00O0 .buildTransaction (OOO0000O0OOO0O0OO )#line:733
            OOOOO000000OOO0OO =OO0O0OO0O0O0OOOOO .w3 .eth .account .sign_transaction (O0000OOOO0O0OOOO0 ,private_key =OO0O0OO0O0O0OOOOO .private_key )#line:736
            try :#line:739
                return OO0O0OO0O0O0OOOOO .w3 .eth .sendRawTransaction (OOOOO000000OOO0OO .rawTransaction )#line:740
            finally :#line:741
                logger .debug (f"nonce: {OOO0000O0OOO0O0OO['nonce']}")#line:742
                OO0O0OO0O0O0OOOOO .last_nonce =Nonce (OOO0000O0OOO0O0OO ["nonce"]+1 )#line:743
        def approve (O0O00OO000OOOO0O0 ,O000O0O00OOOO000O :AddressLike ,O0O00O0O00OO0O00O :Optional [int ]=None )->None :#line:745
            ""#line:746
            O0O00O0O00OO0O00O =O0O00OO000OOOO0O0 .max_approval_int if not O0O00O0O00OO0O00O else O0O00O0O00OO0O00O #line:747
            O0O0OOOO0OO00000O =(O0O00OO000OOOO0O0 .exchange_address_from_token (O000O0O00OOOO000O )if O0O00OO000OOOO0O0 .version ==1 else O0O00OO000OOOO0O0 .router_address )#line:752
            O00O00OO0000000OO =O0O00OO000OOOO0O0 .erc20_contract (O000O0O00OOOO000O ).functions .approve (O0O0OOOO0OO00000O ,O0O00O0O00OO0O00O )#line:755
            logger .info (f"Approving {_O0OOO00OO0O0000O0(O000O0O00OOOO000O)}...")#line:756
            print (f"Approving {_O0OOO00OO0O0000O0(O000O0O00OOOO000O)}...")#line:757
            O0OO000O0OO0000O0 =O0O00OO000OOOO0O0 ._build_and_send_tx2 (O00O00OO0000000OO )#line:758
            O0O00OO000OOOO0O0 .w3 .eth .waitForTransactionReceipt (O0OO000O0OO0000O0 ,timeout =6000 )#line:759
            time .sleep (1 )#line:762
        def _is_approved (OOO00000000O0O000 ,OOO00O0O0O00OOO0O :AddressLike )->bool :#line:764
            ""#line:765
            _OOO00OOOOO0OO0000 (OOO00O0O0O00OOO0O )#line:766
            if OOO00000000O0O000 .version ==1 :#line:767
                OOOO00OO000O00O00 =OOO00000000O0O000 .exchange_address_from_token (OOO00O0O0O00OOO0O )#line:768
            else :#line:769
                OOOO00OO000O00O00 =OOO00000000O0O000 .router_address #line:770
            OO0OOO00O0O0O0O00 =(OOO00000000O0O000 .erc20_contract (OOO00O0O0O00OOO0O ).functions .allowance (OOO00000000O0O000 .address ,OOOO00OO000O00O00 ).call ())#line:775
            if OO0OOO00O0O0O0O00 >=OOO00000000O0O000 .max_approval_check_int :#line:776
                return True #line:777
            else :#line:778
                return False #line:779
        def _deadline (OO00OO0O0O000OOO0 )->int :#line:782
            ""#line:783
            return int (time .time ())+10 *60 #line:784
        def _build_and_send_tx (O0OO00OOO0O00OOO0 ,O000OO00O0000O0O0 ,OOO00O0OOO0OOO00O ,OOOOO0OO0OOO00000 ,O0O00O0OOOOOOO0O0 :ContractFunction ,OO0O00OOO00O0OO0O :Optional [TxParams ]=None )->HexBytes :#line:788
            if not OO0O00OOO00O0OO0O :#line:789
                OO0O00OOO00O0OO0O =O0OO00OOO0O00OOO0 ._get_tx_params (O000OO00O0000O0O0 ,OOO00O0OOO0OOO00O )#line:790
            O000O0000OOO00O00 =O0O00O0OOOOOOO0O0 .buildTransaction (OO0O00OOO00O0OO0O )#line:791
            OO00OOOO00OO00000 =O0OO00OOO0O00OOO0 .w3 .eth .account .sign_transaction (O000O0000OOO00O00 ,private_key =OOOOO0OO0OOO00000 )#line:794
            try :#line:797
                return O0OO00OOO0O00OOO0 .w3 .eth .sendRawTransaction (OO00OOOO00OO00000 .rawTransaction )#line:798
            finally :#line:799
                logger .debug (f"nonce: {OO0O00OOO00O0OO0O['nonce']}")#line:800
                O0OO00OOO0O00OOO0 .last_nonce =Nonce (OO0O00OOO00O0OO0O ["nonce"]+1 )#line:801
        def _get_tx_params (OOOOO000OO0O0000O ,OO00OO00OOOO000OO ,OOO000O000O0O0OO0 ,OOOOO00OOO00OOOO0 :Wei =Wei (0 ),OO000OOOOO0O0OOO0 :Wei =Wei (250000 ))->TxParams :#line:803
            ""#line:804
            return {"from":OOO000O000O0O0OO0 ,"value":OOOOO00OOO00OOOO0 ,"gas":OO000OOOOO0O0OOO0 ,"gasPrice":OO00OO00OOOO000OO ,"nonce":max (OOOOO000OO0O0000O .last_nonce ,OOOOO000OO0O0000O .w3 .eth .getTransactionCount (OOOOO000OO0O0000O .address )),}#line:813
        def _calculate_max_input_token (O000000O0O00O00OO ,OOOOO00O00OO00OOO :AddressLike ,O00O0OO000O000000 :int ,OOO00OO000000OO0O :AddressLike )->Tuple [int ,int ]:#line:818
            ""#line:825
            O0OOO0O0OOO00OOO0 =O00O0OO000O000000 #line:827
            O00O00OO000000000 =O000000O0O00O00OO .get_ex_eth_balance (OOO00OO000000OO0O )#line:828
            OOOOO0OOO0OO0O00O =O000000O0O00O00OO .get_ex_token_balance (OOO00OO000000OO0O )#line:829
            OO00O0OO0OOO0OOO0 =O0OOO0O0OOO00OOO0 *O00O00OO000000000 *1000 #line:832
            OOO0O00OO00OOO00O =(OOOOO0OOO0OO0O00O -O0OOO0O0OOO00OOO0 )*997 #line:833
            O00OO0OO000OO0OO0 =OO00O0OO0OOO0OOO0 /OOO0O00OO00OOO00O +1 #line:834
            O0O00OO00O0OOO0OO =O00OO0OO000OO0OO0 #line:837
            OOOO000O0O0O0O00O =O000000O0O00O00OO .get_ex_token_balance (OOOOO00O00OO00OOO )#line:838
            O0O0O00O0000O0OOO =O000000O0O00O00OO .get_ex_eth_balance (OOOOO00O00OO00OOO )#line:839
            OOO00O00OO00O0OOO =O0O00OO00O0OOO0OO *OOOO000O0O0O0O00O *1000 #line:842
            OOO0000O000OO00O0 =(O0O0O00O0000O0OOO -O0O00OO00O0OOO0OO )*997 #line:843
            O000OO0O0O0O0000O =OOO00O00OO00O0OOO /OOO0000O000OO00O0 -1 #line:844
            return int (O000OO0O0O0O0000O ),int (1.2 *O00OO0OO000OO0OO0 )#line:846
        def _calculate_max_output_token (O00O0O00OO0OOOO00 ,OO000O0O0O000OOO0 :AddressLike ,OO00OOOO000OO0000 :int ,OOOOOO0O000O0OO0O :AddressLike )->Tuple [int ,int ]:#line:850
            ""#line:854
            OO000O00OO0OOO0OO =OO00OOOO000OO0000 #line:856
            OOO0OO0O0O0OOO0O0 =O00O0O00OO0OOOO00 .get_ex_token_balance (OOOOOO0O000O0OO0O )#line:857
            OO000OO0O0000OO0O =O00O0O00OO0OOOO00 .get_ex_eth_balance (OOOOOO0O000O0OO0O )#line:858
            O0OOO0000000OOOOO =OO000O00OO0OOO0OO *OO000OO0O0000OO0O *997 #line:861
            OOOO000O0O000000O =OOO0OO0O0O0OOO0O0 *1000 +OO000O00OO0OOO0OO *997 #line:862
            OO00000O00OOO00O0 =O0OOO0000000OOOOO /OOOO000O0O000000O #line:863
            OO000OO00O00O0O00 =OO00000O00OOO00O0 #line:866
            OO000O0O0O0000O00 =O00O0O00OO0OOOO00 .get_ex_token_balance (OO000O0O0O000OOO0 )#line:867
            O00OO0OOO0O00O0O0 =O00O0O00OO0OOOO00 .get_ex_eth_balance (OO000O0O0O000OOO0 )#line:868
            OOO00OO0OOO000O0O =OO000OO00O00O0O00 *O00OO0OOO0O00O0O0 *997 #line:871
            O0OOOOOO0000OOOOO =OO000O0O0O0000O00 *1000 +OO000OO00O00O0O00 *997 #line:872
            OOO0000OO0OOOOO00 =OOO00OO0OOO000O0O /O0OOOOOO0000OOOOO #line:873
            return int (OOO0000OO0OOOOO00 ),int (1.2 *OO00000O00OOO00O0 )#line:875
        def _buy_test_assets (O0O000O000OO000OO )->None :#line:879
            ""#line:883
            OO0O0O00O0O0OO000 =1 *10 **18 #line:884
            O000O00O000OOO0O0 =int (0.1 *OO0O0O00O0O0OO000 )#line:885
            O0O0000OO0O0OO0O0 =O0O000O000OO000OO ._get_token_addresses ()#line:886
            for OO0O0OOO0000000O0 in ["BAT","DAI"]:#line:888
                OO0OO00O00000O0O0 =O0O0000OO0O0OO0O0 [OO0O0OOO0000000O0 .lower ()]#line:889
                OOOO0O00O00OO0OOO =O0O000O000OO000OO .get_eth_token_output_price (_OOO000000OOO0OO00 (OO0OO00O00000O0O0 ),O000O00O000OOO0O0 )#line:890
                logger .info (f"Cost of {O000O00O000OOO0O0} {OO0O0OOO0000000O0}: {OOOO0O00O00OO0OOO}")#line:891
                logger .info ("Buying...")#line:892
                O0OO00OO0O0OO00O0 =O0O000O000OO000OO .make_trade_output (O0O0000OO0O0OO0O0 ["eth"],O0O0000OO0O0OO0O0 [OO0O0OOO0000000O0 .lower ()],O000O00O000OOO0O0 )#line:895
                O0O000O000OO000OO .w3 .eth .waitForTransactionReceipt (O0OO00OO0O0OO00O0 )#line:896
        def _get_token_addresses (O0OO00O0OOOO0O00O )->Dict [str ,str ]:#line:898
            ""#line:902
            OOOOOO00O0OO0O0OO =int (O0OO00O0OOOO0O00O .w3 .net .version )#line:903
            O0O000OO000O0O0OO =_OO00OO0OOO0O0OO00 [OOOOOO00O0OO0O0OO ]#line:904
            if O0O000OO000O0O0OO =="mainnet":#line:905
                return {"eth":"0x0000000000000000000000000000000000000000","bat":Web3 .toChecksumAddress ("0x0D8775F648430679A709E98d2b0Cb6250d2887EF"),"dai":Web3 .toChecksumAddress ("0x6b175474e89094c44da98b954eedeac495271d0f"),}#line:914
            elif O0O000OO000O0O0OO =="rinkeby":#line:915
                return {"eth":"0x0000000000000000000000000000000000000000","bat":"0xDA5B056Cfb861282B4b59d29c9B395bcC238D29B","dai":"0x2448eE2641d78CC42D7AD76498917359D961A783",}#line:920
            else :#line:921
                raise Exception (f"Unknown net '{O0O000OO000O0O0OO}'")#line:922
except SyntaxError as err :#line:925
    traceback .print_exc ()#line:926
