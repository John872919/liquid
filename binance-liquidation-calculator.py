#!/usr/bin/env python3
'''2021-03-26: Reverse-engineer by searching for the following terms in features*.js:
    - bracketMaintenanceMarginRate
    - cumFastMaintenanceAmount
    - bracketNotionalFloor
    - bracketNotionalCap'''


# (max) position, maintenance margin, maintenance amount
maint_lookup_table = [
    (     50_000,  0.4,           0),
    (    250_000,  0.5,          50),
    (  1_000_000,  1.0,       1_300),
    ( 10_000_000,  2.5,      16_300),
    ( 20_000_000,  5.0,     266_300),
    ( 50_000_000, 10.0,   1_266_300),
    (100_000_000, 12.5,   2_516_300),
    (200_000_000, 15.0,   5_016_300),
    (300_000_000, 25.0,  25_016_300),
    (500_000_000, 50.0, 100_016_300),
]


def lookup_maint(pos):
    pct,amt = [(mr,ma) for p,mr,ma in maint_lookup_table if pos<p][0]
    return pct/100, amt


def binance_btc_liq_balance(wallet_balance, contract_qty, entry_price):
    for max_position, maint_margin_rate_pct, maint_amount in maint_lookup_table:
        maint_margin_rate = maint_margin_rate_pct / 100
        liq_price = (wallet_balance + maint_amount - contract_qty*entry_price) / (abs(contract_qty) * (maint_margin_rate - (1 if contract_qty>=0 else -1)))
        base_balance = liq_price * abs(contract_qty)
        if base_balance <= max_position:
            break
    return round(liq_price, 2)


def binance_btc_liq_leverage(leverage, contract_qty, entry_price):
    wallet_balance = abs(contract_qty) * entry_price / leverage
    print('[Wallet-balance-equivalent of %s] '%wallet_balance, end='')
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
