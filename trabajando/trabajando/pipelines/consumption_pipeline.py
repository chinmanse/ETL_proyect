from .base_pipeline import TrabajandoPipeline
from datetime import datetime
import re 
from urllib.parse import urlparse
from dateutil import parser
import os 
from dotenv import load_dotenv
import json
from scrapy.utils.project import get_project_settings
from database.postgres.DatabaseService import DatabaseService

class ConsumptionPipeline(TrabajandoPipeline):

    def __init__(self) -> None:
            self.service = DatabaseService('consumption')
            settings = get_project_settings()
            self.landing_zone = settings.get('CONSUMPTION_ZONE')
            # # information Connection with DB 
            # # hostname = os.getenv('DB_HOST') 
            # # username = os.getenv('DB_USER') 
            # # password = os.getenv('DB_PASSWORD') 
            # # database = os.getenv('DB_DATABASE') 
            # hostname = '127.0.0.1'
            # username = 'admin'
            # password = 'root'
            # database = 'modulo2'
            # port = '5432'
            
            # self.connection = psycopg2.connect(host=hostname, user=username, password='root', dbname=database, port=port)

            # self.cur = self.connection.cursor()

            # self.cur.execute("""
            #                  CREATE TABLE IF NOT EXISTS job_data_consumption (
            #                  id serial PRIMARY KEY,
            #                  url text,
            #                  title text,
            #                  company text,
            #                  location text,
            #                  type_job text,
            #                  job_description text,
            #                  date_published text,
            #                  date_expiration text, 
            #                  date_saved_iso text
            #                  )
            #                  """
            #                  )

            # self.connection.commit()

    def open_spider(self, spider):
        self.items = []
        settings = get_project_settings()
        self.consumption_zone = settings.get('CONSUMPTION_ZONE')
        self.filename = self.get_filename(spider, None, 'consumption') 



    def process_item(self, item, spider):
        
        settings = get_project_settings()
        landing_zone = settings.get('CONSUMPTION_ZONE')

        filename = self.get_filename(spider, item, 'consumption')

        transformed_item = self.transform_item(item)

        self.save_to_zone(item, landing_zone, filename)
        
        return  transformed_item


    def transform_item(self, item):

        """ Here we can perform all the transformation or even separate it into another file 
         for readability puroposes."""

        # Convert the item to a dictionary first
        transformed = dict(item)
        
        tareas = self.service.get_by_title(transformed['title'])

        if tareas:
            print(f"THis item: {transformed['title']} is already in the DB.")
            # raise Exception(f"The item is already in the DB.")
        else:
            self.service.store_article(transformed)
        return transformed
    
    def close_spider(self, spider):
        os.makedirs(self.landing_zone, exist_ok=True)
        path = os.path.join(self.landing_zone, self.filename)

        # save all items to one JSON file
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)

