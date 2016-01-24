from predictorLSTM import *
from predictorLSTM3 import *
from predictorMLP import *
from predictorGRU import *
from predictorRegular import *

predictors = {
    "LSTM": PredictorLSTM,
    "LSTM3": PredictorLSTM3,
    "MLP": PredictorMLP,
    "GRU": PredictorGRU,
    "Regular": PredictorRegular
}