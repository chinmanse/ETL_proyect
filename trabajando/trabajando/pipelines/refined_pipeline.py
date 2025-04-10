from database.postgres.DatabaseService import DatabaseService
from .base_pipeline import TrabajandoPipeline, get_project_settings

from datetime import datetime
from itemadapter import ItemAdapter
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse
import os
import re 
from dateutil import parser 
import json

class RefinedPipeline(TrabajandoPipeline):
    def __init__(self) -> None:
            self.service = DatabaseService('refined')
            settings = get_project_settings()
            self.landing_zone = settings.get('CONSUMPTION_ZONE')
            # information Connection with DB 
            # hostname = os.getenv('DB_HOST') 
            # username = os.getenv('DB_USER') 
            # password = os.getenv('DB_PASSWORD') 
            # database = os.getenv('DB_DATABASE') 
            
            # self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

            # self.cur = self.connection.cursor()

            # self.cur.execute("""
            #                  CREATE TABLE IF NOT EXISTS job_data_refined (
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
            #                  """)

            # self.connection.commit()

    def open_spider(self, spider):
        self.items = []
        settings = get_project_settings()
        self.consumption_zone = settings.get('REFINED_ZONE')
        self.filename = self.get_filename(spider, None, 'refined') 

    def process_item(self, item, spider):
        
        settings = get_project_settings()
        refined_zone = settings.get('REFINED_ZONE')

        transformed_item = self.transform_item(item)

        filename = self.get_filename(spider, item, 'refined')

        self.save_to_zone(transformed_item, refined_zone, filename)

        return transformed_item

    def transform_item(self, item):

        """ Here we can perform all the transformation or even separate it into another file 
         for readability puroposes."""

        # Convert the item to a dictionary first
        transformed = dict(item)
        
        # Convert all fields to lowercase
        for key, value in transformed.items():
            if transformed[key] and isinstance(transformed[key], str):
                transformed[key] = transformed[key].lower()
        
        # Convert empty strings to None
        for field in transformed:
            if transformed[field] == "" or transformed[field] == "null":
                transformed[field] = None
        cleaned_segments = []
        if 'segments' in transformed:
            if isinstance(transformed['segments'], list):
                for segment in transformed['segments']:
                    segment = self.clean_text(segment)
                    cleaned_segments.append(segment)

        if 'url' in transformed and transformed['url']:
            transformed['domain'] = self.extract_domain(transformed['url'])
        
        
        res = self.service.get_by_title(transformed['title'])

        if res:
            print(f"THis item: {transformed['title']} is already in the DB.")
            # raise Exception(f"The item is already in the DB.")

        else:
            self.service.store_article(transformed)

        return transformed
    
    def close_connection(self, spider):
        self.cur.close()
        self.connection()
                
    def clean_text(self, text):

        """Remove all non-alphanumeric characters from text"""

        if not text:
            return text
            
        # Keep only alphanumeric characters (a-z, A-Z, 0-9)
        return re.sub(r'[^a-zA-Z0-9]', ' ', text)
    
    def convert_date_fields(self, transformed):

        """Convert date strings to datetime objects"""

        date_fields = ['date_published', 'date_expiration']
        
        for field in date_fields:
            if field in transformed and transformed[field]:
                try:
                    # Try to parse the date string
                    parsed_date = parser.parse(transformed[field])
                    transformed[field] = parsed_date.isoformat()
                except (ValueError, TypeError):
                    # If parsing fails, set as "not supported"
                    transformed[field] = "not supported"
        

    def extract_domain(self, url):

        """Extract domain name from URL"""

        try:
            parsed_url = urlparse(url)
            # Get domain with subdomain (e.g., 'trabajito.com.bo')
            domain = parsed_url.netloc
            return domain
        except:
            return None

    def close_spider(self, spider):
        os.makedirs(self.landing_zone, exist_ok=True)
        path = os.path.join(self.landing_zone, self.filename)

        # save all items to one JSON file
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
