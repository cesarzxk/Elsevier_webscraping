@César Vargas dos Santos e Daniel Vargas Dos Santos CEDERJ 2020.2
# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import bs4 as bs
import json
import requests
import datetime
import logging

from .spiders import BaseSpider


class ScopusSpider(BaseSpider) :
    name = 'scopus'  # nome do spider, deve ser único
    pagLen = 100
    
    custom_settings = {
        "LOG_LEVEL" : "WARNING",  # Nível mínimo de registro do log: Critical, error, warning, info
       
    }

    def start_requests(self) :
        yield scrapy.Request(url='https://scopus.com/', callback=self.api_search, dont_filter=True) #inicia os requests

    def api_search(self, response) :
        count = self.user_settings.get('count', 0)  # Caso não exista cont retorna 0
        search = self.user_settings['busca']  # Procurando a key 'busca' que é a pesquisa que está no json
        apiKey = self.user_settings['api-key']  # procurando a key 'api-key' conseguida no site elsevier

        self.search_url = 'https://api.elsevier.com/content/search/scopus?'

        self.headers = {
            'X-ELS-APIKey' : apiKey,
            'Accept' : '*/*'
        }

        params = {
            'query' : search,
            'count' : min(self.pagLen, count) if count > 0 else self.pagLen,  # define o tamanho da primeira página
        }

        url = self.search_url + urllib.parse.urlencode(params)
        meta = {
            'start' : 0,
        }

        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_search, meta=meta)

    def parse_search(self, response) : #realiza tratamento e captura cada artigo individualmente 
        count = self.user_settings.get('count', 0)

        try :
            obj = json.loads(response.text)['search-results']
            result = obj['entry']
            total_found = int(obj['opensearch:totalResults']) #obtém o total de artigos
        except KeyError :
            result = []
        total = min(total_found, count) if count > 0 else total_found  # Quantidade total de artigos


        for artigo in result:

                 params = {
                     'httpAccept' : 'application/json',
                     'fields' : 'description'
                 }

                 meta = {
                     'item' : artigo
                 }
                 links = {'link:' + a['@ref'] : a['@href'] for a in artigo['link']}
                 artigo.update(links)
                 artigo.pop('link', None)
                 artigo.pop('link:author-affiliation', None)
                 artigo.pop('link:self', None)
                 artigo.pop('@_fa', None)

                 doc_details_url = artigo['prism:url'] + '?' + urllib.parse.urlencode(params)
                 logging.warning(doc_details_url)

                 yield scrapy.Request(url=doc_details_url, headers=self.headers, callback=self.parse_doc_details, meta=meta)


        # se o número de artigos já pesquisados for menor que o máximo a pesquisar, vai para a próxima página
        if response.meta['start'] + len(result) < total :
            start = response.meta['start'] + len(result)
            search = self.user_settings['busca']

            params = {
                'query' : search,
                'count' : min(self.pagLen, count - start) if count - start > 0 else self.pagLen,
                # define o tamanho da próxima página
                'start' : start
            }

            url = self.search_url + urllib.parse.urlencode(params)

            meta = {
                'start' : start,
            }
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_search, meta=meta)


    def parse_doc_details(self, response) : #realiza a obtenção do abstract e source-address
        item = response.meta['item']
        obj = json.loads(response.text)
        self.referencias[item['eid']] = []

        try :
            link = obj['abstracts-retrieval-response']['item']['bibrecord']['head']['source']['website'] \
                ['ce:e-address']['$'] #obtenção do source-address
        except :
            link = None

        item['source-address'] = link

        try :
            abstract = obj['abstracts-retrieval-response']['item']['bibrecord']['head']['abstracts'] #obtenção do abstract 
        except :
            abstract = None

        item['abstract'] = abstract
        srcView = None

        try :   #verifica a existencia do artigo pelo doi
            r = requests.get('https://doi.org/' + item['prism:doi'], allow_redirects=False)
            if r.status_code == 302 :
                srcView = str(r.headers['Location'])
        except :
            srcView = None

        item['view-in-source'] = srcView
        print(srcView)

        meta = {
            'item' : item,
        }

        try :
            url_source_details = 'https://www.scopus.com/source/citescore/{}.uri'.format(item['source-id']) #Obtenção do score
        except :
            try :
                source_id = self.get_source_id(item["prism:issn"])
                url_source_details = 'https://www.scopus.com/source/citescore/{}.uri'.format(source_id) #obtém source_id através do issn
            except :
                url_source_details = None

        headers = {
            'Accept' : 'application/json',
            'referer' : url_source_details
        }

        try :
            yield scrapy.Request(url=url_source_details, headers=headers, callback=self.parse_source_details, meta=meta, dont_filter=True)
        except :
            self.save_error(item)


    def save_error(self, item) : #Realiza o salvamento dos arquivos sem issn e source_id.
        with open('erros.json', 'a') as file : #Adiciona os dados providos de erros ao erros.json
            json.dump(item, file) 


    def get_source_id(self, issn) :  # Busca source_id utilizando issn

        url = "https://api.elsevier.com/content/serial/title/issn/" + issn + "?apiKey=" + self.user_settings['api-key']  # URL onde se localiza o id
        arquivo = urllib.request.urlopen(url)  # abre uma requisição para capturar o arquivo lxml
        texto = str(bs.BeautifulSoup(arquivo, features="lxml"))  # formata o arquivo lxml e transforma em String

        inicio = texto.index("sourceId=") + 9  # define o inicio do id
        final = inicio  # define o inicio como final do id

        for i in range(20) :  # procura o final do id
            if texto[final + i].isnumeric() == False :  # Verifica se é número
                final += i
                break

        id = texto[inicio : final]  # realiza a separação do texto principal
        return id

    def parse_source_details(self, response): #calculo de score provido pelo link com o source_id
        try :
            curr_year = datetime.datetime.now().year
            for year in range(curr_year - 3, curr_year) :
                try :
                    obj = json.loads(response.text)
                    score = [m['rp'] for m in obj['yearInfo'][str(year)]['metricType'] if m['documentType'] == 'all']
                    score = score[0]
                except :
                    score = 0
                response.meta['item']['source-score-{}'.format(year)] = score
            yield response.meta['item']
        except :
            print("Erro no parse_source_details")


    def references_cited(self, doi): #captura de dados detalhados internos e aceso simplificado externamente.
        try:
            url = 'https://api.elsevier.com/content/article/doi/'+doi+'?APIKey=' + self.user_settings['api-key'] #Url correspondente a página contendo dados como referencias, e outras informações que podem ser acessados externamente 
            pagina = urllib.request.urlopen(url)
            conteudo = bs.BeautifulSoup(pagina, features="lxml")
            referencias = conteudo.find_all("xocs:ref-info")
        
            with open('referencias.txt', 'a') as file :
                file.write("\n \n ////////////////"+doi+"//////////////// \n \n") 
                file.write(str(referencias)) 
        except:
            print("Erro ao capturar o artigo referente ao DOI: "+doi)