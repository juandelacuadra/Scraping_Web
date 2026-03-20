# IMPORTO MODULOS
from bs4 import BeautifulSoup as bs
from time import sleep
import json
import os
import pandas as pd
import requests


class AxesorMining:

    '''
    Clase para scrapping en Axesor.

    === ATRIBUTOS ===
    DICT_EQUIVALENCIAS -> Convierte el nombre del elemento en código al que usamos en el dataframe.
    DICT_EQUIVALENCIAS_DIRECCION -> Convierte el nombre del elemento en código al que usamos en el dataframe.
    COLUMNAS_DF -> Define las columnas que va a tener la tabla.

    === METODOS ===
    request_soup(url)          -> Devuelve el Soup de la URL que le pasemos sin procesar ningun formato.
    paginado(url_municipio)    -> Devuelve el numero de páginas del municipio.
    listado_empresas(url_page) -> Devuelve el listado de empresas de la página.
    obtener_empresa(parametros)-> Devuelve un diccionario con los datos de la empresa.
    '''

    # ATRIBUTOS:
    DICT_EQUIVALENCIAS = {
        'CIF': 'taxID',
        'Email': 'email',
        'Nombre': 'name',
        'Objeto Social': 'description',
        'Telefono': 'telephone',
        'Web': 'url',
    }

    DICT_EQUIVALENCIAS_DIRECCION = {
        'Calle y Numero': 'streetAddress',
        'Codigo Postal': 'postalCode',
        'Localidad': 'addressLocality',
        'Provincia': 'addressRegion',
    }

    COLUMNAS_DF = [
        'Provincia',
        'Index Localidad',
        'Localidad',
        'Pagina',
        'Index Pagina',

        'Nombre',
        'CIF',
        'Telefono',
        'Email',
        'Web',

        'Calle y Numero',
        'Codigo Postal',

        'Forma Juridica',
        'Objeto Social',
        'CNAE',
        'CNAE Literal',
        'SIC',
        'SIC Literal',
    ]

    ROOT_PROVINCIAS = 'data/0_Provincias'

    ROOT_DIRECTORIOS = 'data/1_Directorios'

   # ============== CONSTRUCTOR: ============== #
    def __init__(self):
        pass

    # ============== MÉTODOS: ============== #
    def request_soup(self, url):
        """
        Parámetro: url (str).
        Devuelve el Soup de la URL que le pasemos sin procesar ningun formato.
        Reintenta hasta 3 veces si salta el captcha.
        """

        # INTENTAMOS UN MÁXIMO DE 3 VECES (PARA EVITAR UN BUCLE INFINITO)
        for intento in range(3):

            # ME TRAIGO EL HTML CON TIMEOUT PARA NO QUEDARNOS COLGADOS
            response = requests.get(url, timeout=15)
            sleep(3)  # POR DEBAJO DE ESTE TIEMPO NOS CAPAN LA CONEXION
            print('Respuesta del servidor: ' + str(response.status_code))

            # SI EL SERVIDOR NOS DA UN ERROR, SALIMOS DIRECTAMENTE
            if response.status_code != 200:
                print('>> Error del servidor: ' + str(response.status_code))
                return None

            html = response.content
            soup = bs(html, "lxml")

            # COMPROBAMOS SI NOS HAN PUESTO CAPTCHA
            if soup.find('div', id='captcha') or soup.find('title', string=lambda t: t and 'captcha' in t.lower()):
                print('>> Ha saltado el captcha. Reintentando en 20 segundos... (intento ' + str(intento + 1) + ' de 3)')
                sleep(20)
                continue  # VOLVEMOS A INTENTARLO

            # SI TODO BIEN, DEVOLVEMOS EL SOUP
            return soup

        # SI AGOTAMOS LOS INTENTOS, AVISAMOS Y DEVOLVEMOS None
        print('>> No se pudo obtener la página tras 3 intentos: ' + url)
        return None

    def paginado(self, url_municipio):
        """
        Parámetro: url_municipio (str).
        Devuelve el numero de páginas del municipio.
        """

        # EXTRAIGO EL CÓDIGO
        soup = self.request_soup(url_municipio)

        # VALIDO SI HAY PAGINACION O NO
        paginacion = soup.find('div', class_='paginacion-numeracion')

        # VAMOS A OBTENER EL NÚMERO DE PÁGINAS:
        if paginacion:
            page_max = int(paginacion.find_all('a')[-1].get_text(strip=True))
        else:
            page_max = 1

        print('\nPáginas de resultados -> ' + str(page_max))
        return page_max

    def listado_empresas(self, url_page):
        """
        Parámetro: url_page (str).
        Devuelve el listado de empresas de la página.
        """
        # EXTRAIGO EL CÓDIGO
        soup = self.request_soup(url_page)

        # ACCEDO Y SACO LOS DATOS
        listado_empresas = soup.select('#listaEmpresas table a')

        print('\n>> Comienza el listado...')
        return listado_empresas

    def obtener_empresa(self, parametros):
        """
        Parámetro: parametros (list).
            - url_empresa
            - dir_provincia
            - nombre_municipio
            - page
            - index_pagina
            - index_localidad

        Devuelve la lista con los datos de la empresa.
        """

        # DESEMPAQUETO LOS PARÁMETROS
        url_empresa, dir_provincia, nombre_municipio, page, index_pagina, index_localidad = parametros

        # DOY FORMATO A LA URL
        print('-----------------------')

        # EXTRAIGO EL CÓDIGO
        soup = self.request_soup(url_empresa)

        # SI request_soup DEVOLVIÓ None (ERROR O CAPTCHA), SALIMOS
        if soup is None:
            return None

        # =========================================== #
        # TENGO QUE VALIDAR SI VIENE CON CAPTCHA O NO #
        # =========================================== #

        if soup.find(id='tablaInformacionGeneral'):

            print('>> Existen datos. Extrayendo...')

            # 1 - DECLARO UN DICCIONARIO A RELLENAR CON LA MISMA ESTRUCTURA QUE LAS COLUMNAS DEL DF
            insert_empresa = {
                'Provincia': os.path.splitext(dir_provincia)[0],  # QUITO LA EXTENSION DEL NOMBRE DE ARCHIVO
                'Index Localidad': 0,
                'Localidad': nombre_municipio,
                'Pagina': '',
                'Index Pagina': 0,

                'Nombre': '',
                'CIF': '',
                'Telefono': '',
                'Email': '',
                'Web': '',

                'Calle y Numero': '',
                'Codigo Postal': '',

                'Forma Juridica': '',
                'Objeto Social': '',
                'CNAE': '',
                'CNAE Literal': '',
                'SIC': '',
                'SIC Literal': '',
            }

            # 2 - BUSCO EL SCRIPT CON LOS REQUISITOS, ES EL QUE TRAE LOS DATOS.
            scripts = soup.find_all("script", type="application/ld+json")

            # INICIALIZO EL DICCIONARIO A None PARA SABER SI LO ENCONTRAMOS O NO
            dict_empresa = None

            # LIMPIO LA INFO Y CONVIERTO DE JSON A DICT
            for i in scripts:
                soup_script = i.get_text(strip=True).replace("\n", "")
                json_script = json.loads(soup_script)

                # DENTRO DE LOS SCRIPTS, APUNTO AL CORRECTO
                if '@type' in json_script and json_script['@type'] == 'LocalBusiness':
                    dict_empresa = json_script

            # SI NO ENCONTRAMOS EL SCRIPT CON DATOS, SALIMOS
            if dict_empresa is None:
                print('>> No se encontraron datos JSON de la empresa.')
                return None

            # CRUZO PARA RELLENAR VALORES
            for key in insert_empresa:
                # EQUIVALENCIAS
                try:
                    # PRIMER INTENTO AL VUELO
                    insert_empresa[key] = dict_empresa[self.DICT_EQUIVALENCIAS[key]].strip(
                    )
                except KeyError:
                    try:
                        # LOS CAMPOS DE DIRECCIÓN ESTÁN EN UN SEGUNDO NIVEL
                        insert_empresa[key] = dict_empresa['address'][self.DICT_EQUIVALENCIAS_DIRECCION[key]].strip(
                        )
                    except Exception:
                        # SI NO EXISTE, LO PONEMOS
                        insert_empresa[key] = 'SIN DATOS'

            # QUITO LOS VALORES ERRÓNEOS EN LAS WEBS Y TELEFONOS
            if insert_empresa['Web'] == 'http://':
                insert_empresa['Web'] = 'SIN DATOS'

            if not insert_empresa['Telefono']:
                insert_empresa['Telefono'] = 'SIN DATOS'

            # RECUPERO FORMA, CNAE Y SIC DESDE CÓDIGO:

            # FILA DE tablaInformacionGeneral DONDE EL PRIMER td ES 'Forma Jurídica:' Y EL SEGUNDO ES EL VALOR.
            try:
                td_element = soup.find('td', text='Forma jurídica:')
                value_forma = td_element.find_next_sibling().text.strip()
                insert_empresa['Forma Juridica'] = value_forma
            except Exception:
                insert_empresa['Forma Juridica'] = 'SIN DATOS'

            # FILA DE tablaInformacionGeneral DONDE EL PRIMER td ES 'CNAE:' Y EL SEGUNDO ES EL VALOR.
            try:
                td_element = soup.find('td', text='CNAE:')
                value_cnae = td_element.find_next_sibling().text.strip()
                split_cnae = value_cnae.split(' ')

                cnae = split_cnae[0]
                cnae_literal = value_cnae[len(cnae):].strip()
                insert_empresa['CNAE'] = cnae
                insert_empresa['CNAE Literal'] = cnae_literal
            except Exception:
                insert_empresa['CNAE'] = 'SIN DATOS'
                insert_empresa['CNAE Literal'] = 'SIN DATOS'

            # FILA DE tablaInformacionGeneral DONDE EL PRIMER td ES 'SIC:' Y EL SEGUNDO ES EL VALOR.
            try:
                td_element = soup.find('td', text='SIC:')
                value_sic = td_element.find_next_sibling().text.strip()
                split_sic = value_sic.split(' ')

                sic = split_sic[0]
                sic_literal = value_sic[len(sic):].strip()
                insert_empresa['SIC'] = sic
                insert_empresa['SIC Literal'] = sic_literal
            except Exception:
                insert_empresa['SIC'] = 'SIN DATOS'
                insert_empresa['SIC Literal'] = 'SIN DATOS'

            # PÁGINA DE RESULTADOS EN LA QUE ESTÁ E INDEX
            insert_empresa['Pagina'] = page
            insert_empresa['Index Pagina'] = index_pagina
            insert_empresa['Index Localidad'] = index_localidad

            # DEVUELVO LA EMPRESA
            return insert_empresa
