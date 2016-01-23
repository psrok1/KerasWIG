from keras.preprocessing import sequence
from keras.models import model_from_yaml
from os.path import isfile
import yaml
import csvmgr
import numpy
from math import floor
import sklearn.cross_validation as crossval

DIR_MODELS = "models/"

class PredictorModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.days_seq = 20
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
            return True

        return False

    def saveModel(self):
        global DIR_MODELS

        model_yaml = self.model.to_yaml()
        open(DIR_MODELS+self.model_name+"_m.yml").write(model_yaml)
        self.model.save_weights(DIR_MODELS+self.model_name+'.h5')

        stream = file(DIR_MODELS+self.model_name+'.yml', 'w')
        model_description = {
            "csv_id": self.csv_id,
            "last_day": self.last_day,
            "batch_size": self.batch_size,
            "nb_epoch": self.nb_epoch
        }
        yaml.dump(model_description, stream)

    def __getStockData(self):
        maxlen = self.days_seq
        stockData = None   # get stock data
        stockValues = None # zamkniecie

        x_data = numpy.array([stockValues[i:i+maxlen] for i in xrange(len(stockValues)-maxlen)])
        y_data = numpy.array([floor(stockValues[i]/stockValues[i-1]) for i in xrange(maxlen,len(stockValues))])

        x_train, x_test, y_train, y_test = crossval.train_test_split(x_data, y_data, test_size=0.2, random_state=0)

        x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
        x_test = sequence.pad_sequences(x_test, maxlen=maxlen)

        return x_train, x_test, y_train, y_test

    def feedWithStockData(self):
        x_train, x_test, y_train, y_test = self.__getStockData()

        self.model.fit(x_train, y_train, batch_size=self.batch_size, nb_epoch=self.nb_epoch,
                        validation_data=(x_test, y_test), show_accuracy=True)