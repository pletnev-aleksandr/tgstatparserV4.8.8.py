import csv
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime


# Function to parse a given link
def parse_link(link,driver):
    try:
        channel = {}
        driver.get('https://tgstat.ru/channel/@'+link)
        #soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract the channel name
        channel_name_element = soup.find('h1', class_="text-dark text-center text-sm-left overflow-hidden")
        channel['channel_name'] = channel_name_element.text.strip() if channel_name_element else 'No Channel Name'

        # Extract the number of subscribers
        subscribers_element = soup.select_one("h2.mb-1.text-dark")
        channel['subscribers'] = int(subscribers_element.text.replace(' ', '')) if subscribers_element else 0

        # Extract geo information
        geo_element = soup.find('div', class_="mt-4")
        if geo_element:
            # Extract and clean up the text
            geo_text = geo_element.get_text(separator=',').strip()
            geo_parts = [part.strip() for part in geo_text.split(',') if part.strip()]
            if len(geo_parts) >= 2:
                channel['geo_country'] = geo_parts[1]  # Россия
                channel['geo_language'] = geo_parts[2]  # Русский
            else:
                channel['geo_country'] = geo_parts[0] if len(geo_parts) > 0 else 'No Country'
                channel['geo_language'] = 'No Language'
        else:
            channel['geo_country'] = 'No Country'
            channel['geo_language'] = 'No Language'

        # Extract category text (fixed deprecation warning)
        category_header = next(
            (header for header in soup.find_all('h5', class_='mb-0') if 'Категория' in header.get_text(strip=True)),
            None)
        if category_header:
            link_element = category_header.find_next_sibling('a')
            channel['category_text']=(link_element.get_text(strip=True) if link_element else 'Ссылка не найдена')

        # The direct Telegram link
        channel['tglink'] = 'https://t.me/' + link

        # Check if comments are allowed
        comment_elements = soup.find_all(class_="uil-comments-alt")
        channel['commenting_allowed'] = len(comment_elements) > 0

        # Check if the channel is private (based on the URL structure)
        channel['private'] = '@' in driver.current_url

        # TODO достать колво лайков и колво просмотров. Но зачем???
        # Главное достать колво комментариев! По ним ориентироваться. Так как смысла нет оставлять комментария, там где меньше 4 !
        time.sleep(1)

        if channel['channel_name']=='No Channel Name':
            try:
                driver.find_element(By.XPATH,'//div[@class="mt-3"]/p[contains(@class, "lead") and text()="Канал не найден"]')
                channel['channel_name'] = 'wrong naming'
                channel['category_text'] = 'wrong naming'
                return channel

            except:
                print('we need to log in')
                print(1/0)


        return channel

        #return title
    except Exception as e:
        return f"Error parsing {link}: {e}"


# Function to check if a link has already been parsed
def is_link_parsed(link, parsed_links_file):
    if not os.path.exists(parsed_links_file):
        return False

    with open(parsed_links_file, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['link'] == link:
                return True
    return False


# Function to save parsing result
def save_parsing_result(link, result, parsed_links_file):
    fieldnames = ['link', 'channel_name', 'subscribers', 'geo_country','geo_language', 'category_text', 'tglink', 'commenting_allowed',
                  'private', 'date', 'error']
    file_exists = os.path.isfile(parsed_links_file)

    with open(parsed_links_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'link': link,
            'channel_name': result.get('channel_name', ''),
            'subscribers': result.get('subscribers', ''),
            'geo_country': result.get('geo_country', ''),
            'geo_language': result.get('geo_language', ''),
            'category_text': result.get('category_text', ''),
            'tglink': result.get('tglink', ''),
            'commenting_allowed': result.get('commenting_allowed', ''),
            'private': result.get('private', ''),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': result.get('error', '')
        })


# Main function to process the .txt file
def process_file(txt_file, parsed_links_file,driver):
    with open(txt_file, 'r') as file:
        for line in file:
            link = line.strip()

            if not link:
                continue

            if is_link_parsed(link, parsed_links_file):
                print(f"Skipping already parsed link: {link}")
                continue

            print(f"Parsing link: {link}")
            result = parse_link(link,driver)

            save_parsing_result(link, result, parsed_links_file)
            print(f"Saved result for: {link}")


# Example usage
txt_file = 'newsOpenChannels10-06-24-18.txt'  # Replace with your .txt file containing the links
parsed_links_file = 'parsed_links.csv'  # Replace with your desired CSV file path




if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    user_data_dir = r'C:\Users\nwsk\AppData\Local\Google\Chrome\User Data'
    profile_directory = 'Default'
    options.add_argument(f'user-data-dir={user_data_dir}')
    options.add_argument(f'profile-directory={profile_directory}')

    driver = uc.Chrome(
        executable_path=r'C:\\Users\\nwsk\\Desktop\\git\\nwsk_ru_stream\\model\\stream\\chromedriver.exe',
        use_subprocess=False,
        #options=options
    )

    auth = 'https://tgstat.ru/?at=znS8QNvgD549X8u6qZluWJDx7XgOjYru'
    driver.get(auth)
    process_file(txt_file, parsed_links_file,driver)

    # TODO добавить отслеживание последнего поста, чтобы не все скрэпить