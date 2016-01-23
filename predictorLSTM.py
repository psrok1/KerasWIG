from keras.models import Sequential
from predictorModel import PredictorModel
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM


class PredictorLSTM(PredictorModel):
    def __init__(self, model_name):
        PredictorModel.__init__(self, model_name, model_type="LSTM")

    def createModel(self, csv_id, desc=""):
        self.csv_id = csv_id
        self.last_day = None
        self.batch_size = 32
        self.nb_epoch = 10
        max_features = 5000

        self.description = desc

        self.model = Sequential()
        self.model.add(Embedding(max_features, 128, input_length=self.days_seq))
        self.model.add(LSTM(128))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))

        print "Creating LSTM model "+self.model_name+"..."

        self.model.compile(loss='binary_crossentropy',
              optimizer='adam',
              class_mode="binary")