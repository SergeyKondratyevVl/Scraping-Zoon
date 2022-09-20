import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
import datetime
from categories import categories, cities


def get_source_html(url):

    category = url.split('/')[-2]
    city = url.split('/')[-3]
    print(city)

    driver = webdriver.Chrome(
        executable_path='chromedriver.exe'
    )
    # driver.maximize_window()
    
    if not os.path.exists(f'data/{city}'):
        os.mkdir(f'data/{city}')
    elif not os.path.exists(f'data/{city}/{category}'):
        os.mkdir(f'data/{city}/{category}')
    
    path_file = f'data/{city}/{category}/'

    try:
        driver.get(url=url)
        time.sleep(2)
        start = datetime.datetime.now()
        
        while True:
            find_more_element = driver.find_element(by=By.CLASS_NAME, value='catalog-button-showMore')
            with open(f'{path_file}{category}.html', 'w', encoding="utf-8") as file:
                    source = str(driver.page_source)
                    file.write(source)
            if driver.find_elements(by=By.CLASS_NAME, value="hasmore-text"):
                break
            else:
                actions = ActionChains(driver=driver)
                actions.move_to_element(find_more_element).perform()
                time.sleep(2)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    
    end = datetime.datetime.now()
    print(f'[INFO] Time Building {end-start}')
    
    return path_file, category

def get_items(file_path, category):

    with open(f'{file_path}{category}.html', encoding='utf-8') as file:
        src = file.read()
    
    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all('div', class_="minicard-item__info")

    items_category = []

    for item in items_divs:

        try:
            item_url = item.find("a", class_="title-link").get('href')
        except:
            item_url = 'Неизвестно'
        
        try:
            item_name = item.find('a', class_="title-link").text.strip()
        except:
            item_name = 'Неизвестно'
        
        try:
            item_tags = ', '.join(item.find('div', class_='minicard-item__features').text.strip().replace('\n', '').split('•'))

        except:
            item_tags = 'Неизвестно'
        
        try:
            item_ratings = item.find('span', class_='rating-value').text.replace(',', '.')
        except:
            item_ratings

        try:
            item_work_time = item.find('div', class_='minicard-item__work-time').text.strip()[1:].strip()
        except:
            item_work_time = 'Неизвестно'

        try:
            item_address = item.find('span', class_='address').text.strip()
        except:
            item_address = 'Неизвестно'

        try:
            item_metro = item.find('a', 'metro').text
        except:
            item_metro = 'Неизвестно'

        try:
            item_distance = item.find('span', 'distance').text.strip()
        except:
            item_distance = 'Неизвестно'

        try:
            item_comments = item.find('div', class_='comments').text.strip()
        except:
            item_comments = '0 отзывов'
        
        item_category = {
            'Url': item_url,
            'Name': item_name,
            'Address': item_address,
            'Work Time': item_work_time,
            'Metro': item_metro,
            'Distance': item_distance,
            'Tags': item_tags,
            'Rating': item_ratings,
            'Comments': item_comments
        }

        items_category.append(item_category)

    print(f'[INFO] Size of {category}: {len(items_category)} objects.\n')
    
    with open(f'{file_path}{category}.json', 'w', encoding='utf-8') as file:
        json.dump(items_category, file, ensure_ascii=False)
        

def main():
    for city in cities:
        for category_name in categories:
            try:
                file_path, category = get_source_html(url=f'https://zoon.ru/{city}/{category_name}/')
                get_items(file_path, category)
            except Exception as ex:
                print(ex)

if __name__ == '__main__':
    main()