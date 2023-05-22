# IMPORTO MODULOS
from bs4 import BeautifulSoup as bs
from time import sleep
import json
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
    request_soup(url)               -> Devuelve el Soup de la URL que le pasemos sin procesar ningun formato.
    paginado(url_municipio)         -> Devuelve el numero de páginas del municipio.
    listado_empresas(url_page)      -> Devuelve el listado de empresas de la página.
    listado_empresas(url_page)      -> Devuelve el listado de empresas de la página.
    depurar_empresas(dir_provincia) -> Revisa si nos hemos saltado alguna empresa.
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
        """


        # ME TRAIGO EL HTML
        response = requests.get(url)
        sleep(3)  # POR DEBAJO DE ESTE TIEMPO NOS CAPAN LA CONEXION
        html = response.content
        soup = bs(html, "lxml")
        print('Respuesta del servidor: ' + str(response))

        if soup.find('meta', attrs={'name': 'ROBOTS'}):  # TRAE CAPTCHA

            print('>> Ha saltado el captcha. Reintentando en 20 segundos...')
            sleep(20)
            soup = self.request_soup(url)

        return soup

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

        # =========================================== #
        # TENGO QUE VALIDAR SI VIENE CON CAPTCHA O NO #
        # =========================================== #

        if soup.find(id='tablaInformacionGeneral'):

            print('>> Existen datos. Extrayendo...')

            # 1 - DECLARO UN DICCIONARIO A RELLENAR CON LA MISMA ESTRUCTURA QUE LAS COLUMNAS DEL DF
            insert_empresa = {
                'Provincia': dir_provincia[:-2],
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

            # LIMPIO LA INFO Y CONVIERTO DE JSON A DICT
            for i in scripts:
                soup_script = i.get_text(strip=True).replace("\n", "")
                json_script = json.loads(soup_script)

                # DENTRO DE LOS SCRIPTS, APUNTO AL CORRECTO
                if '@type' in json_script and json_script['@type'] == 'LocalBusiness':
                    dict_empresa = json_script

            # CRUZO PARA RELLENAR VALORES
            for key in insert_empresa:
                # EQUIVALENCIAS
                try:
                    # PRIMER INTENTO AL VUELO
                    insert_empresa[key] = dict_empresa[self.DICT_EQUIVALENCIAS[key]].strip()
                except KeyError:
                    try:
                        # LOS CAMPOS DE DIRECCIÓN ESTÁN EN UN SEGUNDO NIVEL
                        insert_empresa[key] = dict_empresa['address'][self.DICT_EQUIVALENCIAS_DIRECCION[key]].strip()
                    except:
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
            except:
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
            except:
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
            except:
                insert_empresa['SIC'] = 'SIN DATOS'
                insert_empresa['SIC Literal'] = 'SIN DATOS'

            # PÁGINA DE RESULTADOS EN LA QUE ESTÁ E INDEX
            insert_empresa['Pagina'] = page
            insert_empresa['Index Pagina'] = index_pagina
            insert_empresa['Index Localidad'] = index_localidad

            # DEVUELVO LA EMPRESA
            return insert_empresa
