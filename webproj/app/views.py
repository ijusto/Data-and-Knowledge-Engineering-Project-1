from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from webproj.settings import BASE_DIR
import os
import lxml.etree as ET
import xmltodict
from BaseXClient import BaseXClient
import re

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

def movies_feed(request):
    xml_name = 'movies.xml'
    xslt_name = 'movies.xsl'

    xml_file = os.path.join(BASE_DIR, 'app/data/' + xml_name)
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.parse(xml_file)
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open moviesDB")

    input1 = "import module namespace movies = 'com.movies' at '"+ os.path.join(BASE_DIR, 'app/data/queries/queries.xq') +"';<genres>{movies:get_all_genres()}</genres>"
    query1 = session.query(input1)

    input2 = "import module namespace movies = 'com.movies' at '" + os.path.join(BASE_DIR,
                                                                                 'app/data/queries/queries.xq') + "';<ratings>{movies:get_all_ratings()}</ratings>"
    query2 = session.query(input2)

    input3 = "import module namespace movies = 'com.movies' at '" + os.path.join(BASE_DIR,
                                                                                 'app/data/queries/queries.xq') + "';<years>{movies:get_all_years()}</years>"
    query3 = session.query(input3)



    genres = query1.execute().replace("<genres>\r\n","").replace("\r\n</genres>","").replace("<genre>","").replace(
        "</genre>","").split("\r\n")
    ratings = query2.execute().replace("<ratings>\r\n", "").replace("\r\n</ratings>", "").replace("<rating>", "").replace(
        "</rating>", "").split("\r\n")
    years = query3.execute().replace("<years>\r\n", "").replace("\r\n</years>", "").replace("<year>", "").replace(
        "</year>", "").split("\r\n")

    session.close()

    tparams = {
        'content': newdoc,
        "genres": genres,
        "ratings": ratings,
        "years" : years,
     }
    return render(request, 'index.html', tparams)

def apply_filters(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    session.execute("open moviesDB")

    input1 = "import module namespace movies = 'com.movies' at '" + os.path.join(BASE_DIR,
                                                                                 'app/data/queries/queries.xq') + "';<genres>{movies:get_all_genres()}</genres>"
    query1 = session.query(input1)

    input2 = "import module namespace movies = 'com.movies' at '" + os.path.join(BASE_DIR,
                                                                                 'app/data/queries/queries.xq') + "';<ratings>{movies:get_all_ratings()}</ratings>"
    query2 = session.query(input2)

    input3 = "import module namespace movies = 'com.movies' at '" + os.path.join(BASE_DIR,
                                                                                 'app/data/queries/queries.xq') + "';<years>{movies:get_all_years()}</years>"
    query3 = session.query(input3)

    genres = query1.execute().replace("<genres>\r\n", "").replace("\r\n</genres>", "").replace("<genre>", "").replace(
        "</genre>", "").split("\r\n")
    ratings = query2.execute().replace("<ratings>\r\n", "").replace("\r\n</ratings>", "").replace("<rating>",
                                                                                                  "").replace(
        "</rating>", "").split("\r\n")
    years = query3.execute().replace("<years>\r\n", "").replace("\r\n</years>", "").replace("<year>", "").replace(
        "</year>", "").split("\r\n")


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
    xml = xmltodict.unparse(dict,pretty=True)

    '''
    xslt_name = 'movies.xsl'
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)

    tree = ET.parse(xml)
    xslt = ET.parse(xsl_file)

    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    tparams = {
        'content': newdoc,
        "genres": ["Action", "Adventure", "Fantasy", "Sci-Fi", "Thriller", "Romance", "Animation", "Comedy", "Family",
                   "Musical", "Mystery", "Western", "Drama", "History", "Sport", "Crime", "Horror", "War", "Biography",
                   "Music", "Documentary", "Film-Noir"],
        "ratings": ["PG-13", "PG", "G", "R", "Approved", "NC-17", "X", "Not Rated", "Unrated", "M", "GP", "Passed"],
        "years": ["2003", "2001", "1999", "2000", "1963", "1000"]
    }
    return render(request, 'index.html', tparams)
    '''
    return movies_feed(request)