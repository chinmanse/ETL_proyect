from trabajando.utils.ManageArticles import ManageArticles
from trabajando.utils.functions import validateDate, convertDate
from trabajando.items import JobItem

class Wired ():
    def __init__(self):
        self.manageArticles = ManageArticles()
        self.origin = 'wired'
        self.manageArticles.load_articles(self.origin)
    def parse(self, response):
        print('EJECUTANDO',self.origin)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(response)
        print("SABIENDO SE",response.text)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        groups  = response.css("div.summary-list__items")
        print("SABIENDO SE",groups)
        for group in groups:
            articles = group.css("div.summary-item--article")
            for article in articles:
                title = article.css("h3.summary-item__hed::text").get()
                link = article.css("a.summary-item-tracking__hed-link::attr(href)").get()
                image = article.css("img.responsive-image__image::attr(src)").get()
                if not title:
                    continue
                previus = {
                    "title": title,
                    "link": response.urljoin(link),  # Convierte URL relativa en absoluta
                    "image": image,
                }
                if(link):
                    yield response.follow(link, self.parse_detail, meta=previus)
                else:
                    yield {
                        "title": title,
                        "link": response.urljoin(link),
                        "image": image,
                    }
    def parse_detail(self, response):
        tarea_item = JobItem()
        title = response.meta.get('title')
        link = response.meta.get('link')
        image = response.meta.get('image')
        resume = response.css('div.ContentHeaderDek-bIqFFZ::text').get()
        date_published = response.css('time::attr(datetime)').get()
        author = response.css('[itemprop="name"] a::text').get()
        segments = response.css('div.body__inner-container p::text').getall()
        tarea_item['origin'] =  self.origin
        tarea_item['title'] = title
        tarea_item['link'] = link
        tarea_item['image'] = image
        tarea_item['resume'] = resume
        tarea_item['date_published'] = date_published
        tarea_item['author'] = author
        tarea_item['segments'] = segments

        # date_published = convertDate(date_published)
        # article_information = {
        #     'title': title,
        #     'link': link,
        #     'image': image,
        #     'resume': resume,
        #     'date_published': date_published.isoformat(),
        #     'author': author,
        #     'segments': segments,
        # }
        # if(not self.manageArticles.article_exist(self.origin, article_information['title'])):
        #     self.manageArticles.articles[self.origin].append(article_information)
        # if validateDate(date_published):
        #     tarea_item['title'] = title
        #     tarea_item['link'] = link
        #     tarea_item['image'] = image
        #     tarea_item['resume'] = resume
        #     tarea_item['date_published'] = date_published
        #     tarea_item['author'] = author
        #     tarea_item['segments'] = segments

        yield tarea_item
