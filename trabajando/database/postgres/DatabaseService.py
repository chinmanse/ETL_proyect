from sqlalchemy import Table, Column, String, Date, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from database.postgres.models.information import TareaModel
from database.postgres.config import SessionLocal, meta, engine
from database.postgres.models.jobDataConsumptionModel import JobDataConsumptionModel
from database.postgres.models.JobDataRefinedModel import JobDataRefinedModel
import uuid

class DatabaseService():
  def __init__(self, type):
    if(type == 'consumption'):
      self.model = JobDataConsumptionModel
    elif(type == 'refined'):
      self.model = JobDataRefinedModel
    else:
      self.model = None
    try:
      consumption_table = Table(
        'job_data_consumption', meta,
        Column("id", UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4),
        Column("origin", String, nullable=True),
        Column("title", String, nullable=True),
        Column("link", String, nullable=True),
        Column("image", String, nullable=True),
        Column("resume", String, nullable=True),
        Column("date_published", Date, nullable=True),
        Column("author", String, nullable=True),
        Column("segments", JSON, nullable=True),
        Column("created_at", TIMESTAMP, nullable=True),
        Column("updated_at", TIMESTAMP, nullable=True),
      )

      refined_table = Table(
        'job_data_refined', meta,
        Column("id", UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4),
        Column("origin", String, nullable=True),
        Column("title", String, nullable=True),
        Column("link", String, nullable=True),
        Column("image", String, nullable=True),
        Column("resume", String, nullable=True),
        Column("date_published", Date, nullable=True),
        Column("author", String, nullable=True),
        Column("segments", JSON, nullable=True),
        Column("created_at", TIMESTAMP, nullable=True),
        Column("updated_at", TIMESTAMP, nullable=True),
      )

      meta.create_all(engine)
    except Exception as e:
      print(e.args)

  def store_article(self, article):
    try:
      session = SessionLocal()
      tarea_model= self.model()
      tarea_model.map(article)
      session.add(tarea_model)
      session.commit()
      return True
    except Exception as e:
      session.rollback()
      print(e.args[0])
    finally:
      session.close()
    return False
  
  def get_by_title(self, title):
    try:
      session = SessionLocal()
      tareas = session.query(self.model).\
        filter(self.model.title == title).\
        all()
      session.commit()
      return tareas
    except Exception as e:
      session.rollback()
      print(e.args[0])
    finally:
      session.close()
    return None