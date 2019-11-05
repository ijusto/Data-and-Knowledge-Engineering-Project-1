# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib3.request
import requests
import re
import os

xml = open("people.xml", "w")

xml.write("<?xml version=\"1.0\"?>\n<people>\n")

number = 1

session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

session.execute("open moviesDB")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

input1 = "import module namespace movies = 'com.movies' at '" \
         + os.path.join(BASE_DIR,'app/data/queries/queries.xq') \
         + "';<actors>{movies:get_all_actors()}</actors>"
all_actors = session.query(input1)

input2 = "import module namespace movies = 'com.movies' at '" \
         + os.path.join(BASE_DIR,'app/data/queries/queries.xq') \
         + "';<directors>{movies:get_all_directors()}</directors>"

all_directors = session.query(input2)

'''
<name>
    <first_name>James</first_name>
    <last_name>Cameron</last_name>
</name>
'''

actors = all_actors.execute().replace("<first_name>",
                          "").replace("</first_name>",
                          " ").replace("<last_name>",
                          "").replace("</last_name>",
                          "").replace("\n",
                          "").replace("\r",
                          "").replace(" ",
                          "").replace("</name>",
                          "").split("<name>")
print(actors)
directors = all_directors.execute().replace("<first_name>",
                          "").replace("</first_name>",
                          " ").replace("<last_name>",
                          "").replace("</last_name>",
                          "").replace("\n",
                          "").replace("\r",
                          "").replace(" ",
                          "").replace("</name>",
                          "").split("<name>")
print(directors)
xml.write("<people>\n")
xml.write("\t<actors>\n")
for actor in actors:
    xml.write("\t\t<actor>\n")
    begin_query = "<links>{movies:get_imdb_link("
    end_query = ")}</links>"
    input3 = f'import module namespace movies = \'com.movies\' at \'' \
             f'{os.path.join(BASE_DIR, "app/data/queries/queries.xq")}\';' \
             f'{begin_query}{actor}{end_query}'
    actor_movie_links = session.query(input3)

    # <links><links><link>""</link></links></links>
    movie_link = actor_movie_links.execute().replace("<links>",
                                          "").replace("</links>",
                                          "").replace("\n",
                                          "").replace("\r",
                                          "").replace(" ",
                                          "").replace("</link>",
                                          "").split("<link>")[0]

    actor_page = (BeautifulSoup(requests.get
                                (movie_link).text, "html.parser").find
                                ('a', {'text': actor})['href'])

    actor_img = (BeautifulSoup(requests.get
                               (actor_page).text, "html.parser").find
                               ('img', {'id': 'name-poster'})['src'])

    see_full_bio_link = (BeautifulSoup(requests.get
                                      (actor_page).text, "html.parser").find
                                      ('span', {'class': 'see-more inline nobr-only'}).find
                                      ('a')['href'])

    born = (BeautifulSoup(requests.get
                                      (actor_page).text, "html.parser").find
                                      ('span', {'class': 'see-more inline nobr-only'}).find
                                      ('a')['href'])

    xml.write("\t\t</actor>\n")

    xml.write(actor_info)
    print("wrote actor: " + actor + " - " + number)
    number += 1

xml.write("\t</actors>\n")

xml.write("\t<directors>\n")
for director in directors:
    xml.write("\t\t<director>\n")
    begin_query = "<links>{movies:get_imdb_link("
    end_query = ")}</links>"
    input3 = f'import module namespace movies = \'com.movies\' at \'' \
             f'{os.path.join(BASE_DIR, "app/data/queries/queries.xq")}\';' \
             f'{begin_query}{director}{end_query}'
    director_movie_links = session.query(input3)

    # <links><links><link>""</link></links></links>
    movie_link = director_movie_links.execute().replace("<links>",
                                             "").replace("</links>",
                                             "").replace("\n",
                                             "").replace("\r",
                                             "").replace(" ",
                                             "").replace("</link>",
                                             "").split("<link>")[0]

    director_page = (BeautifulSoup(requests.get
                                (movie_link).text, "html.parser").find
                                ('div', {'class': 'plot_summary '}).find
                                ('div', {'class': 'credit_summary_item'}).find
                                ('a')['href'])

    director_img = (BeautifulSoup(requests.get
                                 (director_page).text, "html.parser").find
                                 ('img', {'id': 'name-poster'})['src'])

    director_story = (BeautifulSoup(requests.get
                                   (director_page).text, "html.parser").find
                                   ('div', {'class': ' name-trivia-bio-text'}).find
                                   ('div', {'class': ' inline'}).find
                                   ('img', {'id': 'name-poster'})['src'])

    xml.write("\t\t</director>\n")

    xml.write(director_info)
    print("wrote director: " + director + " - " + number)
    number += 1

xml.write("\t</directors>\n")
xml.write("</people>\n")
xml.close()

