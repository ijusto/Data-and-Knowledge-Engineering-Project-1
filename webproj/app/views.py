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
    xsl_file = os.path.join(BASE_DIR, 'app/data/' + xslt_name)

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
    if 'title' in request.POST and 'year' in request.POST:
        title = request.POST['title']
        year = request.POST['year']
        if peso and altura:
            icm = (float(peso) / float(altura) ** 2)
            categoria = '0'
            if (icm < 18.5):
                categoria = 'Abaixo do peso ideal',
            elif (icm >= 18.5 and icm < 25):
                categoria = 'Peso normal'
            elif (icm >= 25 and icm < 30):
                categoria = 'Excesso de peso'
            elif (icm >= 30 and icm < 35):
                categoria = 'Obesidade(grau I)'
            elif (icm >= 35 and icm < 40):
                categoria = 'Obesidade(grau II)'
            else:
                categoria = 'Obesidade(grau III)'
            return render(
                request,
                'rcalcIMC.html',
                {
                    'icm': icm,
                    'categoria': categoria,
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