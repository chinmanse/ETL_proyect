from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
#from dotenv import find_dotenv

host = '127.0.0.1'
port = '5432'
user = 'admin'
password = 'root'
database = 'modulo2'
SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{database}"
print("CONEXION A BASE DE DATOS ",SQLALCHEMY_DATABASE_URI)
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
meta = MetaData()

Config = declarative_base()