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

user_agent = ["dog", "cat", "adfwd", "adidas", "main1", "main2", "adidas2", "main2", "main3", "adidas3", "main3",
              "main5", "adic"]
proxies = [{'http': '5.8.23.19:8000:X87TQ7:ohrENL'}, {'http': '5.8.20.19:8000:X87TQ7:ohrENL'}]
name_headrs = [{"User-Agent": "biba"}]


def main():
    while True:
        time_now = datetime.datetime.now()
        date_format = '%d.%m.%Y'
        year_now = time_now.year


        time.sleep(10)
        links_now, url_web_site = get_links()
        time.sleep(1)
        print(links_now)
        print(url_web_site)

        product = []

        ### Проверка на старые и новые сслыки
        with open("links_by_discord", "r") as f:
            file = f.read()
        for link in links_now:
            flag = 0
            file_links = file.split("\n")
            if link not in file_links:
                for link_now in product:
                    if link == link_now["link"]:
                        flag +=1
                if flag > 0:
                    continue
                try:
                    product.append(info_about_article(link))
                except Exception as e:
                    print(e)

        for final_info in product:
            day_drop = datetime.datetime.strptime(final_info["day"] + "." + str(year_now), date_format)
            if (day_drop - datetime.timedelta(days = 3) < time_now):
                print((day_drop - datetime.timedelta(days = 1)))
                discord(final_info)
                with open("links_by_discord", "a") as f:
                    f.write(final_info["link"] + "\n")


def info_about_article(link):
    info_about_articke = {}
    info_about_articke["picture"], info_about_articke["day"] = picture_and_time(link)
    product_id = get_product_id(link)
    info_about_articke["product_id"] = product_id
    info_about_articke["link"] = link
    data = requests.get(link, headers=random.choice(name_headrs), proxies=random.choice(proxies))
    info_about_articke["styleColor"] = data.text.split('","styleColor":"')[1].split('"},"')[0]
    soup = bs4.BeautifulSoup(data.text, "html.parser")
    stock = get_quantity(product_id, info_about_articke["styleColor"])
    info_about_articke["stock"] = stock
    info_about_articke["size"] = list(stock.keys())
    try:
        data1 = soup.find("aside")
        price = data1.div.div.div.string
        article = data1.div.div.h1.string
        article2 = data1.div.div.h5.string
        article += " " + article2
        info_about_articke["article"] = article
        if price is None:
            price = soup.find("div", {"data-qa": "price"}).text
        info_about_articke["price"] = price

        return info_about_articke
    except:
        print('2')
        exit(2)


def get_quantity(product_id, styleColor):
    sizes = {}
    url = "https://api.nike.com/deliver/available_gtins/v2/?filter=styleColor(" + styleColor + ")&filter=merchGroup(XP)"
    data = requests.get(url, headers=random.choice(name_headrs), proxies=random.choice(proxies))
    data = data.json()
    data = data["objects"]

    url2 = "https://api.nike.com/merch/skus/v2/?filter=productId(" + product_id + "),country(RU)"
    data2 = requests.get(url2, headers=random.choice(name_headrs), proxies=random.choice(proxies))
    data2 = data2.json()
    data2 = data2["objects"]

    for size in range(len(data)):
        sizes[data2[size]["nikeSize"]] = data[size]["level"]
    return sizes


def picture_and_time(link):
    options = Options()
    options.add_argument('--headless')
    session = webdriver.Firefox(options=options)
    session.get(link)
    time.sleep(0.5)
    data = session.find_elements_by_class_name('image-component')
    imageLink = data[0].get_attribute('src')
    data_time = session.find_element_by_class_name('available-date-component').text.split(" ")[1]
    session.close()
    return imageLink, data_time


def get_product_id(link):
    info_about_article = requests.get(link, headers=random.choice(name_headrs), proxies=random.choice(proxies)).text
    info_about_article = info_about_article.split('''"productId":"''')
    info_about_article = info_about_article[1].split('"')
    return info_about_article[0]


def get_links():
    url_mass = []
    links = []
    url_site = "https://www.nike.com/ru/launch?s=upcoming"
    data = requests.get(url_site, headers=random.choice(name_headrs), proxies=random.choice(proxies))
    data = bs4.BeautifulSoup(data.text, "html.parser")
    try:
        data = data.find("section", {"data-qa": "upcoming-section"}).findAll("figure")
        for i in data:
            fin_link = "https://www.nike.com" + i.find("a")["href"]
            fin_link = fin_link.split("?")[0]

            links.append(fin_link)
        links = list(dict.fromkeys(links))

        for i in data:
            url_kross = i.div.div
            if url_kross:
                url_kross = url_kross.a["href"]
                url_mass.append("https://www.nike.com" + url_kross)

        return links, url_mass
    except:
        print('1')
        exit(1)


def discord(final_info):
    time.sleep(5)
    russian_size_info = {"3.5": "34.5", "4": "35", "4.5": "35.5", "5": "36.5", "5.5": "37", "6": "37.5", "6.5": "38",
                         "7": "39", "7.5": "39.5",
                         "8": "40", "8.5": "41",
                         "9": "41.5", "9.5": "42",
                         "10": "43", "10.5": "43.5", "11": "44", "11.5": "44.5", "12": "45", "12.5": "46", "13": "46.5",
                         "13.5": "47", "14": "47.5", "15": "48.5", "16": "47.5", "17": "48.5", "18": "51.5",
                         "XXS": "XXS", "XS": "XS", "S": "S", "M": "M", "L": "L", "XL": "XL", "XXL": "XXL", "2XL": "2XL"}
    now = datetime.datetime.now()

    time_now = "[" + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + ":" + str(now.second).zfill(
        2) + "]"

    url = "https://discordapp.com/api/webhooks/718152621965312025/OxROXNzAGSLsAUeZztzzteF6b7_X_6y4VU8V46X7B07sIjHbcfZ_HY1EVl7y6URWqRoj"
    webhook = DiscordWebhook(url=url, content=' ')
    embed = DiscordEmbed(title="SNEAKERS BOT" + " " + time_now + " " + final_info["day"],
                         description=str(final_info["link"]), color=999900)
    embed.set_thumbnail(url=final_info["picture"])

    embed.add_embed_field(name=final_info["article"], value=final_info["price"],
                          inline=False)
    print(final_info)

    for i in range(len(final_info["size"])):
        size = final_info["size"][i]
        print(size, end='/')
        if size not in russian_size_info.keys():
            webhook = DiscordWebhook(url=url, content=' ')
            embed = DiscordEmbed(title="SNEAKERS BOT" + " " + time_now,
                                 description=str(final_info["link"]), color=999900)

            embed.add_embed_field(name=final_info["article"], value=final_info["price"],
                                  inline=False)

            webhook.add_embed(embed)
            time.sleep(10)
            response = webhook.execute()
            return

        final_link = "[" + size + "]" + "(" + final_info["link"] + "?" + "productId=" + str(
            final_info["product_id"]) + "&size=" + size + ")" + " US" + " - " + russian_size_info[size] + " RU"

        ### embed.set_thumbnail(url=info_ARTICLE["image"]
        if final_info["stock"][final_info["size"][i]] == "NA":
            final_info["stock"][final_info["size"][i]] = "LOW"
        embed.add_embed_field(name=final_info["stock"][final_info["size"][i]], value=final_link)
    webhook.add_embed(embed)
    response = webhook.execute()
    time.sleep(3)


if __name__ == '__main__':
    main()
