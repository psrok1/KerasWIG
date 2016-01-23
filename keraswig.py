import argparse
from predictorLSTM import *
from csvmgr import stockDayToDatetime
import os.path
import yaml

predictors = {
    "LSTM": PredictorLSTM
}

def modelLoader(model_name, load_model=True):
    if os.path.isfile("models/"+model_name+'.yml'):
        stream = file("models/"+model_name+'.yml', 'r')
        model_description = yaml.load(stream)
        model = predictors[model_description["model_type"]](model_name)
        print "Model "+model_name
        print "\tDescription: "+model_description["description"]
        print "\tPrediction engine: "+model_description["model_type"]
        print "\tStock: "+model_description["csv_id"]+" (to "+model_description["last_day"]+")"
        print ""
        if load_model:
            print "Loading "+model_name+" model..."
            model.loadModel()
        return model
    else:
        return None


parser = argparse.ArgumentParser(description='Predict stock market trends based on data from stooq.pl')
subparsers = parser.add_subparsers(dest="command")

parser_create = subparsers.add_parser("create", help="Create stock prediction model")
parser_create.add_argument("name", nargs=1, help="Name of used prediction model")
parser_create.add_argument("type", nargs=1, help="Type of prediction model", choices=predictors.keys())
parser_create.add_argument("stock_id", nargs=1, help="Stock identifier")
parser_create.add_argument("--description", dest="description", nargs=1, type=str, help="Description of prediction model", default="")
parser_create.add_argument("--limit-date", dest="limitdate", nargs="?", type=str, help="Limit date for model fitting. Date must be in format yyyy-mm-dd.", default="")

parser_update = subparsers.add_parser("update", help="Update stock prediction model with fresh stock data from stooq.pl")
parser_update.add_argument("name", nargs=1, help="Name of used prediction model")

parser_print = subparsers.add_parser("print", help="Print description of stock prediction model")
parser_print.add_argument("name", nargs=1, help="Name of used prediction model")


print("")

args = parser.parse_args()

if args.command == "create":
    model = predictors[args.type[0]](args.name[0])
    model.createModel(args.stock_id[0], args.description[0])
    model.feedWithStockData(limit_date=stockDayToDatetime(args.limitdate))
    model.saveModel()
elif args.command == "update":
    model = modelLoader(args.name[0])
    if model is None:
        print "Model "+args.name[0]+" doesn't exist!"
    else:
        model.feedWithStockData(fresh=True)
        model.saveModel()
elif args.command == "print":
    model = modelLoader(args.name[0], load_model=False)
    if model is None:
        print "Model "+args.name[0]+" doesn't exist!"
