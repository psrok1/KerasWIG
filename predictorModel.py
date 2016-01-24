from keras.preprocessing import sequence
from keras.models import model_from_yaml
from os.path import isfile
import yaml
import csvmgr
import numpy
from math import floor
from datetime import datetime, timedelta
import sklearn.cross_validation as crossval

DIR_MODELS = "models/"

class PredictorModel:
    def __init__(self, model_name, model_type=""):
        self.model_name = model_name
        self.model_type = model_type
        self.days_seq = 20
        self.last_day = None
        pass

    def loadModel(self):
        global DIR_MODELS
        if(isfile(DIR_MODELS+self.model_name+".yml")):
            self.model = model_from_yaml(open(DIR_MODELS+self.model_name+'_m.yml').read())
            self.model.load_weights(DIR_MODELS+self.model_name+'.h5')

            stream = file(DIR_MODELS+self.model_name+'.yml', 'r')
            model_description = yaml.load(stream)

            self.csv_id = model_description["csv_id"]
            self.last_day = model_description["last_day"]
            self.batch_size = model_description["batch_size"]
            self.nb_epoch = model_description["nb_epoch"]
            self.model_type = model_description["model_type"]
            self.description = model_description["description"]
            return True

        return False

    def saveModel(self):
        global DIR_MODELS

        model_yaml = self.model.to_yaml()
        open(DIR_MODELS+self.model_name+"_m.yml", "w").write(model_yaml)
        self.model.save_weights(DIR_MODELS+self.model_name+'.h5', overwrite=True)

        stream = file(DIR_MODELS+self.model_name+'.yml', 'w')
        model_description = dict(
            csv_id = str(self.csv_id),
            last_day = str(self.last_day),
            batch_size = self.batch_size,
            nb_epoch = self.nb_epoch,
            model_type = str(self.model_type),
            description = str(self.description)
        )
        print model_description
        desc_yaml = yaml.dump(model_description, default_flow_style=True)
        open(DIR_MODELS+self.model_name+".yml", "w").write(desc_yaml)

    def __getStockData(self, from_date=None, to_date=None, fresh=False):
        maxlen = self.days_seq
        stockData = csvmgr.getStockData(self.csv_id, force_update=fresh)

        if from_date is None:
            from_date = csvmgr.stockDayToDatetime(csvmgr.getFirstDayFromStock(stockData))
        if to_date is None:
            to_date = csvmgr.stockDayToDatetime(csvmgr.getLastDayFromStock(stockData))

        if (to_date-from_date) <= timedelta(maxlen):
            from_date -= timedelta(maxlen+20)

        stockData = csvmgr.filterStockData(stockData, from_date, to_date)

        print "Getting stock data from "+csvmgr.getFirstDayFromStock(stockData) + " to " + csvmgr.getLastDayFromStock(stockData)

        stockValues = csvmgr.getPricesFromStock(stockData)

        x_data = numpy.array([stockValues[i:i+maxlen] for i in xrange(len(stockValues)-maxlen)])
        y_data = numpy.array([floor(stockValues[i]/stockValues[i-1]) for i in xrange(maxlen,len(stockValues))])

        return stockData, x_data, y_data

    def feedWithStockData(self, limit_date = None, fresh = False):
        if self.last_day is None:
            stockData, x_data, y_data = self.__getStockData(to_date = limit_date, fresh=fresh)
        else:
            last_date = csvmgr.stockDayToDatetime(self.last_day)
            last_date += timedelta(1)
            stockData, x_data, y_data = self.__getStockData(from_date = last_date, to_date = limit_date, fresh=fresh)

        print "Fitting..."
        self.model.fit(x_data, y_data, batch_size=self.batch_size, nb_epoch=self.nb_epoch,
                        show_accuracy=True)

        self.last_day = csvmgr.getLastDayFromStock(stockData)

    def testWithStockData(self, from_date = None, fresh = False):
        if self.last_day is None:
            print "No data in model!"
            return

        stockData, x_data, y_data = self.__getStockData(from_date = from_date, fresh=fresh)

        print "Testing..."
        score, acc = self.model.evaluate(x_data, y_data,
                            batch_size=self.batch_size,
                            show_accuracy=True)
        print "Score: "+str(score)
        print "Accuracy: "+str(acc)