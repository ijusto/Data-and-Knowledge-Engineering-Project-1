from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from webproj.settings import BASE_DIR
import os
import lxml.etree as ET
import xmltodict
from BaseXClient import BaseXClient
import requests

def index(request):
    return render(request, 'index.html')

def movies_list(request):
    xml_name = 'movies.xml'
    xslt_name = 'movies.xsl'

    xml_file = os.path.join(BASE_DIR, 'app/data/' + xml_name)
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.parse(xml_file)
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    tparams = {
         'content': newdoc,
     }
    return render(request, 'movies.html', tparams)

def new_movie(request):
    assert isinstance(request, HttpRequest)
    #MUDAR If para verificação xmlschema
    if 'title' in request.POST and 'year' in request.POST:
        title = request.POST['title']
        year = request.POST['year']
        if title and year:
            return render(
                request,
                'Auxiliar.html',
                {
                    'title': title,
                    'year' : year,
                }
            )
        else:
            return render(
                request,
                'newMovie.html',
                {
                    'error': True,
                }
            )
    else:
        return render(
            request,
            'newMovie.html',
            {
                'error': False,
            }
        )

def movies_news_feed(request):
    xml_link = "https://www.cinemablend.com/rss/topic/news/movies"
    xml_file = requests.get(xml_link)

    xslt_name = 'rss.xsl'
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.fromstring(xml_file.content)
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    tparams = {
        'content': newdoc,
    }

    return render(request, 'news.html', tparams)

def movies_feed(request):
    xml_name = 'movies_short.xml'
    xslt_name = 'movies.xsl'

    xml_file = os.path.join(BASE_DIR, 'app/data/' + xml_name)
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.parse(xml_file)
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open moviesDB_short")

    input1 = "import module namespace movies = 'com.movies' at '"\
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             +"';<genres>{movies:get_all_genres()}</genres>"

    query1 = session.query(input1)

    input2 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR,'app/data/queries/queries.xq') \
             + "';<ratings>{movies:get_all_ratings()}</ratings>"

    query2 = session.query(input2)

    input3 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR,'app/data/queries/queries.xq') \
             + "';<years>{movies:get_all_years()}</years>"

    query3 = session.query(input3)

    genres = query1.execute().replace("<genres>",
                          "").replace("</genres>",
                          "").replace("\n",
                          "").replace("\r",
                          "").replace(" ",
                          "").replace("</genre>",
                          "").split("<genre>")
    genres.remove('')

    ratings = query2.execute().replace("<ratings>",
                           "").replace("</ratings>",
                           "").replace("\n",
                           "").replace("\r",
                          "").replace(" ",
                           "").replace("</rating>",
                           "").split("<rating>")
    ratings.remove('')

    years = query3.execute().replace("<years>",
                         "").replace("</years>",
                         "").replace("\n",
                         "").replace("\r",
                         "").replace(" ",
                         "").replace("</year>",
                         "").split("<year>")
    years.remove('')

    session.close()

    tparams = {
        'content': newdoc,
        "genres": genres,
        "ratings": ratings,
        "years" : years
     }
    return render(request, 'index.html', tparams)

def apply_filters(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open moviesDB_short")

    input1 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR,'app/data/queries/queries.xq') \
             + "';<genres>{movies:get_all_genres()}</genres>"
    query1 = session.query(input1)

    input2 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR,'app/data/queries/queries.xq') \
             + "';<ratings>{movies:get_all_ratings()}</ratings>"

    query2 = session.query(input2)

    input3 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR,'app/data/queries/queries.xq') \
             + "';<years>{movies:get_all_years()}</years>"

    query3 = session.query(input3)

    genres = query1.execute().replace("<genres>",
                          "").replace("</genres>",
                          "").replace("\n",
                          "").replace("\r",
                          "").replace(" ",
                          "").replace("</genre>",
                          "").split("<genre>")
    genres.remove('')

    ratings = query2.execute().replace("<ratings>",
                           "").replace("</ratings>",
                           "").replace("\n",
                           "").replace("\r",
                           "").replace(" ",
                           "").replace("</rating>",
                           "").split("<rating>")
    ratings.remove('')

    years = query3.execute().replace("<years>",
                         "").replace("</years>",
                         "").replace("\n",
                         "").replace("\r",
                         "").replace(" ",
                         "").replace("</year>",
                         "").split("<year>")
    years.remove('')


    dict={"query": {"genres":{"genre":[""]}, "rating": "", "year":""}}
    for g in genres:
        if g in request.POST:
            if "" in dict["query"]["genres"]["genre"]:
                dict["query"]["genres"]["genre"].remove("")
            dict["query"]["genres"]["genre"].append(g)
    if 'ratings' in request.POST:
        dict["query"]["rating"] = request.POST['ratings']
    if 'years' in request.POST:
        dict["query"]["year"] = request.POST['years']
    xml_query = xmltodict.unparse(dict, pretty=True)
    xml_parts = xml_query.rpartition("?>")
    xml_query = xml_parts[2].lstrip()

    input4 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<movies>{movies:selected_filters(" + xml_query + ")}</movies>"
    query4 = session.query(input4)
    xml_result = query4.execute()
    xml_result = xml_parts[0] + xml_parts[1] + "\n\r" + xml_result

    xslt_name = 'movies.xsl'
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.fromstring(bytes(xml_result,"utf-8"))
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    tparams = {
        'content': newdoc,
        "genres": genres,
        "ratings": ratings,
        "years": years
    }
    return render(request, 'index.html', tparams)

def actors_list(request):
    xml_name = 'movies.xml'
    xslt_name = 'actors.xsl'

    xml_file = os.path.join(BASE_DIR, 'app/data/' + xml_name)
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.parse(xml_file)
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    tparams = {
        'content': newdoc,
    }

    return render(request, 'actors.html', tparams)

# TODO: Not working
def show_movie(request, movie):
    print("movie: " + str(type(movie)))
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open moviesDB")

    input1 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<genres>{movies:get_movie_genres(" + movie + ")}</genres>"

    query1 = session.query(input1)

    genres = query1.execute().replace("<genres>",
                          "").replace("</genres>",
                          "").replace("\n",
                          "").replace("\r",
                          "").replace(" ",
                          "").replace("</genre>",
                          "").split("<genre>")

    input2 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<main_actors>{movies:get_movie_main_actors(" + movie + ")}</main_actors>"

    query2 = session.query(input2)

    main_actors = query2.execute().replace("<main_actors>",
                          "").replace("</main_actors>",
                          "").replace("\n",
                          "").replace("\r",
                          "").replace(" ",
                          "").replace("</actor>",
                          "").split("<actor>")


    secondary_actors = []

    input4 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "'<director>{;movies:get_movie_director_name(" + movie + ")}</director>"

    query4 = session.query(input4)

    director = query4.execute().replace("<director>",
                          "").replace("</director>",
                          "").replace("\n",
                          "").replace("\r",
                          "").replace(" ","")
    tparams = {
        'genres': genres,
        'main_actors': main_actors,
        'secondary_actors': secondary_actors,
        'director': director
    }

    return render(request, 'movie_page.html', tparams)