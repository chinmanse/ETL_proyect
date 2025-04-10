from sqlalchemy import Column, String, DateTime, JSON, Date, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database.postgres.config import Config
from datetime import  datetime, timezone
import uuid

def dateUtc():
  return datetime.now(timezone.utc)

class JobDataConsumptionModel(Config):
  __tablename__ = "job_data_consumption"

  id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid1)
  origin = Column(String)
  title = Column(String)
  link = Column(String)
  image = Column(String)
  resume = Column(String)
  date_published = Column(Date)
  author = Column(String)
  segments = Column(JSON)
  created_at = Column(TIMESTAMP, default=dateUtc)
  updated_at = Column(DateTime, onupdate=func.now())
  
  def map(self, request):
    self.origin = request['origin']
    self.title = request['title']
    self.link = request['link']
    self.image = request['image']
    self.resume = request['resume']
    self.date_published = request['date_published']
    self.author = request['author']
    self.segments = request['segments']
