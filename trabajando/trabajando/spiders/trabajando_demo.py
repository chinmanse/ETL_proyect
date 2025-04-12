import scrapy
from datetime import datetime
from trabajando.items import JobItem 
import uuid
from trabajando.spiders.data_web import CITIES , BASE_URLS, ALLOWED_DOMAINS #, HEADERS
import time 
from trabajando.spiders.domains.theNextWeb import TheNextWeb
from trabajando.spiders.domains.parade import Parade
from trabajando.spiders.domains.wired import Wired
from trabajando.spiders.domains.cnet import Cnet

class TrabajandoDemoSpider(scrapy.Spider):
    name = "trabajando_demo"
    allowed_domains = ALLOWED_DOMAINS 
    start_urls = []
    keep_paginas = []
    # max_paginas = 7
    service = None

    def start_requests(self):
            """Generate initial requests with proper user agent headers."""
            self.nextService = TheNextWeb()
            self.paradeService = Parade()
            self.wiredService = Wired()
            self.CnetService = Cnet()
            for url in BASE_URLS:
                if 'thenextweb.com' in url:
                    yield scrapy.Request(
                            url = url,
                            callback=self.parse,
                            # headers=HEADERS
                            )
                elif 'parade.com' in url:
                    yield scrapy.Request(
                            url = url,
                            callback=self.parse,
                            # headers=HEADERS
                            )
                elif 'www.wired.com' in url:
                    yield scrapy.Request(
                            url = url,
                            callback=self.parse,
                            # headers=HEADERS
                            )
                if 'www.cnet.com' in url:
                    yield scrapy.Request(
                            url = url,
                            callback=self.parse,
                            # headers=HEADERS
                            )
                time.sleep(1)
                    
    def parse(self, response):
        

        if response.status != 200:
            self.logger.warning(f"Failed to fetch {response.url}: {response.status}")
            return
        
        print("Parsing")
        
        url_site = response.url
        if 'thenextweb.com' in url_site:
            yield from self.nextService.parse(response)
        elif 'parade.com' in url_site:
            yield from self.paradeService.parse(response)
        elif 'www.wired.com' in url_site:
            yield from self.wiredService.parse(response)
        elif 'www.cnet.com' in url_site:
            yield from self.CnetService.parse(response)
        # yield from self.service.parse(response)

        # if 'trabajando' in url_site:
        #     job_posting = response.css('div.views-row') 
            
        #     for job in job_posting:

        #         relative_url = job.css('h2.views-field-title a ::attr(href)').get()
        #         job_description_url =  'https://www.trabajando.com.bo' + relative_url  

        #         yield response.follow(job_description_url, callback=self.parse_pagina_specifica)

        # elif 'trabajito' in url_site:
            
        #     job_posting = response.css('div.job-block') 

        
        #     for job in job_posting:

        #         relative_url = job.css('div.inner-box div.content h4 ::attr(href)').get(),
        #         job_description_url =  relative_url[0]  

        #         yield response.follow(job_description_url, callback=self.parse_pagina_specifica)


        # # pagination
        # next_page = ''

        # if 'trabajando' in url_site:

        #     tmp_num = len(self.keep_paginas) + 1  # Increment the page number

        #     if tmp_num <= self.max_paginas:
        #         next_page = f"{url_site}?page={tmp_num}"
        #         if tmp_num not in self.keep_paginas:
        #             self.keep_paginas.append(tmp_num)
        #             yield response.follow(next_page, callback=self.parse)

        # if 'trabajito' in url_site:
        #     next_page = response.css('div.ls-pagination ul.pagination.bravo-pagination li')
        #     last_li_class = next_page[-1].css('li ::attr(class)').get()

        #     if not last_li_class:
        #         next_page = next_page[-1].css('li ::attr(href)').get()
        #     else:
        #         print("End pagination")
        #     #next_page = response.urljoin(next_page)

        # yield response.follow(next_page, callback=self.parse)


    def parse_pagina_specifica(self, response):
        job_item = JobItem()
        url_site = response.url

        if 'trabajando' in url_site:

            wrapper = response.css('div.region-content')

            job_item['data_id'] = str(uuid.uuid4()),
            job_item['url'] = response.url,
            job_item['title'] = wrapper.css('h1.trabajando-page-header span ::text').get(),
            job_item['company'] = wrapper.css('div.views-field-field-nombre-empresa div.field-content a ::text').get(),
            job_item['location'] = wrapper.css("div.views-field-field-ubicacion-del-empleo div.field-content ::text").get(),
            job_item['type_job'] = wrapper.css('div.views-field-field-tipo-empleo div.field-content ::text').get(),
            job_item['date_published'] = wrapper.css("div.views-field-created span.field-content time ::attr(datetime)").get(),
            job_item['date_expiration'] = wrapper.css("div.views-field-field-fecha-empleo-1  div.field-content ::text").get(),
            job_item['job_description'] = wrapper.css('div.field--type-text-with-summary div.field--item p ::text').getall()
            job_item['date_saved'] = datetime.now().isoformat()
            
            yield job_item 

        elif 'trabajito' in url_site:
    
            wrapper = response.css('section.job-detail-section') 
            job_desc = wrapper.css('ul.job-info li')
            job_overview = wrapper.css("aside.sidebar ul.job-overview li")

            job_item['data_id'] = str(uuid.uuid4()),
            job_item['url'] = response.url,
            job_item['title'] = wrapper.css('h4 ::text').get(),
            job_item['company'] = wrapper.css('aside.sidebar div.widget-content div.company-title h5 ::text').get(),
            job_item['location'] = job_desc[1].css("li ::text").get(), 
            job_item['type_job'] = job_desc[0].css('li ::text').get(),
            job_item['job_description'] = wrapper.css('div.job-detail.only-text p ::text').getall()
            job_item['date_published'] = job_desc[2].css("li ::text").get(),
            job_item['date_expiration'] = job_overview[1].css("li span ::text").get(),
            job_item['date_saved'] = datetime.now().isoformat()

    
            yield job_item 
