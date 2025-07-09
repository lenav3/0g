import time
import random
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Налаштування змінних
rpc_url = "https://your-rpc-url-here"  # Замініть на ваш реальний RPC URL
to_address = "0x3eC8A8705bE1D5ca90066b37ba62c4183B024ebf"  # Контракт токена
spender_address = "0xb95b5953ff8ee5d5d9818cdbefe363ff2191318c"  # Spender для approve
chain_id = 16601
gas_price_gwei = 5  # Базова ціна газу в Gwei

# Приватні ключі
private_keys = [
    "0xYourPrivateKey1",  # Замініть на реальні приватні ключі
    "0xYourPrivateKey2",
    # Додайте більше ключів за потреби
]

# Підключення до ноди
w3 = Web3(Web3.HTTPProvider(rpc_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

if not w3.is_connected():
    raise Exception("Не вдалося підключитися до ноди")

def build_approve_data(spender, amount_wei):
    method_id = "0x095ea7b3"
    spender_clean = spender.lower().replace("0x", "").rjust(64, "0")
    amount_hex = hex(amount_wei)[2:].rjust(64, "0")
    return method_id + spender_clean + amount_hex

def check_balance(address):
    balance = w3.eth.get_balance(address)
    min_balance = w3.to_wei(0.01, 'ether')  # Мінімальний баланс для газу
    return balance >= min_balance

def send_transaction(private_key):
    account = w3.eth.account.from_key(private_key)
    from_address = account.address

    # Перевірка балансу
    if not check_balance(from_address):
        print(f"Недостатній баланс на {from_address}")
        return

    nonce = w3.eth.get_transaction_count(from_address)

    # Випадкова сума токенів (0.01–0.1)
    amount_tokens = random.uniform(0.01, 0.1)
    amount_wei = int(amount_tokens * 10**18)

    data = build_approve_data(spender_address, amount_wei)

    # Побудова транзакції
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': 0,
        'gasPrice': w3.to_wei(max(gas_price_gwei, w3.eth.gas_price / 10**9), 'gwei'),
        'data': data,
        'chainId': chain_id
    }

    # Оцінка газу
    try:
        tx['gas'] = w3.eth.estimate_gas(tx)
    except Exception as e:
        print(f"Помилка оцінки газу для {from_address}: {e}")
        return

    # Підпис і відправка
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    try:
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Відправлено: {tx_hash.hex()} | {from_address} | {amount_tokens:.5f} токенів")
        
        # Очікування підтвердження
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status == 1:
            print(f"Транзакція {tx_hash.hex()} успішна")
        else:
            print(f"Транзакція {tx_hash.hex()} не вдалася")
    except Exception as e:
        print(f"Помилка відправки для {from_address}: {e}")

def main():
    while True:
        private_key = random.choice(private_keys)
        send_transaction(private_key)
        delay = random.randint(60, 600)
        print(f"Чекаю {delay} секунд...")
        time.sleep(delay)

if __name__ == "__main__":
    main()
