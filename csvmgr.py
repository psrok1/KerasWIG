import numpy
from datetime import datetime

#

def isStockInCache(id):
    # TODO: check if csvdata has file csvdata/#id#.csv?
    return False

def getStockData(id, force_update=False):
    # TODO: if not isStockInCache(id) or force_update - download to file csvdata/#id#.csv
    # TODO: if stooq doesn't have data - go ahead, throw exception!
    # http://stooq.pl/q/d/l/?s=eur&i=d
    # Where eur needs to be replaced by id
    return numpy.recfromcsv('dbc_d.csv', delimiter=',')

# Nothing to do!
def getLastDayFromStock(stockData):
    return stockData["data"][-1]

def stockDayToDatetime(date):
    return datetime.strptime(date, "%Y-%m-%d")

def getPricesFromStock(stockData):
    return stockData["zamkniecie"]