import json
import time
from datetime import datetime

import requests
import tarfile
import xml.etree.ElementTree as ET

from io import BytesIO

from django.http import HttpResponse
from django.template import loader, Context
from django.shortcuts import render

endpoint = 'http://127.0.0.1:5000{}'


def viewRequest(request):
    context = {}
    response = requests.get(endpoint.format('/consultaDatos'))

    if response.status_code == 200:
        context = {
            'mensaje': 'Datos cargados',
        }
    else:
        context = {
            'mensaje': 'No hay datos cargados'
        }

    return render(request, "request.html", context)


def consultarDatos(request):
    context = {}
    response = requests.get(endpoint.format('/consultaDatos'))

    if response.status_code == 200:
        context = {
            'mensaje': 'Datos cargados',
            'datos': response.text
        }
    else:
        context = {
            'mensaje': 'No hay datos cargados'
        }

    return render(request, "request.html", context)


def archivoConsulta(request):
    context = {}
    response = requests.get(endpoint.format('/consultaDatos'))

    if response.status_code == 200:
        context = {
            'mensaje': 'Datos cargados'
        }

        out = BytesIO()
        tar = tarfile.open(mode="w:gz", fileobj=out)
        data = response.text.encode('utf-8')
        file = BytesIO(data)
        info = tarfile.TarInfo(name="archivo.xml")
        info.size = len(data)
        tar.addfile(tarinfo=info, fileobj=file)
        tar.close()

        response = HttpResponse(out.getvalue(), content_type='application/tgz')
        response['Content-Disposition'] = 'attachment; filename=consulta.tgz'

        return response
    else:
        context = {
            'mensaje': 'No hay datos cargados'
        }

    return render(request, "request.html", context)


def resumenIVA(request):
    context = {}
    response = requests.get(endpoint.format('/resumenIva/' + str(request.GET['fechaUnica'])))

    if response.status_code == 200:
        lista = response.json()['DATOS']['FACTURA']
        listaGraficaY = []
        listaGraficaY2 = []
        listaGraficaX = []

        for temp in lista:
            temp['MONTO'] = str("{:.2f}".format(float(temp['MONTO'])))
            temp['IVA'] = str("{:.2f}".format(float(temp['IVA'])))

            listaGraficaX.append(int(temp['NIT_EMISOR']))
            listaGraficaY.append(float(temp['IVA']))
            listaGraficaY2.append(float(temp['MONTO']))

        context = {
            'mensajeIVA': 'Datos obtenidos',
            'fechaUnica': request.GET['fechaUnica'],
            'datosIVA': lista,
            'datosIVAY': listaGraficaY,
            'datosIVAX': listaGraficaX,
            'datosIVAY2': listaGraficaY2,
        }
    elif response.status_code == 205:
        context = {
            'mensajeIVA': 'No hay datos en esa fecha',
            'fechaUnica': request.GET['fechaUnica']
        }
    else:
        context = {
            'mensajeIVA': 'No hay datos cargados'
        }
    return render(request, "request.html", context)


def resumenFecha(request):
    context = {}
    response = requests.get(endpoint.format(
        '/resumenRango/' + str(request.GET['estado']) + "/" + str(request.GET['fechaInicio']) + "/" + str(
            request.GET['fechaFin'])))

    if response.status_code == 200:
        lista = response.json()['DATOS']['FACTURA']
        listaGraficaY = []
        listaGraficaX = []

        contador = 1
        for temp in lista:
            temp['MONTO'] = str("{:.2f}".format(float(temp['MONTO'])))
            listaGraficaY.append(float("{:.2f}".format(float(temp['MONTO']))))
            listaGraficaX.append(int(contador))
            contador += 1

        context = {
            'mensajeFecha': 'Datos obtenidos',
            'fechaInicio': request.GET['fechaInicio'],
            'fechaFin': request.GET['fechaFin'],
            'datosFecha': lista,
            'datosFechaY': listaGraficaY,
            'datosFechaX': listaGraficaX
        }
    elif response.status_code == 205:
        context = {
            'mensajeFecha': 'No hay datos en esa fecha',
            'fechaInicio': request.GET['fechaInicio'],
            'fechaFin': request.GET['fechaFin'],
        }
    else:
        context = {
            'mensajeFecha': 'No hay datos cargados'
        }

    return render(request, "request.html", context)
