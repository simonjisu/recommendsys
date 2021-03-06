# -*- coding: utf-8 -*-

from data import settings
import sys
import pandas as pd
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# sqlalchemy data넣을 때 쓰는것들
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()

engine = sqlalchemy.create_engine(settings.DB_TYPE + settings.DB_USER + ":" + settings.DB_PASSWORD + "@" +
                                  settings.DB_URL + ":" + settings.DB_PORT + "/" + settings.DB_NAME, echo=settings.QUERY_ECHO)

# ['app_id', 'app_name', 'review_id', 'title', 'author', 'author_url', 'version', 'rating', 'review', 'category']

class Reviews(Base):
    # table name:
    __tablename__ = 'reviews'
    # table column:
    idx = Column(Integer, primary_key=True)
    app_id = Column(String)
    app_name = Column(String)
    review_id = Column(String)
    title = Column(String)
    author = Column(String)
    author_url = Column(String)
    version = Column(String)
    rating = Column(String)
    review = Column(String)
    category = Column(String)

Base.metadata.create_all(engine)

with open('new_app_id_list.txt', 'r') as file:
    app_ids = file.readlines()

app_id_list = []
for i in app_ids:
    app_id_list.append(i.strip())

file_len = len(app_id_list)

start = [i for i in range(1, file_len, 100)]
if file_len % 100 == 0:
    end = [i for i in range(100, file_len+1, 100)]
else:
    end = [i for i in range(100, file_len, 100)] + [file_len]

file_list = []
for i,j in zip(start, end):
    file_list.append('./data/n_reviews[{0}-{1}].txt'.format(i, j))

len_file_list = len(file_list)

if sys.argv[1] == 'all':
    print('please insert 1 ~ {}'.format(len_file_list))
elif len(sys.argv) <= 2:
    if (int(sys.argv[1]) <= len_file_list) & (int(sys.argv[1]) > 0):
        idx = int(sys.argv[1])
        file_list = file_list[:idx]
    else:
        print('only can write 1 ~ {}, int'.format(len_file_list))
else:
    if (int(sys.argv[2]) <= len_file_list) & (int(sys.argv[1]) < int(sys.argv[2])) & (int(sys.argv[1]) < len_file_list):
        idx1 = int(sys.argv[1])
        idx2 = int(sys.argv[2])
        file_list = file_list[idx1:idx2]
    else:
        print('2nd number only can write 1 ~ {0}, int, 1st one must be smaller than 2nd one, from 0 ~ {1}'.format(len_file_list, len_file_list-1))


def add_Data(file_list):
    data_list = []
    for file_path in file_list:
        try:
            data = pd.read_csv(file_path, sep='\t', dtype=str)
        except:
            data = pd.read_csv(file_path, sep='\t', dtype=str, encoding='utf8', engine='python')
        for i in data.index:
            data_list.append(Reviews(
                app_id=data.loc[i, 'app_id'],
                app_name=data.loc[i, 'app_name'],
                review_id=data.loc[i, 'review_id'],
                title=data.loc[i, 'title'],
                author=data.loc[i, 'author'],
                author_url=data.loc[i, 'author_url'],
                version=data.loc[i, 'version'],
                rating=data.loc[i, 'rating'],
                review=data.loc[i, 'review'],
                category=data.loc[i, 'category'],
            ))
        print(file_path, 'complete!!')
    return data_list

data_list = add_Data(file_list)
Session.configure(bind=engine)  # once engine is available
session = Session()
session.add_all(data_list)  # list로 한 번에 넣기
session.commit()