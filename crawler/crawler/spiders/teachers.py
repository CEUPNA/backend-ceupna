from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from crawler.items import TeacherItem
import time

import re

class TeachersSpider(CrawlSpider):
	name = "teachers"
	allowed_domains = ["unavarra.es"]

	deparments = ['automaticaycomputacion', 'cienciasdelmedionatural', 'cienciasdelasalud',
	              'derechoprivado', 'derechopublico', 'economia', 'estadistica', 'filologia',
	              'fisica', 'geografiaehistoria', 'gestionempresas', 'electricayelectronica',
	              'matematicaeinformatica', 'mecanicaenergeticaymateriales', 'matematicas',
	              'produccionagraria', 'proyectoseingenieriarural', 'psicologiaypedagogia',
	              'quimicaaplicada', 'sociologia', 'tecnologiaalimentos', 'trabajosocial']
#	start_urls = ["http://www.unavarra.es/dep-" + dpto +
	#              "/personal/personal-docente-e-investigador?rangoLetras=a-z" for dpto in deparments]
	start_urls = ["http://www.unavarra.es/dep-tecnologiaalimentos/personal/personal-docente-e-investigador?rangoLetras=a-z"]

	rules = (
        # Extract links matching '.html' and parse them with the spider's method parse_item
		Rule(LinkExtractor(allow=('.*',), restrict_xpaths=('//ul[contains(@class, "listadoCurriculum")]')), callback='parse_item'),
    )



	def parse_item(self, response):
		item = TeacherItem()
		item ["id"] = str(re.search('(?<==)\w+', response.url).group(0))
		name = response.xpath('//div[@class="fichaCurriculum"]/div/div/h2/text()')
		item ["name"] = name.extract()[0].title().replace("\t","").replace("\n","").replace("\r","") .replace(" De ", " de ").replace(" Del ", " del ").replace(" La "," la ") #\u00d1 \u00aa
		aux = response.xpath('//div[@class="fichaCurriculum"]/div/div/p/text()').extract();
		item ["email"] = aux[0][1:] + "@unavarra.es"
		item ["telephone"] = aux[2][1:]

		if (item ["id"][0] != ""):
			return item
		else:
			return None
