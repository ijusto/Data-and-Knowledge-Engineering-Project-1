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

def new_movie(request):
    assert isinstance(request, HttpRequest)
    dict={
        "movies": {
            "movie" : {
                "@rating":"",
                "@budget":0,
                "@duration":"",
                "@country":"XXX",
                "title":{
                    "name":"",
                    "year":""
                },
                "imbd_info":{
                    "score":"?",
                },
                "cast": {
                    "main_actors" :{
                        "person" : []
                    }
                },
                "director" :"",
                "genres": {
                    "genre" : []
                }
            }}}

    if 'title' in request.POST:
        if request.POST['title']!="":
            dict['movies']['movie']['title']['name'] = request.POST['title']
    if 'year' in request.POST:
        if request.POST['year'] != "":
            dict['movies']['movie']['title']['year'] = request.POST['year']
    if 'first_name1' and 'last_name1' in request.POST:
        if request.POST['first_name1'] != "" and request.POST['last_name1']!="":
            dict["movies"]["movie"]['director'] = {
                "person" : {
                    "name" :{
                         "first_name" : request.POST['first_name1'],
                         "last_name" : request.POST['last_name1'],
                    }
                }
            }
    if 'first_name2' and 'last_name2' in request.POST:
        if request.POST['first_name2'] != "" and request.POST['last_name2']!="":
            dict["movies"]["movie"]['cast']['main_actors']['person'].append({
                                "name" :{
                                    "first_name" : request.POST['first_name2'],
                                    "last_name" : request.POST['last_name2'],
                                }
                            })
    if 'first_name3' and 'last_name3' in request.POST:
        if request.POST['first_name3'] != "" and request.POST['last_name3'] != "":
            dict["movies"]["movie"]['cast']['main_actors']['person'].append({
                                "name" :{
                                    "first_name" : request.POST['first_name3'],
                                    "last_name" : request.POST['last_name3'],
                                }
                            })
    if 'first_name4' and 'last_name4' in request.POST:
        if request.POST['first_name4'] != "" and request.POST['last_name4'] != "":
            dict["movies"]["movie"]['cast']['main_actors']['person'].append({
                                "name" :{
                                    "first_name" : request.POST['first_name4'],
                                    "last_name" : request.POST['last_name4'],
                                }
                            })
    if 'genre1' in request.POST:
        if request.POST['genre1'] != "":
            dict["movies"]["movie"]['genres']['genre'].append(request.POST['genre1'])
    if 'genre2' in request.POST:
        if request.POST['genre2'] != "":
            dict["movies"]["movie"]['genres']['genre'].append(request.POST['genre2'])
    if 'genre3' in request.POST:
        if request.POST['genre3'] != "":
            dict["movies"]["movie"]['genres']['genre'].append(request.POST['genre3'])
    if 'genre4' in request.POST:
        if request.POST['genre4'] != "":
            dict["movies"]["movie"]['genres']['genre'].append(request.POST['genre4'])
    if 'budget' in request.POST:
        if request.POST['budget'] != "":
            dict["movies"]["movie"]['@budget'] = request.POST['budget']
    if 'country' in request.POST:
        if request.POST['country'] != "":
            dict["movies"]["movie"]['@country'] = request.POST['country']
    if 'duration' in request.POST:
        if request.POST['duration'] != "":
            dict["movies"]["movie"]['@duration'] = request.POST['duration']
    if 'rating' in request.POST:
        if request.POST['rating'] != "":
            dict["movies"]["movie"]['@rating'] = request.POST['rating']

    xml_newmovie=xmltodict.unparse(dict, pretty=True)
    xsd_name = 'moviesSchema.xsd'
    xsd_file = os.path.join(BASE_DIR, 'app/data/' + xsd_name)

    tree = ET.fromstring(bytes(xml_newmovie,'utf-8'))
    xsd_parsed = ET.parse(xsd_file)

    xsd = ET.XMLSchema(xsd_parsed)

    if 'title' in request.POST:
        title = request.POST['title']
        year = request.POST['year']
        if xsd.validate(tree):
            session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

            session.execute("open moviesDB")
            xml_newmovie = xml_newmovie.replace("<?xml version=\"1.0\" encoding=\"utf-8\"?>", "")

            input1 = "import module namespace movies = 'com.movies' at '" \
                     + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
                     + "';movies:ins_movie(" + xml_newmovie + ")"

            query1 = session.query(input1)

            query1.execute()

            session.close()
            return show_movie(request,title)
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
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open moviesDB")

    input0 = "let $c := collection('moviesDB') return $c"

    query0 = session.query(input0)

    xml_result = query0.execute()
    xml_result = "<?xml version=\"1.0\"?>"+"\n\r" + xml_result

    xslt_name = 'movies.xsl'
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.fromstring(bytes(xml_result, "utf-8"))

    #xml_name = 'movies_short.xml'
    xslt_name = 'movies.xsl'

    #xml_file = os.path.join(BASE_DIR, 'app/data/' + xml_name)
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    #tree = ET.parse(xml_file)
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

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

    session.execute("open moviesDB")

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
    order = request.POST["orderby"]

    input4 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<movies>{movies:selected_filters(" + xml_query + ", <o>" + order + "</o>)}</movies>"
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

def apply_search(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open moviesDB")

    input1 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<genres>{movies:get_all_genres()}</genres>"
    query1 = session.query(input1)

    input2 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<ratings>{movies:get_all_ratings()}</ratings>"

    query2 = session.query(input2)

    input3 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
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

    input4 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<movies>{movies:dist_searcher(<s>" + request.POST['search'] + "</s>)}</movies>"

    query4 = session.query(input4)
    xml_result = query4.execute()
    xml_result = "<?xml version=\"1.0\"?>"+"\n\r" + xml_result

    xslt_name = 'movies.xsl'
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.fromstring(bytes(xml_result, "utf-8"))
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    tparams = {
        'content': newdoc,
        "genres": genres,
        "ratings": ratings,
        "years": years
    }
    return render(request,'index.html',tparams)

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

def directors_list(request):
    xml_name = 'movies.xml'
    xslt_name = 'directors.xsl'

    xml_file = os.path.join(BASE_DIR, 'app/data/' + xml_name)
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.parse(xml_file)
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    tparams = {
        'content': newdoc,
    }

    return render(request, 'directors.html', tparams)

# TODO: Not working
def show_movie(request, movie):
    print("movie: " + str(type(movie)))
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open moviesDB")

    input = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<movie>{movies:get_movie(" + "<name>" + movie + "</name>" + ")}</movie>"

    query = session.query(input).execute()
    dict = xmltodict.parse(query)

    # USING QUERY TO GET THE MOVIE CAST
    input = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<actors>{movies:get_movie_main_actors(" + "<name>" + movie + "</name>" + ")}</actors>"

    movie_main_actors = session.query(input).execute().replace("<actors>",
                                                      "").replace("</actors>",
                                                      "").replace("</actor>",
                                                      "").replace("\n",
                                                      "").replace("\r",
                                                      "").split("<actor>")
    for i in range(len(movie_main_actors[1:])+1):
        movie_main_actors[i] = movie_main_actors[i].strip().replace(" ","_")
        print(movie_main_actors[i])

    input = "import module namespace movies = 'com.movies' at '" \
            + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
            + "';<actors>{movies:get_movie_secondary_actors(" + "<name>" + movie + "</name>" + ")}</actors>"

    movie_secondary_actors = session.query(input).execute()

    if movie_secondary_actors == "<actors/>":
        movie_secondary_actors = [" "]
    else:
        movie_secondary_actors.replace("<actors>",
                                      "").replace("</actors>",
                                      "").replace("</actor>",
                                      "").replace("\n",
                                      "").replace("\r",
                                      "").split("<actor>")
        for i in range(len(movie_main_actors[1:]) + 1):
            movie_secondary_actors[i] = movie_secondary_actors[i].strip().replace(" ", "_")

    # USING QUERY TO GET THE MOVIE DIRECTOR
    input = "import module namespace movies = 'com.movies' at '" \
            + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
            + "';<director>{movies:get_movie_director_name(" + "<name>" + movie + "</name>" + ")}</director>"

    movie_director = session.query(input).execute().replace("<director>",
                                                  "").replace("</director>",
                                                  "").replace("\n",
                                                  "").replace("\r",
                                                  "")

    # USING QUERY TO GET THE MOVIE GENRES
    input = "import module namespace movies = 'com.movies' at '" \
            + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
            + "';<genres>{movies:get_movie_genres(" + "<name>" + movie + "</name>" + ")}</genres>"

    movie_genres = session.query(input).execute().replace("<genres>",
                                                "").replace("</genres>",
                                                "").replace("</genre>",
                                                "").replace("\n",
                                                "").replace("\r",
                                                "").split("<genre>")

    # USING QUERY TO GET THE MOVIE KEYWORDS
    input = "import module namespace movies = 'com.movies' at '" \
            + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
            + "';<keywords>{movies:get_movie_plot_keywords(" + "<name>" + movie + "</name>" + ")}</keywords>"

    plot_keywords = session.query(input).execute().replace("<keywords>",
                                                "").replace("</keywords>",
                                                "").replace("</keyword>",
                                                "").replace("\n",
                                                "").replace("\r",
                                                "").replace(" ",
                                                "").split("<keyword>")
    print("----"+str(movie_main_actors[1:])+"---")
    tparams = {
        'movie_name': dict['movie']['movie']['title']['name'],
        'movie_img': dict['movie']['movie']['poster'],
        'movie_year': dict['movie']['movie']['title']['year'],
        'movie_score': dict['movie']['movie']['imbd_info']['score']['#text'],
        'movie_main_actors': movie_main_actors[1:],
        'movie_secondary_actors': movie_secondary_actors[1:],
        'movie_director': movie_director,
        'movie_genres': movie_genres[1:],
        'movie_rating': dict['movie']['movie']['@rating'],
        'movie_language': dict['movie']['movie']['@language'],
        'movie_country': dict['movie']['movie']['@country'],
        'movie_duration': dict['movie']['movie']['@duration'],
        'movie_plot_keywords': plot_keywords[1:],
        'movie_budget': dict['movie']['movie']['@budget']
    }

    return render(request, 'movie_page.html', tparams)

def apply_search(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open moviesDB")

    input1 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<genres>{movies:get_all_genres()}</genres>"
    query1 = session.query(input1)

    input2 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<ratings>{movies:get_all_ratings()}</ratings>"

    query2 = session.query(input2)

    input3 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
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

    input4 = "import module namespace movies = 'com.movies' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
             + "';<movies>{movies:dist_searcher(<s>" + request.POST['search'] + "</s>)}</movies>"

    query4 = session.query(input4)
    xml_result = query4.execute()
    xml_result = "<?xml version=\"1.0\"?>"+"\n\r" + xml_result

    xslt_name = 'movies.xsl'
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.fromstring(bytes(xml_result, "utf-8"))
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    tparams = {
        'content': newdoc,
        "genres": genres,
        "ratings": ratings,
        "years": years
    }
    return render(request,'index.html',tparams)

def actor_profile(request, actor):
    fn_actor = actor.split("_")[0]
    print(fn_actor)
    ln_actor = actor.split("_")[1]
    print(ln_actor)
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open peopleDB")

    input_img = "import module namespace people = 'com.people' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/people_queries.xq') \
             + "';<movie>{people:get_img(" + "<name><first_name>" + fn_actor + "</first_name><last_name>"+ln_actor+"</last_name></name>" + ")}</movie>"

    input_bio = "import module namespace people = 'com.people' at '" \
                + os.path.join(BASE_DIR, 'app/data/queries/people_queries.xq') \
                + "';<movie>{people:get_bio(" + "<name><first_name>" + fn_actor + "</first_name><last_name>"+ln_actor+"</last_name></name>" + ")}</movie>"

    query_img = session.query(input_img).execute()
    print(query_img)
    if query_img == "<movie/>":
        query_img = "https://alumni.crg.eu/sites/default/files/default_images/default-picture_0_0.png"
    query_bio = session.query(input_bio).execute()
    if query_bio == "<movie/>":
        query_bio = "No bio found."
    print(query_bio)

    tparams = {
        'actor_img': query_img.replace("<img>","").replace("</img>", "").replace("<movie>","").replace("</movie>",""),
        'actor_bio': query_bio.replace("<bio>","").replace("</bio>", "").replace("<movie>","").replace("</movie>",""),
        'actor_name': fn_actor+" "+ln_actor
    }

    return render(request, 'actor_profile.html', tparams)

def director_profile(request, director):
    fn_director = director.split("_")[0]
    if len(director.split("_")) >= 2:
        ln_director = director.split("_")[1]
    else:
        ln_director = fn_director
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open peopleDB")

    input_img = "import module namespace people = 'com.people' at '" \
             + os.path.join(BASE_DIR, 'app/data/queries/people_queries.xq') \
             + "';<movie>{people:get_img(" + "<name><first_name>" + fn_director + "</first_name><last_name>"+ln_director+"</last_name></name>" + ")}</movie>"

    input_bio = "import module namespace people = 'com.people' at '" \
                + os.path.join(BASE_DIR, 'app/data/queries/people_queries.xq') \
                + "';<movie>{people:get_bio(" + "<name><first_name>" + fn_director + "</first_name><last_name>"+ln_director+"</last_name></name>" + ")}</movie>"

    query_img = session.query(input_img).execute()
    print(query_img)
    if query_img == "<movie/>":
        query_img = "https://alumni.crg.eu/sites/default/files/default_images/default-picture_0_0.png"
    query_bio = session.query(input_bio).execute()
    if query_bio == "<movie/>":
        query_bio = "No bio found."
    print(query_bio)

    if len(director.split("_")) >= 2:
        ln_director = director.split("_")[1]
    else:
        ln_director = ""

    tparams = {
        'director_img': query_img.replace("<img>","").replace("</img>", "").replace("<movie>","").replace("</movie>",""),
        'director_bio': query_bio.replace("<bio>","").replace("</bio>", "").replace("<movie>","").replace("</movie>",""),
        'director_name': fn_director+" "+ln_director
    }

    return render(request, 'director_profile.html', tparams)