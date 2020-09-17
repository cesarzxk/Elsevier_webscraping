# -*- coding: utf-8 -*-
import scrapy
import urllib
from .spiders import BaseSpider

class DrugBankSpider(BaseSpider):
    name = 'drugbank'

    def start_requests(self):
        inputs = self.user_settings['inputs']

        search_url = 'https://www.drugbank.ca/unearth/q?'

        for input_var in inputs:
            search_params = {
                'utf8': '✓',
                'searcher': 'drugs',
                'query': input_var
            }

            url = search_url+urllib.parse.urlencode(search_params)
            yield scrapy.Request(url=url, callback=self.parse, 
                meta={
                    'buscado': input_var,
#                    "proxy": "http://186.221.186.8:38173",
                })

    def parse(self, response):
        # Três cenários são possíveis por busca:
        #   (1) lista de resultados
        #   (2) nenhum resultado
        #   (3) resultado único

        # se (1) pega apenas o primeiro link da lista
        found = response.css('div.search-result').css('h2 a::attr(href)').get()
        if found:
            # cenário (1)
            yield response.follow(found, callback=self.parse, meta=response.meta)

        # se (3) ou (2) procura pela lista de outputs dentro do documento
        else:
            propriedades = [a.css('td::text').getall() 
                for a in response.css('table#drug-moldb-properties tr') if a.css('td')]

            outputs = self.user_settings['outputs']

            name = response.css('h1::text').get()

            farmaco_output = {}
            farmaco_output['buscado'] = response.meta['buscado']
            farmaco_output['encontrado'] = name or ''

            farmaco_output['url'] = response.url
            farmaco_output['propriedades'] = []
            if propriedades and outputs:
                for out in outputs:
                    propriedade_output = {}
                    propriedade_output[out.strip()] = []
                    for p in propriedades:
                        if out.strip().lower() in p[0].lower():
                            propriedade_output[out.strip()].append({
                                p[0].strip().lower(): p[1].strip().lower(),
                            })
                    if propriedade_output[out.strip()]:
                        farmaco_output['propriedades'].append(propriedade_output)
            yield farmaco_output

    #def getName(self, response):
        #name = response.css('h1')
        #if name:
        #    name = bs.BeautifulSoup(name.get(), features='lxml')
        #if name.find('span'):
        #    name.find('span').decompose()
        #name = name.text.strip()
        #return name if name else ''

        


