import os
import os.path
import pandas as pd
from sqlalchemy import create_engine
from queue import Queue
from threading import Thread, Lock
from datetime import date
from lib import scrap_by_keyword


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            keyword = self.queue.get()
            try:
                scrap_by_keyword(keyword)
            finally:
                self.queue.task_done()


def scrap_all(keywords):
    df = pd.DataFrame()
    for keyword in keywords:
        df = scrap_by_keyword(keyword, df)
    engine = create_engine('sqlite:///game.db')
    df.to_sql('games', con=engine, if_exists='append', index=False)


def read_keywords():
    with open('./words.txt') as reader:
        s = reader.read()
        return s.strip().split()


if __name__ == "__main__":
    queue = Queue()
    for x in range(8):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
    keywords = read_keywords()
    for keyword in keywords:
        queue.put(keyword)
    queue.join()

    today = date.today()
    dbName = 'db/game_{}.db'.format(today)
    if os.path.isfile(dbName):
        os.remove(dbName)
    engine = create_engine('sqlite:///{}'.format(dbName))
    df = pd.DataFrame()
    dir = './files/{}'.format(today)
    for fileName in os.listdir(dir):
        print(fileName)
        if len(fileName) > 2:
            filepath = '{}/{}'.format(dir, fileName)
            df = df.append(pd.read_excel(filepath))
    df.to_sql('games', con=engine, if_exists='append', index=False)
    df.to_excel('{}.xlsx'.format(today))
