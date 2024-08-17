import json
import os
from web3 import Web3
from decimal import Decimal
import asyncio
import time
from itertools import chain, groupby
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()


RPC_url = 'http://localhost:8545/'
w3 = Web3(Web3.HTTPProvider(RPC_url))

class Constants:
    hebe_wetc = '0x82A618305706B14e7bcf2592D4B9324A366b6dAd'
    etc_swap_wetc = '0x1953cab0E5bFa6D4a9BaD6E05fD46C1CC6527a5a'
    usopp ='0x1aCeE42A23d7EA2f6CAA5CE04C699db97F71844d'
    botPilot = ''
    botPilot2 = ''
    usopp_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_executor","type":"address"}],"stateMutability":"payable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"_amountOutMin","type":"uint256"},{"internalType":"address[]","name":"_path","type":"address[]"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_deadline","type":"uint256"}],"name":"ExecuteBuySwap","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amountOutMin","type":"uint256"},{"internalType":"address[]","name":"_path","type":"address[]"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_deadline","type":"uint256"},{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_amountIn","type":"uint256"}],"name":"ExecuteSellSwap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_withdrawalamount","type":"uint256"},{"internalType":"address","name":"_tokencontract","type":"address"}],"name":"WithdrawERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"_recipient","type":"address"}],"name":"WithdrawETC","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_wetcwithdrawalamount","type":"uint256"}],"name":"WithdrawWETC","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
    private_key = ""
    private_key_2 = ""
    hebe_factory = '0x09fafa5eecbc11C3e5d30369e51B7D9aab2f3F53'
    etcswap_factory = '0x0307cd3D7DA98A29e6Ed0D2137be386Ec1e4Bc9C'
    factory_abi = json.loads('[{"type":"constructor","stateMutability":"nonpayable","payable":false,"inputs":[{"type":"address","name":"_feeToSetter","internalType":"address"}]},{"type":"event","name":"PairCreated","inputs":[{"type":"address","name":"token0","internalType":"address","indexed":true},{"type":"address","name":"token1","internalType":"address","indexed":true},{"type":"address","name":"pair","internalType":"address","indexed":false},{"type":"uint256","name":"","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"allPairs","inputs":[{"type":"uint256","name":"","internalType":"uint256"}],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allPairsLength","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"address","name":"pair","internalType":"address"}],"name":"createPair","inputs":[{"type":"address","name":"tokenA","internalType":"address"},{"type":"address","name":"tokenB","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"feeHolder","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"feeTo","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"feeToSetter","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"getPair","inputs":[{"type":"address","name":"","internalType":"address"},{"type":"address","name":"","internalType":"address"}],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"setFeeTo","inputs":[{"type":"address","name":"_feeTo","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"setFeeToSetter","inputs":[{"type":"address","name":"_feeToSetter","internalType":"address"}],"constant":false}]')
    er20_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')
    hebe_router = '0xEcBcF5C7aF4c323947CFE982940BA7c9fd207e2b'
    etcswap_router = '0x79Bf07555C34e68C4Ae93642d1007D7f908d60F5'
    etcmc_router = '0x2d18693b77acF8F2785084B0Ae53F6e0627e4376'
    etcmc_factory = '0x164999e9174686b39987dfb7e0fab28465b867a5'
    etcmc_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
    factory_addresses = [hebe_factory,etcswap_factory,etcmc_factory]
    router_addresses = [hebe_router,etcswap_router,etcmc_router]
    wetc_addresses =[hebe_wetc, etc_swap_wetc]
    lookup_contract_address = '0x5200b29D7018880A623b7719C94F8832e2B03891'
    lookup_contract_abi = json.loads('[{"inputs":[{"internalType":"contract UniswapV2Factory","name":"_uniswapFactory","type":"address"},{"internalType":"uint256","name":"_start","type":"uint256"},{"internalType":"uint256","name":"_stop","type":"uint256"}],"name":"getPairsByIndexRange","outputs":[{"internalType":"address[3][]","name":"","type":"address[3][]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IUniswapV2Pair[]","name":"_pairs","type":"address[]"}],"name":"getReservesByPairs","outputs":[{"internalType":"uint256[5][]","name":"","type":"uint256[5][]"}],"stateMutability":"view","type":"function"}]')
    kabuto_v2 = ''
    ETHER = int(6000000000000000000)
    kabuto_v2_abi = json.loads('')
    router_abi = json.loads('[{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"address","name":"_factory","internalType":"address"},{"type":"address","name":"_WETC","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"WETC","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"amountB","internalType":"uint256"},{"type":"uint256","name":"liquidity","internalType":"uint256"}],"name":"addLiquidity","inputs":[{"type":"address","name":"tokenA","internalType":"address"},{"type":"address","name":"tokenB","internalType":"address"},{"type":"uint256","name":"amountADesired","internalType":"uint256"},{"type":"uint256","name":"amountBDesired","internalType":"uint256"},{"type":"uint256","name":"amountAMin","internalType":"uint256"},{"type":"uint256","name":"amountBMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256","name":"amountToken","internalType":"uint256"},{"type":"uint256","name":"amountETC","internalType":"uint256"},{"type":"uint256","name":"liquidity","internalType":"uint256"}],"name":"addLiquidityETC","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"amountTokenDesired","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETCMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"factory","inputs":[]},{"type":"function","stateMutability":"pure","outputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"}],"name":"getAmountIn","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"uint256","name":"reserveIn","internalType":"uint256"},{"type":"uint256","name":"reserveOut","internalType":"uint256"}]},{"type":"function","stateMutability":"pure","outputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"}],"name":"getAmountOut","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"reserveIn","internalType":"uint256"},{"type":"uint256","name":"reserveOut","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"getAmountsIn","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"getAmountsOut","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"}]},{"type":"function","stateMutability":"pure","outputs":[{"type":"uint256","name":"amountB","internalType":"uint256"}],"name":"quote","inputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"reserveA","internalType":"uint256"},{"type":"uint256","name":"reserveB","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"amountB","internalType":"uint256"}],"name":"removeLiquidity","inputs":[{"type":"address","name":"tokenA","internalType":"address"},{"type":"address","name":"tokenB","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountAMin","internalType":"uint256"},{"type":"uint256","name":"amountBMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountToken","internalType":"uint256"},{"type":"uint256","name":"amountETC","internalType":"uint256"}],"name":"removeLiquidityETC","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETCMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountETC","internalType":"uint256"}],"name":"removeLiquidityETCSupportingFeeOnTransferTokens","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETCMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountToken","internalType":"uint256"},{"type":"uint256","name":"amountETC","internalType":"uint256"}],"name":"removeLiquidityETCWithPermit","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETCMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"bool","name":"approveMax","internalType":"bool"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountETC","internalType":"uint256"}],"name":"removeLiquidityETCWithPermitSupportingFeeOnTransferTokens","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETCMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"bool","name":"approveMax","internalType":"bool"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"amountB","internalType":"uint256"}],"name":"removeLiquidityWithPermit","inputs":[{"type":"address","name":"tokenA","internalType":"address"},{"type":"address","name":"tokenB","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountAMin","internalType":"uint256"},{"type":"uint256","name":"amountBMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"bool","name":"approveMax","internalType":"bool"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapETCForExactTokens","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapExactETCForTokens","inputs":[{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[],"name":"swapExactETCForTokensSupportingFeeOnTransferTokens","inputs":[{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapExactTokensForETC","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"swapExactTokensForETCSupportingFeeOnTransferTokens","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapExactTokensForTokens","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapTokensForExactETC","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"uint256","name":"amountInMax","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapTokensForExactTokens","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"uint256","name":"amountInMax","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"receive","stateMutability":"payable"}]')

class MarketPair:
    def __init__(self, address: str,router: str ,tokens: List[str] = None, token_balances: Dict[str, int] = None, decimal_places:Dict[str,int]=None ):
        self.address = address
        self._tokens = tokens or []
        self.router = router
        self._token_balances = token_balances or {}
        self._decimal_places = decimal_places or {}
    
    def get_matching_token(self, address1: str, address2: str) -> str:
        for token in self._tokens:
            if token == address1 or token == address2:
                return token
        return None
    
    def get_other_token(self, address1: str, address2: str) -> str:
        for token in self._tokens:
            if token != address1 and token != address2:
                return token
        return None

    def set_reserves_via_ordered_balances(self, balances: List[int]):
        self.set_reserves_via_matching_array(self._tokens, balances)

    def set_reserves_via_matching_array(self, tokens: List[str], balances: List[int]):
        token_balances = dict(zip(tokens, balances))
        if self._token_balances != token_balances:
            self._token_balances = token_balances

    def set_ordered_decimal_places(self, decimal_places: List[int]):
        self.set_decimal_via_matching_array(self._tokens, decimal_places)

    def set_decimal_via_matching_array(self, tokens: List[str], decimal_places: List[int]):
        decimal_places = dict(zip(tokens, decimal_places))
        self._decimal_places = decimal_places
    

    def __repr__(self):
        return f"MarketPair(address={self.address}, tokens={self._tokens}, token_balances={self._token_balances}, decimal_places={self._decimal_places})"

    def get_balance(self, token_address: str) -> int:
        balance = self._token_balances.get(token_address)
        if balance is None:
            raise ValueError("bad token")
        return balance
    
    def get_decimals(self, token_address: str) -> int:
        decimal_places = self._decimal_places.get(token_address)
        if decimal_places is None:
            raise ValueError("bad token")
        return decimal_places

async def estimate_amount_out_and_trade(arbitrage_p):

    for key in arbitrage_p.keys():

        lower_bound = Decimal(0)
        
        upper_bound = Decimal(0.3) * Decimal(w3.from_wei(w3.eth.get_balance(Constants.botPilot2), 'ether')) 
        
        optimal_swap_amount, sell_amount_out, buy_amount_out = find_optimal_swap_amount(lower_bound, upper_bound, key, arbitrage_p)

        buy_reserves_dict = arbitrage_p[key]['buy_token_balances']
        sell_reserves_dict = arbitrage_p[key]['sell_token_balances']

        buy_decimals_dict = arbitrage_p[key]['buy_decimals']

     
        sell_decimals_dict = arbitrage_p[key]['sell_decimals']


        buy_token_0 = list(buy_reserves_dict.keys())[0]
        buy_token_1 = list(buy_reserves_dict.keys())[1]
        sell_token_0 = list(sell_reserves_dict.keys())[0]
        sell_token_1 = list(sell_reserves_dict.keys())[1]


        buy_pair = [buy_token_0, buy_token_1]

        if buy_pair[0] in Constants.wetc_addresses:
            buy_pair = [buy_pair[0], buy_pair[1]]
        else:
            buy_pair = [buy_pair[1], buy_pair[0]]

        buy_swap_path = buy_pair

        buy_receipt = ''
        
        sell_receipt = None
        
        sellamountoutmin = Decimal(0.8) * Decimal(sell_amount_out)
        
        if (sellamountoutmin - optimal_swap_amount > Decimal(0.0009)):
        
                sell_pair = [sell_token_0, sell_token_1]

                if sell_pair[0] in Constants.wetc_addresses:
                    sell_pair = [sell_pair[1], sell_pair[0]]
                else:
                    sell_pair = [sell_pair[0],sell_pair[1]]
                
                sell_path = sell_pair

                sell_receipt, sold = await atomic_swap(optimal_swap_amount,
                                                       buy_swap_path,
                                                       (Decimal(0.8) * Decimal(buy_amount_out)),
                                                       arbitrage_p[key]['buy_router'],
                                                       buy_decimals_dict[buy_swap_path[1]],
                                                       sell_amount_out,
                                                       arbitrage_p[key]['sell_router'],
                                                       sell_path)

                return buy_receipt, sell_receipt
        else:
           print( "not worth it" )

#get wetc address for the factory
def get_canonical_wetc(router_address):

    if router_address == Constants.etcmc_router:
        router_contract =  w3.eth.contract(address=Constants.etcmc_router, abi=Constants.etcmc_abi)

        canonical_wetc  = router_contract.functions.WETH().call()
    else:
        router_contract =  w3.eth.contract(address=router_address, abi=Constants.router_abi)
        
        canonical_wetc  = router_contract.functions.WETC().call()

    return canonical_wetc

async def get_uniswap_markets_by_token():

    all_pairs = await get_all_pairs(Constants.factory_addresses, Constants.router_addresses)



    markets_by_token_all = {
    key: list(group)
    for key, group in groupby(
        sorted(chain(*all_pairs), key=lambda tokens: tokens['tokens'][0]),
        key=lambda tokens: tokens['tokens'][0]
    )
    }


    # Filtering pairs with more than one entry, i.e. there is an arb opportunity
    filtered_markets_by_token_all = {key: value for key, value in markets_by_token_all.items() if len(value) > 1}

   
    # Flattening and collecting all market pairs
    all_market_pairs_data = list(chain.from_iterable(filtered_markets_by_token_all.values()))

    # Map the data to the MarketPair class
    all_market_pairs = [MarketPair(**data) for data in all_market_pairs_data]

    all_market_pairs, markets_by_token = await update_pairs_and_filter(all_market_pairs)


    return all_market_pairs, markets_by_token

#get all pairs, append only pairs that have the wrapped ether
async def get_all_pairs(factory_addresses, router_addresses):
    all_pairs = await asyncio.gather(
        *[get_uniswappy_markets(factory_address, router_address) for factory_address, router_address in zip(factory_addresses, router_addresses)]
    )
    return all_pairs

async def get_uniswappy_markets(factory_address, router_address):

    market_pairs = []

    query_contract = w3.eth.contract(address=Constants.lookup_contract_address, abi = Constants.lookup_contract_abi)

    canonical_wetc = get_canonical_wetc(router_address)

    # for i in range(0, Constants.batch_count_limit * Constants.uniswap_batch_size, Constants.uniswap_batch_size):
      
    pairs = query_contract.functions.getPairsByIndexRange(w3.to_checksum_address(factory_address), 0, 900).call()
    
    for pair in pairs:

        if pair[0] == canonical_wetc or pair[1] == canonical_wetc:
            market_address = pair[2]
            other_token = pair[0] if pair[0] != canonical_wetc else pair[1]
            uniswappy_v2_eth_pair = {"address": market_address, "tokens": [pair[0], pair[1]], "router": router_address}
            market_pairs.append(uniswappy_v2_eth_pair)

    
    return market_pairs

async def update_pairs_and_filter(all_market_pairs):
        #get current reserves for each pair
    await update_reserves(all_market_pairs) 


    # filter for  balance greater than whatever the value in constants is, 
    # but this means groups are lost, seems to be only the USDT pairs that qualify
    filtered_pairs = [pair for pair in all_market_pairs if pair.get_balance(pair.get_matching_token(Constants.hebe_wetc,Constants.etc_swap_wetc)) > Constants.ETHER]    

    #group again by tokens that are not the wrapped ether token
    markets_by_token = {key: list(group) for key, group in groupby(sorted(filtered_pairs, key=lambda pair: pair.get_other_token(Constants.hebe_wetc, Constants.etc_swap_wetc)), key=lambda pair: pair.get_other_token(Constants.hebe_wetc, Constants.etc_swap_wetc))}

    #filter again for items with more than one market found, this is because adjusting for actual value in the pair removes some
    markets_by_token = {key: value for key, value in markets_by_token.items() if len(value) > 1}

    return all_market_pairs, markets_by_token

#get token price in WETC, reference is WETC and price should only be in WETC to compare across markets
def get_token_price(markets_by_token):

    result_dict = {}
  
    for address, market_pairs in markets_by_token.items():
        result_list = []
        for market_pair in market_pairs:
            if any(token in market_pair._tokens for token in Constants.wetc_addresses):
                
                fixed_value = next(token for token in Constants.wetc_addresses if token in market_pair._tokens)

                other_value = market_pair.get_other_token(Constants.hebe_wetc,Constants.etc_swap_wetc)
                
                balance_fixed = market_pair.get_balance(fixed_value)
                
                balance_fixed_decimals = market_pair.get_decimals(fixed_value)

                balance_fixed = balance_fixed/Decimal(10 ** balance_fixed_decimals)
              
                balance_other = market_pair.get_balance(other_value)

                balance_other_decimals = market_pair.get_decimals(other_value)

                balance_other = balance_other/Decimal(10 ** balance_other_decimals)
     
                #price in wetc, i.e. how may wetc per other token
                price =  balance_fixed/balance_other if balance_fixed != 0 else 0
                
                result_list.append({'address': market_pair.address, 
                                    'price': price,
                                    'token_balances':market_pair._token_balances,
                                    'decimals':market_pair._decimal_places,
                                    'router':market_pair.router})
    
        result_dict[address] = result_list
    
    return result_dict

def get_highest_price(data):

# Create a new dictionary to store the result
    result_dict = {}

    # Iterate through each entry in the data dictionary
    for key, pairs in data.items():
        # Extract prices from each pair
        ratios = [pair['price'] for pair in pairs]

        # Find the highest and lowest ratios
        sell_price = max(ratios)
        buy_price = min(ratios)

        # Calculate the percentage difference
        percentage_difference = ((sell_price - buy_price) / sell_price) * 100

        # Find the address with the highest and lowest prices
        buy_address = next(pair['address'] for pair in pairs if pair['price'] == buy_price)
        sell_address = next(pair['address'] for pair in pairs if pair['price'] == sell_price)
        buy_token_balances = next(pair['token_balances'] for pair in pairs if pair['price'] == buy_price)
        sell_token_balances = next(pair['token_balances'] for pair in pairs if pair['price'] == sell_price)
        buy_decimals = next(pair['decimals'] for pair in pairs if pair['price'] == buy_price)
        sell_decimals = next(pair['decimals'] for pair in pairs if pair['price'] == sell_price)
        buy_router = next(pair['router'] for pair in pairs if pair['price'] == buy_price)
        sell_router = next(pair['router'] for pair in pairs if pair['price'] == sell_price)




        # Add the result to the dictionary
        result_dict[key] = {
            'percentage_difference': percentage_difference,
            'buy_address': buy_address,
            'sell_address': sell_address,
            'buy_token_balances':buy_token_balances,
            'sell_token_balances':sell_token_balances,
            'buy_decimals':buy_decimals,
            'sell_decimals': sell_decimals,
            'buy_router': buy_router,
            'sell_router':sell_router
        }

    return result_dict

async def atomic_swap(buyamount,
                      buyswappath, 
                      buyminamountout, 
                      buyrouter, buydecimals, 
                      sell_amount_out, sellrouter, sellpath):


        kabuto_v2 = w3.eth.contract(address=Constants.kabuto_v2, abi=Constants.kabuto_v2_abi)
        
        account_address = Constants.botPilot2
        
        sellamountoutmin = Decimal(0.5) * Decimal(sell_amount_out)

        buyminamountout = Decimal(buyminamountout) * (10 ** buydecimals)
        
        buypath = [buyswappath[0],buyswappath[1]]

        swap = kabuto_v2.functions.AtomicSwap(
            int(buyminamountout),
            buypath,
            str(buyrouter),
            w3.to_wei(sellamountoutmin,'ether'),
            sellpath,
            str(sellrouter)
            )
        
        tx = swap.build_transaction({
        'from': account_address,
        'gas' : int(509000),
        'gasPrice': int(1314159265),
        'nonce': w3.eth.get_transaction_count(account_address),
        'value':w3.to_wei(buyamount,'ether')
        })

        signed_tx = w3.eth.account.sign_transaction(tx, Constants.private_key_2)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = None
        sold = False
        while receipt is None:
            try:
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=1200)
                sold = True
            except Web3.exceptions.TimeExhausted:
                pass
    
        return receipt, sold
   



def calculate_difference(swapFromAmount, key, arbitrage_p):
    buy_reserves_dict = arbitrage_p[key]['buy_token_balances']
    sell_reserves_dict = arbitrage_p[key]['sell_token_balances']
    buy_decimals_dict = arbitrage_p[key]['buy_decimals']
    sell_decimals_dict = arbitrage_p[key]['sell_decimals']

    buy_token_0 = list(buy_reserves_dict.keys())[0]
    sell_token_0 = list(sell_reserves_dict.keys())[0]

    buy_token0_decimals = buy_decimals_dict.get(list(buy_reserves_dict.keys())[0])
    buy_token1_decimals = buy_decimals_dict.get(list(buy_reserves_dict.keys())[1])
    sell_token0_decimals = sell_decimals_dict.get(list(sell_reserves_dict.keys())[0])
    sell_token1_decimals = sell_decimals_dict.get(list(sell_reserves_dict.keys())[1])




    buy_reserve_0 = buy_reserves_dict.get(list(buy_reserves_dict.keys())[0])/ (10 ** buy_token0_decimals)
    buy_reserve_1 = buy_reserves_dict.get(list(buy_reserves_dict.keys())[1]) / (10 ** buy_token1_decimals)
    sell_reserve_0 = sell_reserves_dict.get(list(sell_reserves_dict.keys())[0]) / (10 ** sell_token0_decimals)
    sell_reserve_1 = sell_reserves_dict.get(list(sell_reserves_dict.keys())[1]) / (10 ** sell_token1_decimals)

    buy_constant_product = Decimal(buy_reserve_0) * Decimal(buy_reserve_1)

    if buy_token_0 in [Constants.hebe_wetc, Constants.etc_swap_wetc]:
        new_buy_token0_reserve = Decimal(buy_reserve_0) + Decimal(swapFromAmount) + (Decimal(0.003) * Decimal(swapFromAmount))
        new_buy_token1_reserve = buy_constant_product / new_buy_token0_reserve
        buy_amount_out = Decimal(buy_reserve_1) - new_buy_token1_reserve
    else:
        new_buy_token1_reserve = Decimal(buy_reserve_1) + Decimal(swapFromAmount) + (Decimal(0.003) * Decimal(swapFromAmount))
        new_buy_token0_reserve = buy_constant_product / new_buy_token1_reserve
        buy_amount_out = Decimal(buy_reserve_0) - new_buy_token0_reserve
        
    
    sell_constant_product = Decimal(sell_reserve_0) * Decimal(sell_reserve_1)

    if sell_token_0  == key:
       
        new_sell_token0_reserve = Decimal(sell_reserve_0) + Decimal(buy_amount_out) + (Decimal(0.003) * Decimal(buy_amount_out))
        new_sell_token1_reserve = sell_constant_product / new_sell_token0_reserve
        sell_amount_out = Decimal(sell_reserve_1) - new_sell_token1_reserve
    else:
        
        new_sell_token1_reserve = Decimal(sell_reserve_1) + Decimal(buy_amount_out) + (Decimal(0.003) * Decimal(buy_amount_out))
        new_sell_token0_reserve = sell_constant_product / new_sell_token1_reserve
        sell_amount_out = Decimal(sell_reserve_0) - new_sell_token0_reserve


    diff_mid = sell_amount_out - Decimal(swapFromAmount)
    return sell_amount_out, diff_mid, buy_amount_out

def find_optimal_swap_amount(lower_bound, upper_bound, key, arbitrage_p, tolerance=1e-6, max_iterations=100):
    max_difference = float('-inf')
    optimal_swap_amount = None

    for _ in range(max_iterations):
        mid = (lower_bound + upper_bound) / 2
        sell_amount_out, diff_mid, buy_amount_out = calculate_difference(mid, key, arbitrage_p)


        if abs(diff_mid) < tolerance:
            return sell_amount_out, mid, buy_amount_out

        if diff_mid > max_difference:
            max_difference = diff_mid
            optimal_swap_amount = mid

        if diff_mid > 0:
            lower_bound = mid
        else:
            upper_bound = mid

    return optimal_swap_amount, sell_amount_out, buy_amount_out

async def update_reserves(all_market_pairs):

    query_contract = w3.eth.contract(address=Constants.lookup_contract_address, abi = Constants.lookup_contract_abi)
    
    pair_addresses = [market_pair.address for market_pair in all_market_pairs]
    
    reserves = query_contract.functions.getReservesByPairs(pair_addresses).call()

    for i in range(len(all_market_pairs)):
      
      market_pair = all_market_pairs[i]
     
      reserve = reserves[i]

      market_pair.set_reserves_via_ordered_balances([reserve[0], reserve[1]])
      
      market_pair.set_ordered_decimal_places([reserve[3],reserve[4]])

async def evaluate_markets(all_market_pairs):
    

    all_market_pairs, markets_by_token = await update_pairs_and_filter(all_market_pairs)


    #for each token, get price across markets, always in WETC terms
    result = get_token_price(markets_by_token)


    #for each key, determine market to buy from and sell from along with percentage difference in price
    arbitrage_markets = get_highest_price(result)

    await take_markets(arbitrage_markets)

    return 

# for each transaction estimate volume
# check difference between amount bought and the amount sold
# include transaction fee
async def take_markets(arbitrage_markets):

    await estimate_amount_out_and_trade(arbitrage_markets)


    return 


def main():
    loop = asyncio.get_event_loop()
    b, c = loop.run_until_complete(get_uniswap_markets_by_token())
    loop.run_until_complete(evaluate_markets(b))




if __name__ == '__main__':
    main()

    

    

 







