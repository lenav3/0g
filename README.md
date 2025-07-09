# 0g Token Approve Transaction Script

This Python script (`swap.py`) sends ERC-20 `approve` transactions for the 0g token on a blockchain with `chainId=16601`. It uses a list of private keys to generate sender addresses, approves a random amount of 0g tokens (0.01–0.1 tokens) for a specified spender, and includes random delays between transactions (1–10 minutes).

## Prerequisites

- **Python 3.8+**: Ensure Python is installed. Download from [python.org](https://www.python.org/downloads/).
- **web3.py**: The script uses the `web3.py` library to interact with the blockchain.
- **Access to a Node**: You need an RPC URL for a node supporting the 0g network (`chainId=16601`), such as a custom node or a provider like Infura or Alchemy (if supported).
- **Private Keys**: Valid private keys for accounts with sufficient ETH (or native currency of the 0g network) to cover gas fees.
- **0g Token Contract**: The script interacts with the 0g token ERC-20 contract at the specified address.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lenav3/0g.git
   cd 0g
   ```

2. **Install Dependencies**:
   Install the required Python library using pip:
   ```bash
   pip install web3
   ```

## Configuration

Edit the `swap.py` file to configure the following variables at the top:

- **`rpc_url`**: Replace `"https://your-rpc-url-here"` with the RPC URL for the 0g network (`chainId=16601`). Contact your node provider or the 0g network documentation for the correct URL.
  ```python
  rpc_url = "https://your-rpc-url-here"
  ```

- **`private_keys`**: Replace the placeholder keys (`"0xYourPrivateKey1"`, `"0xYourPrivateKey2"`) with your actual private keys. Ensure each account has enough ETH (or native currency) to cover gas fees.
  ```python
  private_keys = [
      "0xYourActualPrivateKey1",
      "0xYourActualPrivateKey2",
      # Add more keys as needed
  ]
  ```

- **`to_address`**: The address of the 0g token ERC-20 contract. The default is:
  ```python
  to_address = "0x3eC8A8705bE1D5ca90066b37ba62c4183B024ebf"
  ```
  Verify this is the correct contract address for the 0g token on `chainId=16601`.

- **`spender_address`**: The address allowed to spend the 0g tokens via the `approve` function. The default is:
  ```python
  spender_address = "0xb95b5953ff8ee5d5d9818cdbefe363ff2191318c"
  ```
  Ensure this is the intended spender (e.g., a DEX or another contract).

- **`chain_id`**: Set to `16601` for the 0g network. Do not change unless you are targeting a different network.
  ```python
  chain_id = 16601
  ```

- **`gas_price_gwei`**: Base gas price in Gwei. The script uses the maximum of this value and the network’s current gas price.
  ```python
  gas_price_gwei = 5
  ```

**Security Warning**: Storing private keys directly in the script is insecure. Do not share `swap.py` or push it to a public repository with real private keys. Use this approach only in a secure environment. For production, consider environment variables or a secrets manager.

## Usage

1. **Verify Configuration**:
   - Ensure the `rpc_url` is valid and connects to a node supporting the 0g network (`chainId=16601`).
   - Confirm that `to_address` is the correct 0g token contract address.
   - Verify that each private key corresponds to an account with sufficient ETH (or native currency) for gas fees.
   - Ensure the `spender_address` is correct for your use case (e.g., a decentralized exchange or other contract).

2. **Run the Script**:
   Execute the script using Python:
   ```bash
   python swap.py
   ```

3. **What the Script Does**:
   - Randomly selects a private key from the `private_keys` list to generate a sender address.
   - Creates an `approve` transaction for a random amount of 0g tokens (0.01–0.1 tokens).
   - Dynamically estimates gas using `web3.eth.estimate_gas`.
   - Uses the higher of the specified `gas_price_gwei` or the network’s current gas price.
   - Signs and sends the transaction.
   - Waits for transaction confirmation (up to 120 seconds).
   - Prints transaction details (hash, sender address, token amount, and status).
   - Pauses for a random delay (1–10 minutes) before sending the next transaction.

4. **Example Output**:
   ```
   Відправлено: 0x123...abc | 0xSenderAddress | 0.05234 токенів
   Транзакція 0x123...abc успішна
   Чекаю 342 секунд...
   ```

## Troubleshooting

- **Connection Error**: If you see `"Не вдалося підключитися до ноди"`, verify your `rpc_url` and ensure the node supports `chainId=16601`. Check the 0g network documentation for a valid RPC endpoint.
- **Insufficient Balance**: If an account lacks ETH (or native currency) for gas, the script skips it and prints `"Недостатній баланс на <address>"`. Fund the account with sufficient ETH.
- **Gas Estimation Error**: Ensure `to_address` is a valid ERC-20 contract for the 0g token and that the `approve` function is accessible. Verify the contract address.
- **Transaction Failure**: Check for network congestion, incorrect contract addresses, or insufficient gas. Try increasing `gas_price_gwei` if transactions are stuck.
- **Token Decimals**: The script assumes the 0g token uses 18 decimals (standard for ERC-20). If the 0g token uses a different number of decimals, adjust the `amount_wei` calculation in the script (e.g., `int(amount_tokens * 10**<decimals>)`).

## Notes

- **Token Balance**: The script does not check the 0g token balance of the sender accounts. Ensure each account has sufficient 0g tokens if the contract requires it for the `approve` function.
- **Network**: The 0g network (`chainId=16601`) is non-standard. Confirm that your node supports this chain and that the contract addresses are correct.
- **Timeout**: For slow networks, you may need to increase the `timeout` in `wait_for_transaction_receipt` (currently 120 seconds).
- **PoA Middleware**: The script includes `geth_poa_middleware` for Proof of Authority networks. If the 0g network does not use PoA, comment out this line:
  ```python
  w3.middleware_onion.inject(geth_poa_middleware, layer=0)
  ```

## Contributing

Feel free to submit issues or pull requests to improve the script. For feature requests (e.g., token balance checks, retry logic, or logging to a file), open an issue at [https://github.com/lenav3/0g](https://github.com/lenav3/0g).

## License

This project is licensed under the MIT License. See the `LICENSE` file in the repository for details.

**Warning**: Use this script at your own risk. Verify all addresses and test in a safe environment (e.g., a testnet, if available) before using real funds or tokens. Never share private keys publicly.
