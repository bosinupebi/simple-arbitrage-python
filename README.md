# simple-arbitrage-python

This repository contains a simple, mechanical system for discovering, evaluating, rating, and submitting arbitrage opportunities to an EVM RPC endpoint. This script is very unlikely to be profitable, as many users will have access to it, and it is targeting well-known Ethereum opportunities.

This early iteration uses a binary search to solve for the volume, but there are better ways to determine the optimal volume for arbitrage between to uniswapV2 pairs

This repository is a spiritual successor to the Flashbots typescript simple arbitrage repo. See the [Flashbots Simple Arbitrage](https://github.com/flashbots/simple-arbitrage)

Important Variables
=====================
- **RPC_url** - Ethereum RPC endpoint.
- **PRIVATE_KEY** - Private key for the Ethereum EOA that will be submitting Ethereum transactions.
- **botPilot** - Address for the Ethereum EOA that will be submitting Ethereum transactions.



Usage
======================
1. Generate a new bot wallet address and extract the private key into a raw 32-byte format.
2. Bot logic is driven by the util.py file once a profitable trade is found a transaction is sent to kabuto.sol
3. Deploy the included flashquery.sol and kabuto.sol to Ethereum, from a secured account, with the address of the newly created wallet as the constructor argument
4. Fund the newly created wallet with ETH

_It is important to keep both the bot wallet private key secure. The bot wallet attempts to not lose WETH inside an arbitrage, but a malicious user would be able to drain the contract._

