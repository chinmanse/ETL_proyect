import json
from datetime import datetime
class ManageArticles():
    def __init__(self):
        self.file = 'articles.json'
        self.articles = {}
    def load_articles(self, origin):
        try:
            with open(self.file, 'r') as f:
                self.articles = json.load(f) 
        except:
            self.articles = {}
        if(not origin in self.articles):
            self.articles[origin] = []
        
    def save_articles(self):
        with open(self.file, 'w') as f:
            json.dump(self.articles, f, indent=4)

    def article_exist(self, origin, title):
        for article in self.articles[origin]:
            if(title in article):
                return article.title == title
        return False

    def should_scrape(self, origin, title, date_published):
        if origin in self.articles:
            for article in self.articles[origin]:
                if(article['title'] == title):
                    stored_date = datetime.fromisoformat(article['date_published'])
                    return date_published > stored_date
        return True