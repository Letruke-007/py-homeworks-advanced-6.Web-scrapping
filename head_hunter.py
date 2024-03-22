import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

# Создаем функцию записи полученных в ходе парсинга данных в json файл
def json_write(data):
    with open('search_result.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        print(json_str)

# Определяем списки ключевых слов, городов и пустой список данных для загрузки в последующем в json
keywords = ['Django', 'Flask']
cities = ['Москва', 'Санкт-Петербург']
data_list = []

# Создаем генератор заголовков с данными о пользователе (ОС, браузер и т.п.)
headers_generator = Headers(os='win', browser='chrome')

# Получаем данные с сайта hh.ru (адрес ссылки учитывает настройки городов и тег Python)

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_generator.generate())

# Получаем перечень вакансий
main_html_data = response.text
main_soup = BeautifulSoup(main_html_data, 'lxml')
vacancies_list = main_soup.find('div', id='a11y-main-content')
vacancies = vacancies_list.find_all('div', class_='vacancy-serp-item__layout')

# Итерируемся по перечню вакансий, определяем и чистим данные для загрузки в список data_list
for vacancy in vacancies:
    title_tag = vacancy.find('span', class_='serp-item__title-link serp-item__title')
    title = title_tag.text

    vacancy_link_tag = vacancy.find('a', class_='bloko-link')
    link = vacancy_link_tag['href']

    address_tag = vacancy.find('div', class_='vacancy-serp-item-body__main-info').text
    for city in cities:
        if city in address_tag:
            address = city
        else:
            pass

    # Получаем недостающие данные из текстов размещенных вакансий, а не preview
    response = requests.get(url=link, headers=headers_generator.generate())
    vacancy_data = response.text

    vacancy_soup = BeautifulSoup(vacancy_data, 'lxml')

    description_tag = vacancy_soup.find('div', class_='g-user-content')
    description = description_tag.text

    salary_tag = vacancy_soup.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite')
    salary = salary_tag.text

    # Очищаем данные о ЗП для записи в список (без сплита и джоина неверно распознаются), предусматриваем проверку на предмет отсутствия данных о ЗП
    if '₽' in salary:
        salary = salary.split()
        salary = ' '.join(salary)
    else:
        salary = 'ЗП не указана'

    employee_tag = vacancy_soup.find('span', class_='vacancy-company-name')
    employee = employee_tag.text

    # Проверяем полученные данные на предмет наличия заданных ключевых слов в тексте объявления, при наличии - записываем данные в список data_list
    for keyword in keywords:
        if keyword in description:
            data = {
                'link': link,
                'salary': salary,
                'employee': employee,
                'address': address
            }
            data_list.append(data)

# Записываем полученный список data_list в файл JSON
json_write(data_list)



