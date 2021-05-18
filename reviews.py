import csv
import os
import psycopg2
from psycopg2 import Error
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:bookworm3@bw-3.cykhepzbvf9e.ap-south-1.rds.amazonaws.com:5432/bookwormdb')
#engine = create_engine("postgres://fmtlseqqcudqpx:e215c3120ed02f8b0e064ee2795ad2daaf53ed2c8d942997402e0b5fe067a50e@ec2-54-88-130-244.compute-1.amazonaws.com:5432/dama885492rtun")
db = scoped_session(sessionmaker(bind=engine))
#db.execute("CREATE TABLE IF NOT EXISTS allbook (isbn VARCHAR ( 20 ) PRIMARY KEY,title VARCHAR ( 100 ) NOT NULL,author VARCHAR ( 100 ) NOT NULL,year VARCHAR ( 4 ) NOT NULL);")
db.execute("CREATE TABLE IF NOT EXISTS review(email VARCHAR ( 50 ),comment VARCHAR ( 100 ) NOT NULL,bookid VARCHAR ( 25 ) PRIMARY KEY NOT NULL,rating INT NOT NULL);")
db.commit();
# query="%"+"J"+"%"
# allbook=db.execute("SELECT * FROM allbook where author like :query order by title",{"query": query}).fetchall()
# print(allbook)