import discord
import pyperclip
import asyncio
import re
import time
from collections import deque
from discord.ext import commands

# Configuration - Crypto addresses by site
SITE_ADDRESSES = {
    'stake.us': {
        'ltc': 'YOUR LTC',
        'litecoin': 'YOUR LTC',
        'btc': 'YOUR BTC',
        'bitcoin': 'YOUR BTC',
        'sol': 'YOUR SOL',
        'solana': 'YOUR SOL',
        'xrp': 'YOUR XRP',
        'solusdc': 'YOUR SOLUSDC',
        'trx': 'YOUR TRX',
        'tron': 'YOUR TRON',
        'xrp_tag': 'YOUR XRP TAG'
    },
    'shuffle.us': {
        'ltc': 'YOUR LTC',
        'litecoin': 'YOUR LTC',
        'sol': 'YOUR SOL',
        'solana': 'YOUR SOL',
        'xrp': 'YOUR XRP',
        'ripple': 'YOUR XRP',
        'solusdc': 'YOUR SOLUSDC',
        'trx': 'YOUR TRX',
        'tron': 'YOUR TRON',
        'pol': 'YOUR POL',
        'polygon': 'YOUR POL',
        'xrp_tag': 'YOUR XRP TAG'
    },
    'stakestats.com': {
        'ltc': 'YOUR LTC',
        'litecoin': 'YOUR LTC',
        'sol': 'YOUR SOL',
        'solana': 'YOUR SOL',
        'xrp': 'YOUR XRP',
        'btc': 'YOUR BTC',
        'bitcoin': 'YOUR BTC',
        'eth': 'YOUR ETH',
        'ethereum': 'YOUR ETH',
        'trx': 'YOUR TRX',
        'tron': 'YOUR TRON',
        'pol': 'YOUR POL',
        'polygon': 'YOUR POL',
        'xrp_tag': 'YOUR XRP TAG'
    }
    
    # Add more sites and addresses here if needed
    
}

# Global variables
current_site = None
current_addresses = {}
waiting_for_xrp_tag = False
last_xrp_time = 0

TOKEN = 'your_discord_token_here'

class CryptoAddressBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents, self_bot=True)

    async def on_ready(self):
        print(f'{self.user} is ready!')

    async def on_message(self, message):
        if message.author != self.user:
            return
        
        withdraw_pattern = r'withdraw\s+(\w+)'
        match = re.search(withdraw_pattern, message.content, re.IGNORECASE)
        
        if match:
            token = match.group(1).lower()
            if token in current_addresses:
                address = current_addresses[token]
                pyperclip.copy(address)
                print(f"Address for {token.upper()} copied!")

def clipboard_monitor():
    print(f"Clipboard Monitor - {current_site}")
    print("Available tokens:", ", ".join([k for k in current_addresses.keys() if not k.endswith('_tag')]))
    
    last_clipboard = ""
    
    try:
        while True:
            try:
                current_clipboard = pyperclip.paste()
                
                if current_clipboard != last_clipboard:
                    last_clipboard = current_clipboard
                    
                    withdraw_pattern = r'withdraw\s+(\w+)'
                    match = re.search(withdraw_pattern, current_clipboard, re.IGNORECASE)
                    
                    if match:
                        token = match.group(1).lower()
                        if token in current_addresses:
                            address = current_addresses[token]
                            pyperclip.copy(address)
                            print(f"Detected withdraw {token.upper()}")
                            print(f"Address copied: {address}")
                
                time.sleep(0.5)
                
            except Exception as e:
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("Script stopped.")

def keyboard_monitor():
    import keyboard
    
    global waiting_for_xrp_tag, last_xrp_time
    
    print(f"Keyboard Monitor - {current_site}")
    print("Available tokens:", ", ".join([k for k in current_addresses.keys() if not k.endswith('_tag')]))
    print("Press Ctrl+Shift+Q to stop")
    
    key_buffer = deque(maxlen=50)
    
    def process_buffer():
        global waiting_for_xrp_tag, last_xrp_time
        
        buffer_text = ''.join(key_buffer).lower()
        withdraw_pattern = r'withdraw\s+(\w+)'
        match = re.search(withdraw_pattern, buffer_text)
        
        if match:
            token = match.group(1).lower()
            if token in current_addresses:
                address = current_addresses[token]
                pyperclip.copy(address)
                key_buffer.clear()
                
                print(f"Detected: withdraw {token.upper()}")
                print(f"Address copied: {address}")
                
                if token in ['xrp', 'ripple']:
                    waiting_for_xrp_tag = True
                    last_xrp_time = time.time()
                    xrp_tag = current_addresses.get('xrp_tag', '')
                    print(f"XRP detected! Destination tag will be copied next: {xrp_tag}")
                    print("Step 1: Paste address and press Enter")
                else:
                    print("Paste (Ctrl+V) and press Enter")
                
                return True
        return False
    
    def handle_xrp_tag():
        global waiting_for_xrp_tag
        
        if waiting_for_xrp_tag:
            time.sleep(0.2)
            xrp_tag = current_addresses.get('xrp_tag', '')
            pyperclip.copy(xrp_tag)
            waiting_for_xrp_tag = False
            
            print(f"XRP tag copied: {xrp_tag}")
            print("Step 2: Paste tag and press Enter")
    
    def on_key_event(event):
        try:
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'space':
                    key_buffer.append(' ')
                elif event.name == 'backspace':
                    if key_buffer:
                        key_buffer.pop()
                elif event.name == 'enter':
                    if waiting_for_xrp_tag and (time.time() - last_xrp_time < 30):
                        handle_xrp_tag()
                    else:
                        process_buffer()
                        key_buffer.clear()
                elif len(event.name) == 1:
                    key_buffer.append(event.name.lower())
                elif event.name in ['shift', 'ctrl', 'alt']:
                    pass
                else:
                    special_chars = {
                        'minus': '-', 'period': '.', 'comma': ',',
                        'semicolon': ';', 'apostrophe': "'", 'grave': '`',
                        'slash': '/', 'backslash': '\\', 'left_bracket': '[',
                        'right_bracket': ']', 'equal': '='
                    }
                    if event.name in special_chars:
                        key_buffer.append(special_chars[event.name])
        except Exception as e:
            pass
    
    def stop_script():
        print("Script stopped")
        keyboard.unhook_all()
        exit()
    
    keyboard.add_hotkey('ctrl+shift+q', stop_script)
    keyboard.on_press(on_key_event)
    
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("Script stopped.")
        keyboard.unhook_all()

def select_site():
    print("Select site:")
    print("1. stake.us")
    print("2. shuffle.us")
    print("3. stakestats.com")
    
    site_choice = input("Enter choice (1-3): ").strip()
    
    if site_choice == "1":
        return "stake.us", SITE_ADDRESSES['stake.us']
    elif site_choice == "2":
        return "shuffle.us", SITE_ADDRESSES['shuffle.us']
    elif site_choice == "3":
        return "stakestats.com", SITE_ADDRESSES['stakestats.com']
    else:
        print("Invalid choice")
        return None, None

if __name__ == "__main__":
    print("Crypto Address Helper")
    print("1. Clipboard Monitor")
    print("2. Discord API Bot")
    print("3. Keyboard Monitor")
    
    method_choice = input("Select method (1-3): ").strip()
    
    if method_choice == "3":
        current_site, current_addresses = select_site()
        if current_site is None:
            exit()
        
        print(f"\nSelected: {current_site}")
        keyboard_monitor()
    
    elif method_choice == "1":
        current_site, current_addresses = select_site()
        if current_site is None:
            exit()
            
        print(f"\nSelected: {current_site}")
        clipboard_monitor()
    
    elif method_choice == "2":
        current_site, current_addresses = select_site()
        if current_site is None:
            exit()
            
        if TOKEN == 'your_discord_token_here':
            print("Set Discord token first!")
        else:
            print(f"\nSelected: {current_site}")
            bot = CryptoAddressBot()
            bot.run(TOKEN)
    else:
        print("Invalid choice")