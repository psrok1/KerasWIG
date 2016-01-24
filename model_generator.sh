#!/bin/bash

python keraswig.py create wig20_lstm LSTM wig20 --description "WIG20 LSTM complete model"
python keraswig.py create wig20_part LSTM wig20 --description "WIG20 LSTM partial model" --limit-date 2015-11-01
python keraswig.py create bzwbk_lstm LSTM bzw --description "BZWBK LSTM complete model"
python keraswig.py create bzwbk_part LSTM bzw --description "BZWBK LSTM partial model" --limit-date 2015-11-01
python keraswig.py create eur_lstm   LSTM eur --description "Eurocash LSTM complete model"
python keraswig.py create eur_part   LSTM eur --description "Eurocash LSTM partial model" --limit-date 2015-11-01
python keraswig.py create pkn_lstm   LSTM pkn --description "PKN Orlen LSTM complete model"
python keraswig.py create pkn_part   LSTM pkn --description "PKN Orlen LSTM partial model" --limit-date 2015-11-01
python keraswig.py create kgh_lstm   LSTM kgh --description "KGHM LSTM complete model"
python keraswig.py create kgh_part   LSTM kgh --description "KGHM LSTM partial model" --limit-date 2015-11-01
python keraswig.py create pzu_lstm   LSTM pzu --description "PZU LSTM complete model"
python keraswig.py create pzu_part   LSTM pzu --description "PZU LSTM partial model" --limit-date 2015-11-01
python keraswig.py create mbank_lstm LSTM mbk --description "mBank LSTM complete model"
python keraswig.py create mbank_part LSTM mbk --description "mBank LSTM partial model" --limit-date 2015-11-01
