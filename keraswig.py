import argparse
from predictorModel import *
from predictorLSTM import *


predictors = {
    "LSTM": PredictorLSTM
}

parser = argparse.ArgumentParser(description='Predict stock market trends based on data from stooq.pl')
subparsers = parser.add_subparsers(dest="command")

parser_create = subparsers.add_parser("create", help="Create stock prediction model")
parser_create.add_argument("name", nargs=1, help="Name of used prediction model")
parser_create.add_argument("type", nargs=1, help="Type of prediction model", choices=predictors.keys())
parser_create.add_argument("stock_id", nargs=1, help="Stock identifier")
parser_create.add_argument("description", nargs="?", help="Description of prediction model", default="")

parser_update = subparsers.add_parser("update", help="Update stock prediction model with fresh stock data from stooq.pl")
parser_update.add_argument("name", nargs=1, help="Name of used prediction model")

print("")

args = parser.parse_args()

if args["command"] == "create":
    model = predictors[args["type"]](args["name"])
    model.createModel(args["stock_id"], args["description"])
    model.feedWithStockData()
    model.saveModel()
elif args["command"] == "update":
    model = PredictorModel(args["name"])
    model.loadModel()
    model.feedWithStockData()
    model.saveModel()

