from keras.models import Sequential
from predictorModel import PredictorModel
from keras.layers.core import Dense, Dropout, Activation

class PredictorMLP(PredictorModel):
    def __init__(self, model_name):
        PredictorModel.__init__(self, model_name, model_type="MLP")

    def createModel(self, csv_id, desc=""):
        self.csv_id = csv_id
        self.last_day = None
        self.batch_size = 32
        self.nb_epoch = 10
        max_features = 5000

        self.description = desc

        self.model = Sequential()
        self.model.add(Dense(64, input_dim=20, init='uniform', activation='sigmoid'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(64, init='uniform', activation='sigmoid'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1))

        print "Creating MLP model "+self.model_name+"..."

        self.model.compile(loss='binary_crossentropy',
              optimizer='adam',
              class_mode="binary")