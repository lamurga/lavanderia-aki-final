# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:postgres@0.tcp.ngrok.io:15992/lavanderiadb')
Session = sessionmaker(bind=engine)
Base = declarative_base()
