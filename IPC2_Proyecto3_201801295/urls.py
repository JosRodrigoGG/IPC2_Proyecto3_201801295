"""IPC2_Proyecto3_201801295 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from IPC2_Proyecto3_201801295.view.view_File import *
from IPC2_Proyecto3_201801295.view.view_Request import *

urlpatterns = [
    path('', viewFile),
    path('archivo/', viewFile),
    path('peticion/', viewRequest),
    path('cargarArchivo/', cargarArchivo),
    path('buscarDatos/', buscar),
    path('reset/', reset),
    path('archivoSalida/', generarArchivoSalida),
    path('consultar/', consultarDatos),
    path('archivoConsulta/', archivoConsulta),
    path('resumen/IVA/', resumenIVA),
    path('resumen/Fecha/', resumenFecha),
    path('archivoIVA/', archivoIVA),
    path('archivoFECHA/', archivoFecha),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
