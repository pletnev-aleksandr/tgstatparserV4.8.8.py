import random


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import time
# Замените эту строку на ваш путь к браузерному драйверу
options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument(r'user-data-dir=\User')
options.add_argument('--profile-directory=Profile 1')

url = 'https://tgstat.ru/erotica'


def parse_channels(driver):
    try:
        while True:
            try:
                button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Показать больше')]"))
                )

                # Нажать кнопку
                time.sleep(random.randint(1, 3))
                button.click()
            except:
                break
        # Ожидание загрузки новой информации
        time.sleep(6)

        # Получить HTML обновленной страницы
        html = driver.page_source

        # Парсить HTML с помощью BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Извлечь нужные данные из обновленной страницы
        # ... например ...
        # Извлечь все ссылки
        chanelLinks = soup.find_all("a", href=lambda href: href and f"https://tgstat.ru/channel/" in href)
        # Вывод результата
        ChanelOpenLinks = []
        ChanelCloseLinks = []
        for link in chanelLinks:
            link = link.get("href")
            if "@" in link:
                ChanelOpenLinks.append(link)
            else:
                ChanelCloseLinks.append(link)

        with open(f'{url.split("/")[-1]}OpenChannels.txt', 'w') as file:
            for link in ChanelOpenLinks:
                link = link.split("/")[-1]
                file.write(f"{link}\n")
        with open(f'{url.split("/")[-1]}CloseChannels.txt', 'w') as file:
            for link in ChanelCloseLinks:
                file.write(f"{link}\n")

    except Exception as e:
        print(e)
        return "ошибка парснига"


def parse_groups(driver):
    try:
        try:
            input_element = driver.find_element(By.ID, "peer_type_chat")
            driver.execute_script("arguments[0].click();", input_element)
        except:
            pass
        while True:
            try:
                button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Показать больше')]"))
                )

                # Нажать кнопку
                time.sleep(random.randint(1, 3))
                button.click()
            except:
                break

            # Нажать кнопку
            time.sleep(random.randint(1, 3))

        html = driver.page_source
        driver.quit()

        # Парсить HTML с помощью BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Извлечь нужные данные из обновленной страницы
        # ... например ...
        # Извлечь все ссылки
        chatLinks = soup.find_all("a", href=lambda href: href and f"https://tgstat.ru/chat/" in href)
        # Вывод результата
        ChatOpenLinks = []
        ChatCloseLinks = []
        for link in chatLinks:
            link = link.get("href")
            if "@" in link:
                ChatOpenLinks.append(link)
            else:
                ChatCloseLinks.append(link)

        with open(f'{url.split("/")[-1]}OpenChats.txt', 'w') as file:
            for link in ChatOpenLinks:
                link = link.split("/")[-1]
                file.write(f"{link}\n")
        with open(f'{url.split("/")[-1]}CloseChats.txt', 'w') as file:
            for link in ChatCloseLinks:
                file.write(f"{link}\n")

    except Exception as e:
        print(e)
        return "ошибка парсинга"


def parse_page(url):
    with webdriver.Chrome(executable_path=r'C:\\Users\\nwsk\\Desktop\\git\\nwsk_ru_stream\\model\\stream\\chromedriver.exe',options=options) as driver:
        driver.get(f'{url}')
        # Найти кнопку "Показать больше"
        while True:
            try:
                button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Показать больше')]"))
                )

                # Нажать кнопку
                time.sleep(random.randint(1,3))
                button.click()
            except:
                break
        # Ожидание загрузки новой информации
        time.sleep(6)


        # Получить HTML обновленной страницы
        html = driver.page_source

        # Парсить HTML с помощью BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Извлечь нужные данные из обновленной страницы
        # ... например ...
        # Извлечь все ссылки
        chanelLinks = soup.find_all("a", href=lambda href: href and f"https://tgstat.ru/channel/" in href)
        # Вывод результата
        ChanelOpenLinks = []
        ChanelCloseLinks = []
        for link in chanelLinks:
            link = link.get("href")
            if "@" in link:
                ChanelOpenLinks.append(link)
            else:
                ChanelCloseLinks.append(link)

        try:
            input_element = driver.find_element(By.ID, "peer_type_chat")
            driver.execute_script("arguments[0].click();", input_element)
        except:
            pass
        while True:
            try:
                button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Показать больше')]"))
                )

                # Нажать кнопку
                time.sleep(random.randint(1, 3))
                button.click()
            except:
                break

            # Нажать кнопку
            time.sleep(random.randint(1, 3))

        html = driver.page_source
        driver.quit()

        # Парсить HTML с помощью BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        print(soup)

        # Извлечь нужные данные из обновленной страницы
        # ... например ...
        # Извлечь все ссылки
        chatLinks = soup.find_all("a", href=lambda href: href and f"https://tgstat.ru/chat/" in href)
        # Вывод результата
        ChatOpenLinks = []
        ChatCloseLinks = []
        for link in chatLinks:
            link = link.get("href")
            if "@" in link:
                ChatOpenLinks.append(link)
            else:
                ChatCloseLinks.append(link)


        with open (f'{url.split("/")[-1]}OpenChats.txt', 'w') as file:
            for link in ChatOpenLinks:
                link = link.split("/")[-1]
                file.write(f"{link}\n")
        with open (f'{url.split("/")[-1]}CloseChats.txt', 'w') as file:
            for link in ChatCloseLinks:
                file.write(f"{link}\n")

parse_page(url=url)
