#!/usr/bin/env python3


maint_lookup_table = [
    (   50000,  0.4,       0),
    (  250000,  0.5,      50),
    ( 1000000,  1.0,    1300),
    ( 5000000,  2.5,   16300),
    (10000000,  5.0,  141300),
    (20000000, 10.0,  641300),
    (35000000, 12.5, 1141300),
    (50000000, 15.0, 2016300),
    (  1e1000, 25.0, 7016300),
]


def lookup_maint(pos):
    pct,amt = [(mr,ma) for p,mr,ma in maint_lookup_table if pos<p][0]
    return pct/100, amt


def binance_btc_liq_balance(wallet_balance, contract_qty, entry_price):
    maint_margin_rate,maint_amount = lookup_maint(abs(wallet_balance*contract_qty))
    liq_price = (wallet_balance + maint_amount - contract_qty*entry_price) / (abs(contract_qty) * (maint_margin_rate - (1 if contract_qty>=0 else -1)))
    return round(liq_price, 2)


def binance_btc_liq_leverage(leverage, contract_qty, entry_price):
    wallet_balance = abs(contract_qty) * entry_price / leverage
    return binance_btc_liq_balance(wallet_balance, contract_qty, entry_price)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--wallet-balance', type=float, help='wallet balance in USDT')
    parser.add_argument('--contract-quantity', required=True, type=float, help='contract quantity in BTC, negative for shorts')
    parser.add_argument('--entry-price', required=True, type=float, help='entry price in USDT')
    parser.add_argument('--leverage', type=int, help='leverage to use instead of wallet balance')
    options = parser.parse_args()
    assert (options.leverage is None) != (options.wallet_balance is None)
    if options.leverage:
        print(binance_btc_liq_leverage(options.leverage, options.contract_quantity, options.entry_price))
    else:
        print(binance_btc_liq_balance(options.wallet_balance, options.contract_quantity, options.entry_price))
