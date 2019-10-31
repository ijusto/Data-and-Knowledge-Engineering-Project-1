from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from webproj.settings import BASE_DIR
import os
import lxml.etree as ET

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

    tparams = {
        'content': newdoc,
        "genres": ["Action", "Adventure", "Fantasy", "Sci-Fi", "Thriller", "Romance", "Animation", "Comedy", "Family",
              "Musical", "Mystery", "Western", "Drama", "History", "Sport", "Crime", "Horror", "War", "Biography",
              "Music", "Documentary", "Film-Noir"],
        "ratings": ["PG-13", "PG", "G", "R", "Approved", "NC-17", "X", "Not Rated", "Unrated", "M", "GP", "Passed"]
     }
    return render(request, 'index.html', tparams)

def apply_filters(request):
    genres = ["Action", "Adventure", "Fantasy", "Sci-Fi", "Thriller", "Romance", "Animation", "Comedy", "Family",
              "Musical", "Mystery", "Western", "Drama", "History", "Sport", "Crime", "Horror", "War", "Biography",
              "Music", "Documentary", "Film-Noir"]
    ratings = ["PG-13", "PG", "G", "R", "Approved", "NC-17", "X", "Not Rated", "Unrated", "M", "GP", "Passed"]
    print("\n- - - GENRES: - - -")
    for g in genres:
        if g in request.POST:
            print(g)
    print(("- - - - - - - - -\n"))
    return movies_feed(request)
