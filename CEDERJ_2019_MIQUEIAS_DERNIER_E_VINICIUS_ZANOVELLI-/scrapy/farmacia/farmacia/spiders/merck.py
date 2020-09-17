# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import bs4 as bs

from .spiders import BaseSpider

class MerckSpider(BaseSpider):
    name = 'merck'

    def start_requests(self):
        inputs = self.user_settings['inputs']

        search_url = 'http://www.merckmillipore.com/BR/pt/search/'

        for input_var in inputs:
            url = search_url+urllib.parse.quote(input_var)
            yield scrapy.Request(url=url, callback=self.parse, 
                meta={
                    'buscado': input_var,
                })

    def parse(self, response):
        # Três cenários são possíveis por busca:
        #   (1) lista de resultados
        #   (2) nenhum resultado
        #   (3) resultado único

        # se (1) pega apenas o primeiro link da lista
        found = response.css(
            'div.container-serp').css('h2').css('a::attr(href)').get()
        if found:
            # cenário (1)
            yield response.follow(found, callback=self.parse, meta=response.meta)

        # se (3) ou (2) procura pela lista de outputs dentro do documento
        else:
            propriedades = [a.css('td::text').getall()
                for a in response.css('table.attribute-group-table tbody').css('tr')]

            outputs = self.user_settings['outputs']

            farmaco_output = {}
            farmaco_output['buscado'] = response.meta['buscado']
            farmaco_output['encontrado'] = ''

            farmaco_output['url'] = response.url
            farmaco_output['propriedades'] = []
            if propriedades and outputs:
                name = self.getName(response)
                farmaco_output['encontrado'] = name
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
                    farmaco_output['propriedades'].append(propriedade_output)
            yield farmaco_output
        

    def getName(self, response):
        name = response.css('h1')
        if name:
            name = bs.BeautifulSoup(name.get(), features='lxml')
        if name.find('span'):
            name.find('span').decompose()
        name = name.text.strip()
        return name if name else ''

        


