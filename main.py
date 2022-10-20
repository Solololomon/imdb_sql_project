import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import sqlite3

print('Welcome to the IMDb Film Scraper\n'
      'This script will return information on up to 40 films based on the '
      'range of years and ratings you specify, sorted by popularity\n'
      'The films will be stored in a database called films.db\n'
      'Please fill in all the fields:')

while True:
    try:
        startyear = int(input('Start year of your search: '))
    except ValueError:
        print('Please enter a number')
        continue
    if startyear <= 2022 and 1900 <= startyear:
        break
    else:
        print('Please enter a date between 1900 and 2022')

while True:
    try:
        endyear = int(input('End year of your search: '))
    except ValueError:
        print('Please enter a number')
        continue
    if endyear <= 2022 and 1900 <= endyear:
        if endyear >= startyear:
            break
        else:
            print('End year must not be before the start year')
            continue
    else:
        print('Please enter a date between 1900 and 2022')

while True:
    try:
        minrat = float(input('Minimum rating to consider: '))
    except ValueError:
        print('Please enter a number')
        continue
    if minrat <= 10.0 and 1.0 <= minrat:
        break
    else:
        print('Please enter a number between 1.0 and 10.0')

while True:
    try:
        maxrat = float(input('Maximum rating to consider: '))
    except ValueError:
        print('Please enter a number')
        continue
    if maxrat <= 10.0 and 1.0 <= maxrat:
        if maxrat >= minrat:
            break
        else:
            print('Maximum rating must not be lower than minimum rating')
            continue
    else:
        print('Please enter a number between 1.0 and 10.0')

URL = f'https://www.imdb.com/search/title/?title=&title_type=feature&release_date={startyear}-01-01,{endyear}-12-31&user_rating={minrat},{maxrat}&num_votes=1000,&languages=en'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(class_='lister-list')

while True:
    try:
        film_elements = results.find_all(class_='lister-item-content')
        print()
        print('Films that match your specifications:')
        print()
        break
    except AttributeError:
        film_elements = []
        print()
        print('No results found')
        break

loops = 1
films = len(film_elements)
film_id = []
film_title = []
film_year = []
film_genre = []
film_rating = []
film_runtime = []
film_certificate = []
while films > 0:
    for film_element in film_elements:
        film_id.append(f'{loops}')
        title_element = film_element.find('a')
        film_title.append(f'{title_element.text.strip()}')
        year_element = film_element.find(class_='lister-item-year text-muted unbold')
        film_year.append(re.findall('\d+', year_element.text.strip()))
        genre_element = film_element.find(class_='genre')
        film_genre.append(f'{genre_element.text.strip()}')
        rating_element = film_element.find('strong')
        film_rating.append(f'{rating_element.text.strip()}')
        try:
            runtime_element = film_element.find(class_='runtime')
            film_runtime.append(f'{runtime_element.text.strip()}')
            pass
        except AttributeError:
            film_runtime.append('N/a')
        try:
            age_element = film_element.find(class_='certificate')
            film_certificate.append(f'{age_element.text.strip()}')
            pass
        except AttributeError:
            film_certificate.append('N/a')
        films -= 1
        loops += 1
        if loops == 41:
            break

    break

film_years = []
for i in film_year:
    for j in i:
        j.replace('[', '')
        j.replace(']', '')
        film_years.append(j)

features = {'film_id':film_id, 'title':film_title, 'year':film_years, 'genre':film_genre, 'rating':film_rating, 'runtime':film_runtime, 'certificate':film_certificate}
films = pd.DataFrame(features, columns = ['film_id', 'title', 'year','genre', 'rating', 'runtime', 'certificate'])

print(films.to_string(index=False))

conn = sqlite3.connect('films.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS films (film_id number, title text, year number, genre text, rating text, runtime text, certificate text)')
conn.commit()

films.to_sql('films', conn, if_exists='replace', index=False)
conn.commit()
conn.close()

