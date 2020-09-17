# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import bs4 as bs
import json
import requests
import datetime
import logging

from .spiders import BaseSpider

class ScopusSpider(BaseSpider):
    name = 'scopus'
    pagLen = 100
    custom_settings ={
        "AUTOTHROTTLE_ENABLED": True,
        "LOG_LEVEL": "WARNING"

    }
    
    def start_requests(self):
        yield scrapy.Request(url='https://scopus.com/', callback=self.api_search, dont_filter=True)
    def api_search(self, response):
        count = self.user_settings.get('count',0)
        search = self.user_settings['busca']
        apiKey = self.user_settings['api-key']

        self.search_url = 'https://api.elsevier.com/content/search/scopus?'

        self.headers = {
            'X-ELS-APIKey': apiKey,
            'Accept': '*/*'
        }

        params = {
            'query': search,
            'count': min(self.pagLen,count) if count>0 else self.pagLen, #define o tamanho da primeira página
        }

        url = self.search_url+urllib.parse.urlencode(params)
        meta = {
            'start': 0,
        }

        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_search, meta=meta)
    def parse_search(self, response):
        count = self.user_settings.get('count',0)

        try:
            obj = json.loads(response.text)['search-results']
            result = obj['entry']
            total_found = int(obj['opensearch:totalResults'])
        except KeyError:
            result = []

        total = min(total_found, count) if count>0 else total_found #retorna o número máximo de artigos que devem ser pesquisados

        for artigo in result:
            params = {
                'httpAccept': 'application/json',
                'fields': 'description'
            }

            meta = {
                'item': artigo
            }
            links = {'link:'+a['@ref']: a['@href'] for a in artigo['link']}
            artigo.update(links)
            artigo.pop('link',None)
            artigo.pop('link:author-affiliation',None)
            artigo.pop('link:self',None)
            artigo.pop('@_fa',None)

            doc_details_url = artigo['prism:url']+'?'+urllib.parse.urlencode(params)
            logging.warning(doc_details_url)
            yield scrapy.Request(url=doc_details_url, headers=self.headers, callback=self.parse_doc_details, meta=meta)

        # se o número de artigos já pesquisados for menor que o máximo a pesquisar, vai para a próxima página
        if response.meta['start'] + len(result) < total:
            start = response.meta['start'] + len(result)
            search = self.user_settings['busca']
            
            params = {
                'query': search,
                'count': min(self.pagLen,count-start) if count-start>0 else self.pagLen, #define o tamanho da próxima página
                'start': start
            }
            
            url = self.search_url+urllib.parse.urlencode(params)

            meta = {
                'start': start,
            }
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_search, meta=meta)
    
            
    def parse_doc_details(self, response):
        item = response.meta['item']
        obj = json.loads(response.text)
        
        try:
            link = obj['abstracts-retrieval-response']['item']['bibrecord']['head']['source']['website']\
                ['ce:e-address']['$']
        except:
            link = None
        item['source-address'] = link
        try:
            abstract = obj['abstracts-retrieval-response']['item']['bibrecord']['head']['abstracts']
        except:
            abstract = None
        item['abstract'] = abstract
        srcView = None
        try:
            r = requests.get('https://doi.org/'+item['prism:doi'], allow_redirects=False)
            if r.status_code == 302:
                srcView = str(r.headers['Location'])
        except:
            srcView = None
        item['view-in-source'] = srcView
        


        meta = {
            'item': item,
            }

        url_source_details = 'https://www.scopus.com/source/citescore/{}.uri'.format(item['source-id'])
        headers = {
            'Accept': 'application/json',
            'referer': url_source_details
        }

        yield scrapy.Request(url=url_source_details, headers=headers, callback=self.parse_source_details, meta=meta,dont_filter=True)

    def parse_source_details(self, response):
        curr_year = datetime.datetime.now().year
        for year in range(curr_year-3,curr_year):
            try:
                obj = json.loads(response.text)
                score = [m['rp'] for m in obj['yearInfo'][str(year)]['metricType'] if m['documentType']=='all']
                score = score[0]
            except:
                score = 0
            response.meta['item']['source-score-{}'.format(year)] = score
        yield response.meta['item']