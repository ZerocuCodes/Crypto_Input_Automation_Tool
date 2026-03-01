# Crypto Address Auto-Input Helper

A Python automation tool that automatically copies cryptocurrency addresses to clipboard when withdrawal commands are detected. Supports multiple monitoring methods and crypto platforms.

## Features

- **Multiple Monitoring Methods**:
  - Clipboard Monitor: Detects withdrawal commands in clipboard content
  - Discord API Bot: Monitors Discord messages for withdrawal commands
  - Keyboard Monitor: Real-time keyboard input detection

- **Supported Platforms**:
  - Stake.us
  - Shuffle.us  
  - StakeStats.com

- **Supported Cryptocurrencies**:
  - Litecoin (LTC)
  - Bitcoin (BTC)
  - Solana (SOL)
  - XRP (with destination tag support)
  - Tron (TRX)
  - Polygon (POL)
  - Ethereum (ETH)
  - SOL/USDC

## Installation

1. Install required dependencies:

```bash
pip install discord.py pyperclip keyboard
```

1. Download the script to your desired location

## Configuration

### 1. Set Your Crypto Addresses

Edit the `SITE_ADDRESSES` dictionary in the script and replace the placeholder values:

```python
SITE_ADDRESSES = {
    'stake.us': {
        'ltc': 'YOUR_LTC_ADDRESS_HERE',
        'btc': 'YOUR_BTC_ADDRESS_HERE',
        'sol': 'YOUR_SOL_ADDRESS_HERE',
        # ... other currencies
    }
}
```

### 2. Discord Bot Setup (Optional)

If using the Discord API method, replace the placeholder token:

```python
TOKEN = 'your_actual_discord_token_here'
```

## Usage

Run the script and choose your preferred monitoring method:

```bash
python Auto-Input_Crypto_Addresses.py
```

### Method 1: Clipboard Monitor

- Monitors clipboard content for "withdraw [currency]" commands
- Automatically copies the corresponding address to clipboard
- Useful for automated workflows

### Method 2: Discord API Bot

- Creates a Discord self-bot that monitors your own messages
- Detects withdrawal commands in Discord chat
- Requires Discord token setup

### Method 3: Keyboard Monitor (Recommended)

- Real-time keyboard input detection
- Most responsive method
- Special XRP handling with automatic destination tag copying
- Press `Ctrl+Shift+Q` to stop the monitor

## How It Works

1. **Detection**: The script monitors for patterns like "withdraw btc", "withdraw ltc", etc.
2. **Matching**: When a withdrawal command is detected, it matches the currency to your configured address
3. **Auto-copy**: The corresponding crypto address is automatically copied to clipboard
4. **XRP Special Handling**: For XRP withdrawals, the address is copied first, then after pressing Enter, the destination tag is automatically copied

## Example Workflow

1. Run the script and select "Keyboard Monitor"
2. Choose your crypto platform (e.g., "stake.us")
3. Type "withdraw btc" in any application
4. The script automatically copies your BTC address to clipboard
5. Paste the address where needed
6. For XRP: After pasting the address and pressing Enter, the destination tag is automatically copied

## Security Notes

- Keep your Discord token secure and never share it
- Store your crypto addresses securely in the script
- The script only runs locally and doesn't transmit data externally
- Consider using environment variables for sensitive data in production

## Troubleshooting

- **Keyboard Monitor Issues**: May require administrator privileges on some systems
- **Discord Bot Issues**: Ensure Discord API permissions are correct
- **Clipboard Issues**: Some security software may interfere with clipboard access

## Requirements

- Python 3.7+
- discord.py
- pyperclip
- keyboard (for keyboard monitoring method)
- Windows OS (recommended for keyboard monitoring)

## License

This project is provided as-is for educational and personal use. Use responsibly and at your own risk.
