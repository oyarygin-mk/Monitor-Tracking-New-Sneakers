import requests
import bs4
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import random
import json
from getmac import get_mac_address as gma
url = "https://www.nike.com/ru/launch/t/jordan-delta-mid-union-la-off-noir"
data = requests.get(url).text
data2 = data.split('","styleColor":"')[1].split('"},"')[0]
print(data2)

