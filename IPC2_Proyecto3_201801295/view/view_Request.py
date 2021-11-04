from pipes import Template
from unittest import loader
from urllib.request import BaseHandler

import requests
import tarfile

from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from xhtml2pdf import pisa

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

    response = render(request, "request.html", context)
    response.set_cookie('FECHA_UNICA', str(request.GET['fechaUnica']))
    return response


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

    response = render(request, "request.html", context)
    response.set_cookie('FECHA_INICIO', str(request.GET['fechaInicio']))
    response.set_cookie('FECHA_FIN', str(request.GET['fechaFin']))
    response.set_cookie('ESTADO', str(request.GET['estado']))
    return response


def archivoFecha(request):
    FECHA_INICIO = request.COOKIES.get('FECHA_INICIO')
    FECHA_FIN = request.COOKIES.get('FECHA_FIN')
    ESTADO = request.COOKIES.get('ESTADO')

    if len(FECHA_FIN) != 0 and len(FECHA_INICIO) != 0:
        context = {}
        response = requests.get(endpoint.format(
            '/resumenRango/' + str(ESTADO) + "/" + str(FECHA_INICIO) + "/" + str(
                FECHA_FIN)))

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
                'fechaInicio': FECHA_INICIO,
                'fechaFin': FECHA_FIN,
                'datosFecha': lista,
                'datosFechaY': listaGraficaY,
                'datosFechaX': listaGraficaX
            }
        elif response.status_code == 205:
            context = {
                'mensajeFecha': 'No hay datos en esa fecha',
                'fechaInicio': FECHA_INICIO,
                'fechaFin': FECHA_FIN,
            }
        else:
            context = {
                'mensajeFecha': 'No hay datos cargados'
            }

        template_path = "template_FECHA.html"
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Reporte_Fecha.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

    return render(request, "request.html")


def archivoIVA(request):
    FECHA_UNICA = request.COOKIES.get('FECHA_UNICA')
    if len(FECHA_UNICA) != 0:
        context = {}
        response = requests.get(endpoint.format('/resumenIva/' + str(FECHA_UNICA)))

        if response.status_code == 200:
            print("HOLA")
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
                'fechaUnica': FECHA_UNICA,
                'datosIVA': lista,
                'datosIVAY': listaGraficaY,
                'datosIVAX': listaGraficaX,
                'datosIVAY2': listaGraficaY2,
            }
        elif response.status_code == 205:
            context = {
                'mensajeIVA': 'No hay datos en esa fecha',
                'fechaUnica': FECHA_UNICA
            }
        else:
            context = {
                'mensajeIVA': 'No hay datos cargados'
            }

        template_path = "template_IVA.html"
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Reporte_IVA.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

    return render(request, "request.html")
