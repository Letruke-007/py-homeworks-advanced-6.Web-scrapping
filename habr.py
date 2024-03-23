import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

# Список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Создаем генератор заголовков с данными о пользователе (ОС, браузер и т.п.)
headers_generator = Headers(os='win', browser='chrome')

# Парсим данные статей с главной страницы Хабра
response = requests.get('https://habr.com/ru/articles', headers=headers_generator.generate())
main_html_data = response.text
main_soup = BeautifulSoup(main_html_data, 'lxml')

# Находим сами статьи, создаем список для добавления нужных данных впоследствии
article_list = main_soup.find('div', class_='tm-articles-list')
articles = article_list.find_all('article')
articles_data = []

# Итерируемся по списку статей, вытаскиваем и очищаем данные об имени пользователя, ссылке на статью, заголовок и текст статьи, дату ее создания
for article_tag in articles:
    user_name_tag = article_tag.find('a', class_='tm-user-info__username')
    if user_name_tag:
        user_name = user_name_tag.text.strip()
    else:
        user_name = None
    time_tag = article_tag.find('time')
    date_time = time_tag['datetime']

    article_link_tag = article_tag.find('a', class_='tm-title__link')
    link_relative = article_link_tag['href']
    link_absolute = f'https://habr.com{link_relative}'
    title = article_link_tag.text.strip()
    response = requests.get(url=link_absolute, headers=headers_generator.generate())
    article_html_data = response.text

    article_soup = BeautifulSoup(article_html_data, 'lxml')

    article_body_tag = article_soup.find(id='post-content-body')
    if article_body_tag:
        article_text = article_body_tag.text.strip()
    else:
        article_text = None

    # Прописываем необходимые связи (если в тексте статьи есть заданные ключевые слова, она добавляется в итоговый
    # список статей, отвечающих условиям запроса)
    for tag in KEYWORDS:
        if tag in article_text:
            articles_data.append({
            'user_name': user_name,
            'date_time': date_time,
            'link': link_absolute,
            'title': title,
            'article_text': article_text,
            })
# Выводим на печать время публикации статьи, ее заголовок и ссылку на нее. Можно еще имя пользователя добавить и текст
# статьи, если нужно (они есть в результирующем списке)

for articles in articles_data:
    print('_____________________________________________________________________')
    print(articles['date_time'])
    print(articles['title'])
    print(articles['link'])
