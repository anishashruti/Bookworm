import csv
import os
import psycopg2
from psycopg2 import Error
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:bookworm3@bw-3.cykhepzbvf9e.ap-south-1.rds.amazonaws.com:5432/bookwormdb')
#engine = create_engine("postgres://fmtlseqqcudqpx:e215c3120ed02f8b0e064ee2795ad2daaf53ed2c8d942997402e0b5fe067a50e@ec2-54-88-130-244.compute-1.amazonaws.com:5432/dama885492rtun")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    db.execute("CREATE TABLE IF NOT EXISTS allbook (isbn VARCHAR ( 20 ) PRIMARY KEY,title VARCHAR ( 100 ) NOT NULL,author VARCHAR ( 100 ) NOT NULL,year VARCHAR ( 4 ) NOT NULL);")
    for isbn, title, author,year in reader:
        db.execute("INSERT INTO allbook (isbn, title, author,year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author,"year":year})
        print(f"Added book no. {isbn} having title {title},author as {author} released in {year} .")
    db.commit()

if __name__ == "__main__":
    main()
