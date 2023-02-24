import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from sqlalchemy import inspect, create_engine
from sqlalchemy import event
import pandas as pd

movie_name = []
year = []
movie_rating = []
movie_genre = []
time = []
movie_metascore = []

movie_no=1
while movie_no <= 201:

    url = "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start="+str(movie_no)+"&ref_=adv_nxt"

    driver = Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(url)
    movie_no += 50
    result = driver.find_elements(By.CLASS_NAME, 'lister-item')
    for item in result:
        title = item.find_element(By.CLASS_NAME, 'lister-item-header').find_element(By.TAG_NAME, 'a').text
        movie_name.append(title)

        release_year = item.find_element(By.CLASS_NAME, 'lister-item-year').text.strip('()')
        year.append(release_year)

        rating = item.find_element(By.CLASS_NAME, 'ratings-bar').find_element(By.CLASS_NAME, 'inline-block').text
        movie_rating.append(rating)

        genre = item.find_element(By.CLASS_NAME, 'genre').text.strip()
        movie_genre.append(genre)

        movie_time = item.find_element(By.CLASS_NAME, 'runtime').text
        time.append(movie_time)
        
        try:
            metascore = item.find_element(By.CLASS_NAME, 'metascore').text.strip()
            movie_metascore.append(metascore)

        except:
            movie_metascore.append('N/A')
        
        print(title, release_year, rating, genre, movie_time, metascore)

driver.quit()

movie_DF = pd.DataFrame({'Title': movie_name, 'release_year': year, 'Movie_rating': movie_rating, 'Genre': movie_genre, 'Metascore': movie_metascore})

alchemy_driver = 'postgresql+psycopg2'
postgres_user = 'postgres'
postgres_password = '123456789'
postgres_host = '127.0.0.1'
postgres_db = 'imdb_data'
postgres_schema = 'public'


postgres_conn = create_engine(f'{alchemy_driver}://{postgres_user}:{postgres_password}@{postgres_host}:5432/{postgres_db}')
print("Postgres connection set")

movie_DF.to_sql(name='movie_sel', con=postgres_conn, schema=postgres_schema, if_exists='replace', index=False)
