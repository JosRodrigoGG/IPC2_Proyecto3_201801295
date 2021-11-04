import requests
import tarfile
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from json2xml import json2xml

endpoint = 'http://127.0.0.1:5000{}'


def viewFile(request):
    context = {}
    response = requests.get(endpoint.format('/procesar'))

    if response.status_code == 200:
        context = {
            'data': 'Archivo cargado'
        }
    else:
        context = {
            'data': 'No hay datos cargados'
        }
    return render(request, "file.html", context)


def cargarArchivo(request):
    if request.method == 'POST':
        response = requests.post(endpoint.format("/procesar"), request.FILES['archivoXML'].read())

        context = {}
        if response.status_code == 200:
            context = {
                'data': 'Archivo cargado'
            }
        else:
            context = {
                'data': 'Error en la carga de archivo'
            }

        return render(request, "file.html", context)
    elif request.method == 'GET':
        context = {}
        response = requests.get(endpoint.format('/procesar'))

        if response.status_code == 200:
            context = {
                'data': 'Archivo cargado',
                'datos': json2xml.Json2xml(response.json()).to_xml()
            }
        else:
            context = {
                'data': 'No hay datos cargados'
            }
        return render(request, "file.html", context)
    else:
        return render(request, "file.html")


def buscar(request):
    context = {}
    response = requests.get(endpoint.format('/procesar'))

    if response.status_code == 200:
        context = {
            'data': 'Archivo cargado',
            'datos': json2xml.Json2xml(response.json()).to_xml()
        }
    else:
        context = {
            'data': 'No hay datos cargados'
        }
    return render(request, "file.html", context)


def reset(request):
    context = {
        'data': 'No hay datos cargados',
    }

    requests.put(endpoint.format('/borrar'))

    return render(request, "file.html", context)


def generarArchivoSalida(request):
    context = {}
    response = requests.get(endpoint.format('/procesar'))

    if response.status_code == 200:
        context = {
            'data': 'Archivo cargado',
            'datos': json2xml.Json2xml(response.json()).to_xml()
        }

        out = BytesIO()
        tar = tarfile.open(mode="w:gz", fileobj=out)
        data = json2xml.Json2xml(response.json()).to_xml().encode('utf-8')
        file = BytesIO(data)
        info = tarfile.TarInfo(name="archivo.xml")
        info.size = len(data)
        tar.addfile(tarinfo=info, fileobj=file)
        tar.close()

        response = HttpResponse(out.getvalue(), content_type='application/tgz')
        response['Content-Disposition'] = 'attachment; filename=archivo.tgz'

        return response
    else:
        context = {
            'data': 'No hay datos cargados'
        }

    return render(request, "file.html", context)
