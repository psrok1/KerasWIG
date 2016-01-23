import numpy
from datetime import datetime
import os.path
import urllib
#

def isStockInCache(id):
	if os.path.isfile("csvdata/"+id+".csv")
		return True
    return False

def getStockData(id, force_update=False):
	if not isStockInCache(id) or force_update:
		urllib.urlretrieve("http://stooq.pl/q/d/l/?s="+id+"&i=d", "csvdata/"+id+".csv")	
    return numpy.recfromcsv("csvdata/"+id+".csv", delimiter=',')

# Nothing to do!
def getLastDayFromStock(stockData):
    return stockData["data"][-1]

def stockDayToDatetime(date):
    return datetime.strptime(date, "%Y-%m-%d")

def getPricesFromStock(stockData):
    return stockData["zamkniecie"]