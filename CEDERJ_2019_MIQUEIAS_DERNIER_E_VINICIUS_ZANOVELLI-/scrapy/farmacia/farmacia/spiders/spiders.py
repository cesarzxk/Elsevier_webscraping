import scrapy
import json

class BaseSpider(scrapy.spiders.Spider):
    def __init__(self,*args,usersettings='',outputfile='',tipo=['json'],**kwargs):
        self.user_settings = {}
        self.outputfile = outputfile
        self.tipo = tipo
        if(usersettings):
            with open(usersettings,encoding="utf-8") as json_file:
                data = json.load(json_file)
                self.user_settings = data
        super().__init__(*args, **kwargs)
