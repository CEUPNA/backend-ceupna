# -*- coding: utf-8 -*-

from ..items import TeacherItem
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import parse_qs, urlparse

addition_url = "&dato=tutorias"


class TeachersSpider(CrawlSpider):
    """
    Clase para importar todos los profesores de la Universidad.
    """
    name = "teachers"
    allowed_domains = ["unavarra.es"]

    deparments = ['automaticaycomputacion', 'cienciasdelmedionatural', 'cienciasdelasalud', 'derechoprivado',
                  'derechopublico', 'economia', 'estadistica', 'filologia', 'fisica', 'geografiaehistoria',
                  'gestionempresas', 'electricayelectronica', 'matematicaeinformatica', 'mecanicaenergeticaymateriales',
                  'matematicas', 'produccionagraria', 'proyectoseingenieriarural', 'psicologiaypedagogia',
                  'quimicaaplicada', 'sociologia', 'tecnologiaalimentos', 'trabajosocial']

    start_urls = ["http://www.unavarra.es/dep-" + dpto +
                  "/personal/personal-docente-e-investigador?rangoLetras=a-z" for dpto in deparments]
#    start_urls = ["http://www.unavarra.es/dep-tecnologiaalimentos/personal/personal-docente-e-investigador?rangoLetras=a-z"]

    rules = (
        Rule(LinkExtractor(allow=('.*',), restrict_xpaths=('//ul[contains(@class, "listadoCurriculum")]'),
                           process_value=lambda x: x + addition_url), callback='parse_item'),
    )

    def parse_item(self, response):
        """
        Método para la extracción de los datos de cada una de las URL refente a cada profesor.
        :param response: objeto de respuesta a la petición HTTP a cada una de las URL generadas.
        :return: ojeto de tipo `teacher` con todos los datos de un profesor.
        """
        # Extracción y tratamiento de los campos.
        params_url = parse_qs(urlparse(response.url).query)  # Tratamiento del URL para coger el ID.
        upna_id = params_url['uid'][0]  # Recogido el ID del diccionario y guardado el texto.
        name = response.xpath('//div[@class="fichaCurriculum"]/div/div/h2/text()').extract()[0]  # Base del nombre.
        name = ' '.join(name.title().split()).replace(" De ", " de ").replace(" Del ", " del ").replace(" La ", " la ")
        aux = response.xpath('//div[@class="fichaCurriculum"]/div/div/p/text()').extract()  # Para sacar el tfno y mail.
        email = ''.join(aux[0][1:].split()) + '@unavarra.es'  # Tratado para evitar los espacios en blanco.
        telephone = aux[2][1:] # TODO: Tratar el teléfono para aquellos que son "raros" y hacer todos iguales
        timetable = self._parse_timetable(response.xpath('//div[@class="texto"]').extract()[0])  # Utilizando un método.

        # Guardado de datos en las variables correspondientes.
        item = TeacherItem()
        item["upna_id"] = upna_id
        item["name"] = name
        item["email"] = email
        item["telephone"] = telephone
        item["timetable"] = timetable

        # Revisar que el item exista, sino entregar vacío.
        if item["upna_id"][0] != "":
            return item
        else:
            return None

    @staticmethod
    def _parse_timetable(timetable_html):
        """
        Extracción y tratamiento del código de la página web de las tutorías.
        :param timetable_html: código html del div `texto` de la web de la Universidad.
        :return: código html concreto de las tutorías.
        """
        # Extracción y tratamiento de las tutorías.
        timetable_html = ' '.join(timetable_html.split())
        parse_timetable = BeautifulSoup(timetable_html, 'html.parser')
        del_elem = parse_timetable.div.div  # Extraigo y elimino los datos de la fichaCurriculum.
        del_elem.extract()
        del_elem = parse_timetable.div.h2  # Extraigo y elimino el h2 de tutorías.
        del_elem.extract()

        children = parse_timetable.find("div", {"class": "texto"}).findChildren()
        timetable = ''
        for child in children:
            timetable += str(child)

        return timetable
