from trabajando.utils.ManageArticles import ManageArticles
from trabajando.utils.functions import validateDate, convertDate
from trabajando.items import JobItem

class TheNextWeb ():
    def __init__(self):
        self.manageArticles = ManageArticles()
        self.origin = 'thenextweb'
        self.manageArticles.load_articles(self.origin)
    def parse(self, response):
        print('EJECUTANDO',self.origin)
        for article in response.css("article.c-listArticle"):
            article_title = article.css("h2.c-listArticle__heading") 
            title = article_title.css('a::text').get()
            link = article_title.css("a::attr(href)").get()
            image = article.css("figure.c-listArticle__image")
            image = image.css('img::attr(src)').get()
            print('VIENDO', self.origin,title)
            if(not title):
                continue
            yield response.follow(link, self.parse_detail, meta={'title': title, 'link': link, 'image': image})
    def parse_detail(self, response):
        tarea_item = JobItem()
        title = response.meta.get('title')
        link = response.meta.get('link')
        image = response.meta.get('image')
        resume = response.css('p.c-header__intro::text').get()
        date_published = response.css('time::attr(datetime)').get()
        author = response.css('span.c-article__authorName::text').get()
        segments = response.css('#article-main-content p::text').getall()
        tarea_item['origin'] =  self.origin
        tarea_item['title'] =  title
        tarea_item['link'] =  link
        tarea_item['image'] =  image
        tarea_item['resume'] =  resume
        tarea_item['date_published'] =  date_published
        tarea_item['author'] =  author
        tarea_item['segments'] =  segments
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
        yield tarea_item

        # if(validateDate(date_published)):
            
        #     tarea_item['title'] = title
        #     tarea_item['link'] = link
        #     tarea_item['image'] = image
        #     tarea_item['resume'] = resume
        #     tarea_item['date_published'] = date_published
        #     tarea_item['author'] = author
        #     tarea_item['segments'] = segments

        #     yield tarea_item


        # tarea_item = JobItem()
        # title = response.meta.get('title')
        # link = response.meta.get('link')
        # image = response.meta.get('image')
        # resume = response.css('div.ContentHeaderDek-bIqFFZ::text').get()
        # date_published = response.css('time::attr(datetime)').get()
        # date_published = convertDate(date_published)
        # author = response.css('[itemprop="name"] a::text').get()
        # segments = response.css('div.body__inner-container p::text').getall()
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

        #     yield tarea_item
