from trabajando.utils.ManageArticles import ManageArticles
from trabajando.utils.functions import validateDate, convertDate
from trabajando.items import JobItem

class Cnet ():
    def __init__(self):
        self.manageArticles = ManageArticles()
        self.origin = 'cnet'
        self.manageArticles.load_articles(self.origin)
    def parse(self, response):
        print('EJECUTANDO',self.origin)
        articles = response.css('[data-name="article_link|latest_stories_neon"] a')
        for article in articles:
            image = article.css("img::attr(src)").get()
            title = article.css("h3::text").get()
            link = article.attrib.get('href')
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
        resume = response.css('p.u-speakableText-dek.c-contentHeader_description.g-outer-spacing-top-small::text').get()
        date_published = response.css('time::text').get()
        author = response.css('span.c-globalAuthor_name::text').get()
        segments = response.css('article p::text').getall()
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
