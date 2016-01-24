#!/bin/bash

python keraswig.py create pkn_lstm LSTM pkn --description "PKN LSTM complete model"
python keraswig.py create pkn_part LSTM pkn --description "PKN LSTM partial model" --limit-date 2015-11-01
python keraswig.py create pkn_lstm3 LSTM3 pkn --description "PKN LSTM3 complete model"
python keraswig.py create pkn_reg Regular pkn --description "PKN Regular complete model"
python keraswig.py create pkn_gru GRU pkn --description "PKN GRU complete model"
python keraswig.py create pkn_mlp MLP pkn --description "PKN MLP complete model"
python keraswig.py create pkn_gru_2014 GRU pkn --description "PKN GRU partial model" --limit-date 2014-01-01
