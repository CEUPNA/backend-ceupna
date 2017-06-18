# -*- coding: utf-8 -*-

from ..items import SubjectItem
from bs4 import BeautifulSoup, Comment
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import parse_qs, urlparse
import re


LANG_ES = 'es'
LANG_EU = 'eu'
LANG_EN = 'en'

SUBJ_BASIC = 'ba'
SUBJ_MANDATORY = 'ob'
SUBJ_OPTIONAL = 'op'
LITERAL_BASIC = ['Básica', 'Oinarrizkoa', 'Basic']
LITERAL_MANDATORY = ['Obligatoria', 'Nahitaezkoa', 'Mandatory']
LITERAL_OPTIONAL = ['Optativa', 'Aukerakoa', 'Optative']


class SubjectsSpider(CrawlSpider):
    """
    Clase para importar todos las asignaturas de las titulaciones de la Universidad.
    """
    name = "subjects"
    allowed_domains = ["unavarra.es"]

    # Bases para las URL
    base = 'http://www.unavarra.es'
    centers_and_degrees = ['fac-economicas/grado-en-economia',
                         'fac-economicas/grado-en-administracion-y-direccion-de-empresas',
                         'fac-economicas/grado-en-administracion-y-direccion-de-empresas-y-derecho-doble-grado',
                         'fac-economicas/programa-internacional-grado-ade',
                         'fac-economicas/programa-internacional-doble-grado',
                         'fac-economicas/doble-grado-ade-derecho-itinerario-internacional',
                         'ets-industrialesytelecos/grado-en-ingenieria-informatica',
                         'ets-industrialesytelecos/grado-en-ingenieria-en-tecnologias-industriales',
                         'ets-industrialesytelecos/grado-en-ingenieria-en-tecnologias-de-telecomunicacion',
                         'ets-industrialesytelecos/grado-ingenieria-electrica-electronica',
                         'ets-industrialesytelecos/grado-ingenieria-mecanica',
                         'ets-industrialesytelecos/grado-en-ingenieria-en-disenio-mecanico-campus-de-tudela',
                         'ets-industrialesytelecos/programa-internacional-ingenieria-informatica',
                         'ets-industrialesytelecos/programa-internacional-ingenieria-tecnologias-industriales'
                         'ets-industrialesytelecos/programa-internacional-telecomunicacion'
                         'fac-humanasysociales/grado-de-maestro-en-educacion-infantil',
                         'fac-humanasysociales/grado-de-maestro-en-educacion-primaria',
                         'fac-humanasysociales/grado-en-sociolog%C3%ADa-aplicada',
                         'fac-humanasysociales/grado-en-trabajo-social',
                         'fac-juridicas/grado-en-derecho',
                         'fac-juridicas/grado-en-relaciones-laborales-y-recursos-humanos',
                         'fac-cienciasdelasalud/grado-en-enfermeria',
                         'fac-cienciasdelasalud/grado-en-fisioterapia-campus-de-tudela',
                         'ets-agronomos/grado-en-ingenieria-agroalimentaria-y-del-medio-rural',
                         'ets-agronomos/grado-innovacion-procesos-productos-alimentarios',
                         'ets-agronomos/doble-grado-iamr-ippa']
    others = ['fac-humanasysociales/estudios/grado/haur-hezkuntzako-irakasleen-gradua/irakasgaien-zerrenda',
              #'fac-humanasysociales/estudios/grado/haur-hezkuntzako-irakasleen-gradua/ingelesezko-irakasgaien-eskaintza',
              'fac-humanasysociales/estudios/grado/lehen-hezkuntzako-irakasleen-gradua/irakasgaien-zerrenda',
              #'fac-humanasysociales/estudios/grado/lehen-hezkuntzako-irakasleen-gradua/ingelesezko-irakasgaien-eskaintza'
              ]
    types_subs = ['lista-asignaturas', 'oferta-de-asignaturas-en-ingles', 'ofertas-de-asignaturas-en-euskera']

    # Generación de las URL
    start_urls = []
    for centre_degree in centers_and_degrees:
        for type_sub in types_subs:
            cd_split = centre_degree.split('/')
            start_urls.append(base + '/' + cd_split[0] + '/estudios/grado/' + cd_split[1] + '/' + type_sub)

    for other in others:
        start_urls.append(base + '/' + other)

#    start_urls = ["http://www.unavarra.es/ets-industrialesytelecos/estudios/grado/grado-en-ingenieria-informatica/lista-asignaturas"]
#    start_urls = ["http://www.unavarra.es/fac-cienciasdelasalud/estudios/grado/grado-en-enfermeria/lista-asignaturas"]
#    start_urls = ['http://www.unavarra.es/fac-economicas/estudios/grado/grado-en-administracion-y-direccion-de-empresas-y-derecho-doble-grado/oferta-de-asignaturas-en-ingles']
#    start_urls = ['http://www.unavarra.es/fac-humanasysociales/estudios/grado/grado-de-maestro-en-educacion-infantil/oferta-de-asignaturas-en-euskera']

    rules = (
        Rule(LinkExtractor(allow=('.*',),
                           restrict_xpaths=('//table[contains(@class, "listadoAsignaturas")]/tbody/tr/td[3]'),),
                           callback='parse_subject'),
    )

    def parse_subject(self, response):
        """
        Método para la extracción de los datos de cada una de las URL referente a cada una de las guías de asignaturas.
        :param response: objeto de respuesta a la petición HTTP a cada una de las URL generadas.
        :return: objeto de tipo `subject` con todos los datos de una asignatura.
        """

        # Extracción de los campos de la URL.
        params_url = parse_qs(urlparse(response.url).query)  # Tratamiento del URL para coger el ID.
        subject_id = int(params_url['codAsig'][0])  # Recogido el ID del diccionario y guardado el texto.
        degree_id = int(params_url['codPlan'][0])  # Recogido el ID del diccionario y guardado el texto.
        language = int(params_url['languageId'][0])
        if language == 1:
            language = LANG_EN
        elif language == 100000:
            language = LANG_ES
        elif language == 100001:
            language = LANG_EU
        else:
            language = None

        # Para el grado de económicas que repite código. Suponemos que el internacional de ADE asecas es el 174.
        if 'programa-internacional-grado-ade' in response.url:
            degree_id = 174

        # Extracción de los campos de la cajetilla superior de datos básicos.
        table_basic_data = '//div[@class="contenedorSombraFicha"]/table/tbody'

        # Saber si la ficha existe o no
        flag = response.xpath(table_basic_data + '/text()')
        #print(flag)
        if not flag:
            name = None
            ects = None
            year = None
            semester = None
            kind_subj = None
            department = None
            teachers_list = None
            evaluation = None
            contents = None
            curriculum = None

        # Si la asignatura existe, cogemos el resto de los datos
        else:
            name = response.xpath(table_basic_data + '/tr/td[2]/text()').extract_first()  # Base del nombre.
            name = self._clean_names(name)
            ects = float(response.xpath(table_basic_data + '/tr[2]/td/text()').extract_first())
            kind_subj_base = response.xpath(table_basic_data + '/tr[2]/td[2]/text()').extract_first().strip()
            if kind_subj_base in LITERAL_BASIC:
                kind_subj = SUBJ_BASIC
            elif kind_subj_base in LITERAL_MANDATORY:
                kind_subj = SUBJ_MANDATORY
            elif kind_subj_base in LITERAL_OPTIONAL:
                kind_subj = SUBJ_OPTIONAL
            else:
                kind_subj = None

            year = response.xpath(table_basic_data + '/tr[2]/td[3]/text()').extract_first().strip()
            if year == '':
                year = None
            else:
                year = int(year)

            # NOTE: Por ahora el deparamento sale de la ficha, pero igual tendrá más sentido sacarlo de donde pertenezcan
            #       los profesores, sabiendo que así una asignatura puede tener más de un departamento.
            department = response.xpath(table_basic_data + '/tr[3]/td/text()').extract_first().strip()

            teachers_list_base = response.xpath('//a[@class="nuevaVentana"]/@href').extract()
            teachers_list = [int(re.findall("\d+", t)[0]) for t in teachers_list_base]

            semester = response.xpath(table_basic_data + '/tr[2]/td[4]/text()').extract_first()
            if '1' in semester:
                semester = 1
            elif '2' in semester:
                semester = 2
            else:
                language = None

            evaluation = self._clean_guide_fields(response.xpath('//div[@id="C08"]').extract_first())
            contents = self._clean_guide_fields(response.xpath('//div[@id="C07"]').extract_first())
            curriculum = self._clean_guide_fields(response.xpath('//div[@id="C09"]').extract_first())

        # Guardado de datos en las variables correspondientes.
        item = SubjectItem()
        item["subject_id"] = subject_id
        item["degree_id"] = degree_id
        item["language"] = language
        item["name"] = name
        item["credits"] = ects
        item["year"] = year
        item["semester"] = semester
        item["type"] = kind_subj
        item["department"] = department
        item["teachers"] = teachers_list
        item["evaluation"] = evaluation
        item["contents"] = contents
        item["curriculum"] = curriculum

        # Revisar que el item exista, sino entregar vacío.
        if item["subject_id"] != "":
            return item
        else:
            return None

    @staticmethod
    def _clean_guide_fields(html_fields):
        """
        Función para limpiar el código HTML obtenido para los campos de las guías. En particular, se encarga de:
            * Limpiar el nombre de las secciones (h3), los p vacíos que se añaden y el p para subir al comienzo.
            * Retirar todos los campos de tipo span (conservando el texto de su interior).
            * Limpiar todo el CSS inline que hay en los p y div.
            * Retira todos los comentarios.
        :param html_fields: Código original obtenido de la web de la guía de la asignatura.
        :return: Todo el código HTML limpio aplicado lo anterior.
        """
        # Hay que quitar los H3, los p vacíos (uno después del H3 y otro antes del p final) y el p de clase "subir".
        parsed_fields = BeautifulSoup(html_fields, 'html.parser')
        parsed_fields.h3.extract()  # Quitar el título
        parsed_fields.div.unwrap()  # Quitar el div que contiene el campo.

        # Para retirar todos los span pero guardar el texto.
        span_elems = parsed_fields.findAll('span')
        [e.unwrap() for e in span_elems]

        # Para quitar los p vacíos que tiene por defecto el campo.
        empty_tags = parsed_fields.findAll(
            lambda tag: tag.name == 'p' and not tag.contents and (tag.string is None or not tag.string.strip()))
        [empty_tag.extract() for empty_tag in empty_tags]

        # Para quitar el ancla que permite subir en la ficha.
        del_elem = parsed_fields.find('p', {'class': 'subir'})
        del_elem.extract()

        # Para limpiar los estilos CSS en los tags (inline).
        for tag in parsed_fields.findAll('p'):
            del tag.attrs
        for tag in parsed_fields.findAll('div'):
            del tag.attrs

        # Para quitar también los comentarios
        for tag in parsed_fields:
            if isinstance(tag, Comment):
                tag.extract()

        return str(parsed_fields)

    @staticmethod
    def _clean_names(name):

        name = ' '.join(name.title().split()).replace(" De ", " de ").replace(" Del ", " del ").replace(" La ", " la ")
        name.replace(" A ", " a ").replace(" Ii", " II").replace(" Iii", " III").replace(" Iv", " IV")
        name.replace(" Y ", " y ").replace(" En ", " en ").replace(" El ", " el ")
        return name
