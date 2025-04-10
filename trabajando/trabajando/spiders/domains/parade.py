from trabajando.utils.ManageArticles import ManageArticles
from trabajando.utils.functions import validateDate, convertDate
from trabajando.items import JobItem

class Parade ():
    def __init__(self):
        self.manageArticles = ManageArticles()
        self.origin = 'parade'
        self.manageArticles.load_articles(self.origin)
    def parse(self, response):
        print('EJECUTANDO',self.origin)
        groups  = response.css("section.m-list-hub")
        for group in groups:
            articles = group.css("div.l-grid--item")
            for article in articles:
                title = article.css("h2.m-ellipsis--text::text").get()
                # title = article.css("a::attr(data-component-title)").get()
                link = article.css("a::attr(href)").get()
                image = article.css("img.m-card--image-element::attr(src)").get()
                print('VIENDO', self.origin,title)
                previus = {
                    "title": title,
                    "link": response.urljoin(link),
                    "image": image,
                }
                yield response.follow(link, self.parse_detail, meta=previus)
    def parse_detail(self, response):
        tarea_item = JobItem()
        title = response.meta.get('title')
        link = response.meta.get('link')
        image = response.meta.get('image')
        resume = response.css('div.m-detail-header--dek::text').get()
        date_published = response.css('time::attr(datetime)').get()
        author = response.css('a.m-detail-header--meta-author::text').get()
        segments = response.css('div.m-detail--body p::text').getall()
        tarea_item['origin'] =  self.origin
        tarea_item['title'] = title
        tarea_item['link'] = link
        tarea_item['image'] = image
        tarea_item['resume'] = resume
        tarea_item['date_published'] = date_published
        tarea_item['author'] = author
        tarea_item['segments'] = segments

        yield tarea_item

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

        #     yield tarea_item
        #     # yield {
        #     #     'title': title,
        #     #     'link': link,
        #     #     'image': image,
        #     #     'resume': resume,
        #     #     'date_published': date_published,
        #     #     'author': author,
        #     #     'segments': segments,
        #     # }



        # tarea_item = JobItem()
        # title = response.meta.get('title')
        # link = response.meta.get('link')
        # image = response.meta.get('image')
        # resume = response.css('div.ContentHeaderDek-bIqFFZ::text').get()
        # date_published = response.css('time::attr(datetime)').get()
        # author = response.css('[itemprop="name"] a::text').get()
        # segments = response.css('div.body__inner-container p::text').getall()
        
        # tarea_item['title'] = title
        # tarea_item['link'] = link
        # tarea_item['image'] = image
        # tarea_item['resume'] = resume
        # tarea_item['date_published'] = date_published
        # tarea_item['author'] = author
        # tarea_item['segments'] = segments

        # # date_published = convertDate(date_published)
        # # article_information = {
        # #     'title': title,
        # #     'link': link,
        # #     'image': image,
        # #     'resume': resume,
        # #     'date_published': date_published.isoformat(),
        # #     'author': author,
        # #     'segments': segments,
        # # }
        # # if(not self.manageArticles.article_exist(self.origin, article_information['title'])):
        # #     self.manageArticles.articles[self.origin].append(article_information)
        # # if validateDate(date_published):
        # #     tarea_item['title'] = title
        # #     tarea_item['link'] = link
        # #     tarea_item['image'] = image
        # #     tarea_item['resume'] = resume
        # #     tarea_item['date_published'] = date_published
        # #     tarea_item['author'] = author
        # #     tarea_item['segments'] = segments

        # yield tarea_item
