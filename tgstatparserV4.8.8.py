import sys
import random
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QComboBox, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My PyQt Widget")

        # Выпадающее меню режима
        self.mode = 'каналы и чаты'
        self.mode_box = QComboBox()
        self.modes = ['каналы и чаты', 'каналы', 'чаты']
        for mode in self.modes:
            self.mode_box.addItem(mode)
        self.mode_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.mode_box.setMinimumWidth(150)

        # конфигурация
        self.categories = {
            'Блоги': '/blogs',
            'Новости и СМИ': '/news',
            'Юмор и развлечения': '/entertainment',
            'Технологии': '/tech',
            'Экономика': '/economics',
            'Бизнес и стартапы': '/business',
            'Криптовалюты': '/crypto',
            'Путешествия': '/travels',
            'Маркетинг, PR, реклама': '/marketing',
            'Психология': '/psychology',
            'Дизайн': '/design',
            'Политика': '/politics',
            'Искусство': '/art',
            'Право': '/law',
            'Образование': '/education',
            'Книги': '/books',
            'Лингвистика': '/language',
            'Карьера': '/career',
            'Познавательное': '/edutainment',
            'Курсы и гайды': '/courses',
            'Спорт': '/sport',
            'Мода и красота': '/beauty',
            'Медицина': '/medicine',
            'Здоровье и Фитнес': '/health',
            'Картинки и фото': '/pics',
            'Софт и приложения': '/apps',
            'Видео и фильмы': '/video',
            'Музыка': '/music',
            'Игры': '/games',
            'Еда и кулинария': '/food',
            'Цитаты': '/quotes',
            'Рукоделие': '/handmade',
            'Семья и дети': '/babies',
            'Природа': '/nature',
            'Интерьер и строительство': '/construction',
            'Telegram': '/telegram',
            'Инстаграм': '/instagram',
            'Продажи': '/sales',
            'Транспорт': '/transport',
            'Религия': '/religion',
            'Эзотерика': '/esoterics',
            'Даркнет': '/darknet',
            'Букмекерство': '/gambling',
            'Шок-контент': '/shock',
            'Эротика': '/erotica',
            'Для взрослых': '/adult',
            'Другое': '/other'}

        self.base_url = "https://tgstat.ru"

        # Выпадающее меню категории
        self.combo_box = QComboBox()
        for key in self.categories.keys():
            self.combo_box.addItem(f"{key}")
        self.combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.combo_box.setMinimumWidth(150)

        # Кнопка для выпадающего меню
        self.mode_button = QPushButton("выбрать режим")

        # Кнопка для выпадающего меню
        self.combo_button = QPushButton("парсинг выбранной категории")

        # Поле ввода
        self.input_field = QLineEdit()

        # Кнопка для поля ввода
        self.input_button = QPushButton("парсинг заданной ссылки")

        # Вертикальная компоновка для меню и поля
        vbox = QVBoxLayout()

        # Горизонтальная компоновка для выпадающего меню режима
        mode_combo = QHBoxLayout()
        mode_combo.addWidget(self.mode_box)
        mode_combo.addWidget(self.mode_button)

        # Горизонтальная компоновка для выпадающего меню и кнопки категории
        hbox_combo = QHBoxLayout()
        hbox_combo.addWidget(self.combo_box)
        hbox_combo.addWidget(self.combo_button)

        # Горизонтальная компоновка для поля ввода и кнопки ссылки
        hbox_input = QHBoxLayout()
        hbox_input.addWidget(self.input_field)
        hbox_input.addWidget(self.input_button)

        # текстовые поля
        self.mode_text = QLabel("выбор режима")
        self.mode_text.setStyleSheet("QLabel { font-size: 16px}")

        self.combo_text = QLabel("выбор категории")
        self.combo_text.setStyleSheet("QLabel { font-size: 16px}")

        self.input_text = QLabel("парсинг по ссылке")
        self.input_text.setStyleSheet("QLabel { font-size: 16px}")

        # Добавление компоновок в вертикальную компоновку
        vbox.addWidget(self.mode_text)
        vbox.addLayout(mode_combo)
        vbox.addWidget(self.combo_text)
        vbox.addLayout(hbox_combo)
        vbox.addWidget(self.input_text)
        vbox.addLayout(hbox_input)
        self.config_button = QPushButton("настройка браузера/первый вход")
        self.config_text = QLabel("на подключение аккаунта даётся 10 минут")
        vbox.addWidget(self.config_button)
        vbox.addWidget(self.config_text)

        self.filters_page_button = QPushButton("открыть страницу фильтров")
        self.filters_page_parsing_button = QPushButton("спарсить открытую страницу фильтров")
        vbox.addWidget(self.filters_page_button)
        vbox.addWidget(self.filters_page_parsing_button)


        # Установка вертикальной компоновки как основной
        self.setLayout(vbox)

        # Подключение сигналов к слотам
        self.mode_button.clicked.connect(self.mode_button_clicked)
        self.combo_button.clicked.connect(self.combo_button_clicked)
        self.input_button.clicked.connect(self.input_button_clicked)
        self.config_button.clicked.connect(self.config_button_clicked)

        self.filters_page_button.clicked.connect(self.openFiltersPage)
        self.filters_page_parsing_button.clicked.connect(self.parseFiltersPage)

        # настройка селениум
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--allow-profiles-outside-user-dir')
        self.options.add_argument('--enable-profile-shortcut-manager')
        user_data_dir = r'C:\Users\nwsk\AppData\Local\Google\Chrome\User Data'
        profile_directory = 'Default'
        self.options.add_argument(f'user-data-dir={user_data_dir}')
        self.options.add_argument(f'profile-directory={profile_directory}')

        # создаём общий элемент драйвера, который будем использовать
        self.driver = None

    def config_button_clicked(self):
        self.parsing(self.base_url, 'настройка')

    def mode_button_clicked(self):
        self.mode = self.mode_box.currentText()

    def openFiltersPage(self):
        url = "https://tgstat.ru/channels/search"
        self.driver = webdriver.Chrome(executable_path=r'C:\\Users\\nwsk\\Desktop\\git\\nwsk_ru_stream\\model\\stream\\chromedriver.exe',options=self.options)
        self.driver.get(f'{url}')

    def parseFiltersPage(self):
        try:
            html = self.driver.page_source
            while True:
                try:
                    button = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Показать больше')]"))
                    )

                    # Нажать кнопку
                    time.sleep(random.randint(1, 3))
                    button.click()
                except Exception as e:
                    print(e)
                    break

            html = self.driver.page_source
            self.driver.quit()
            self.driver = None
            # Парсить HTML с помощью BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Извлечь все ссылки
            links = soup.find_all("a", href=lambda href: href and (f"https://tgstat.ru/channel/" or f"https://tgstat.ru/chat/") in href, target="_blank")
            date = str(datetime.datetime.now().strftime(format="%m-%d-%M-%S"))
            with open(f'Filtered{date}.txt', 'w') as file:
                for link in links:
                    link = link.get("href")
                    link = link.split("/")[-2]
                    link = str(link).replace("@", "", 1)
                    file.write(f"{link}\n")


        except Exception as e:
            self.driver.quit()
            self.driver = None
            print("ERROR")
            print(e)


    def parse_channels(self, url):
        try:
            while True:
                try:
                    button = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Показать больше')]"))
                    )

                    # Нажать кнопку
                    time.sleep(random.randint(1, 3))
                    button.click()
                    html = self.driver.page_source
                except:
                    break
            # Ожидание загрузки новой информации
            time.sleep(6)

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
            date = str(datetime.datetime.now().strftime(format="%m-%d-%M-%S"))
            with open(f'{url.split("/")[-1]}OpenChannels{date}.txt', 'w') as file:
                for link in ChanelOpenLinks:
                    link = link.split("/")[-1]
                    link = str(link).replace("@", "", 1)
                    file.write(f"{link}\n")
            with open(f'{url.split("/")[-1]}CloseChannels{date}.txt', 'w') as file:
                for link in ChanelCloseLinks:
                    file.write(f"{link}\n")

            # Получить HTML обновленной страницы
            self.driver.quit()
            self.driver = None

        except Exception as e:
            self.driver.quit()
            self.driver = None
            print(e)
            print("ERROR")
            return "ошибка парснига"

    def parse_groups(self, url):
        try:
            try:
                input_element = self.driver.find_element(By.ID, "peer_type_chat")
                self.driver.execute_script("arguments[0].click();", input_element)
            except:
                pass
            while True:
                try:
                    button = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Показать больше')]"))
                    )

                    # Нажать кнопку
                    time.sleep(random.randint(1, 3))
                    button.click()
                    html = self.driver.page_source
                except:
                    break

                # Нажать кнопку
                time.sleep(random.randint(1, 3))

            self.driver.quit()
            self.driver = None

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
            date = str(datetime.datetime.now().strftime(format="%m-%d-%M-%S"))
            with open(f'{url.split("/")[-1]}OpenChats{date}.txt', 'w') as file:
                for link in ChatOpenLinks:
                    link = link.split("/")[-1]
                    link = str(link).replace("@", "", 1)
                    file.write(f"{link}\n")
            with open(f'{url.split("/")[-1]}CloseChats{date}.txt', 'w') as file:
                for link in ChatCloseLinks:
                    file.write(f"{link}\n")

        except Exception as e:
            self.driver.quit()
            self.driver = None
            print(e)
            print("ERROR")
            return "ошибка парсинга"

    def parsing(self, url, mode):
        try:
            self.driver = webdriver.Chrome(executable_path=r'C:\\Users\\nwsk\\Desktop\\git\\nwsk_ru_stream\\model\\stream\\chromedriver.exe',
                                options=self.options)
            self.driver.get(f'{url}')

            if mode == 'каналы и чаты':
                self.parse_channels(url)
                self.parse_groups(url)
            elif mode == 'каналы':
                self.parse_channels(url)
            elif mode == 'чаты':
                self.parse_groups(url)
            elif mode == 'настройка':
                try:
                    try:
                        while True:
                            time.sleep(1)
                            # Проверяем, доступен ли веб-драйвер
                            self.driver.title
                    except Exception as e:
                        print("Браузер закрыт")
                    self.driver.quit()
                except:
                    self.driver.quit()
            else:
                self.driver.quit()
                return 'error'
        except Exception as e:
            return e

    def combo_button_clicked(self):
        # "Кнопка выпадающего меню нажата!"
        selected_item = self.combo_box.currentText()
        add_url = self.categories[selected_item]
        url = self.base_url + add_url
        mode = self.mode
        self.parsing(url, mode)

    def input_button_clicked(self):
        # "Кнопка поля ввода нажата!"
        url = self.input_field.text()
        mode = self.mode
        self.parsing(url, mode)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())