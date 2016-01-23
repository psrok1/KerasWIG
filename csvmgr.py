import numpy
from datetime import datetime
import os.path
import urllib
from bisect import bisect
#

def isStockInCache(id):
    if os.path.isfile("csvdata/"+id+".csv"):
        return True
    return False

def getStockData(id, force_update=False):
    if not isStockInCache(id) or force_update:
        print "Downloading "+id+"..."
        urllib.urlretrieve("http://stooq.pl/q/d/l/?s="+id+"&i=d", "csvdata/"+id+".csv")

    return numpy.recfromcsv("csvdata/"+id+".csv", delimiter=',')

def getFirstDayFromStock(stockData):
    return stockData["data"][0]

def getLastDayFromStock(stockData):
    return stockData["data"][-1]

def stockDayToDatetime(date):
    return datetime.strptime(date, "%Y-%m-%d")

def filterStockData(stockData, fromDate, toDate):
    dates = [stockDayToDatetime(x) for x in stockData["data"]]
    ai = bisect(dates, fromDate)
    bi = bisect(dates, toDate)

    return stockData[ai:bi+1]

def getPricesFromStock(stockData):
    return stockData["zamkniecie"]