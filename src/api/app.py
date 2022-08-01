
from flask import Flask, request
from joblib import load
import json
from pathlib import Path

folder_path = Path(__file__).parent

# load model
model_path = folder_path.joinpath('resources', 'posology-model.joblib')
model = load(model_path)

# create app
app = Flask(__name__)

def predict_posology(query):
    """predict if query is posology instruction

    Args:
        query (list(str)): list of instructions to predict
        model (sklearn.pipeline.Pipeline): pipeline containing vectorizer and model

    Returns:
        list(int): list of 0 and 1. 1 if instruction is posology 0 otherwise
    """
    # 
    # return the prediction
    return model.predict(query)

@app.route('/posology', methods = ['POST','GET'])
def is_posology():
    # get posology instruction from query params
    # query = request.get_json()
    # query = query["q"]
    # the pipe(|) separator is used to enable prediction of multiple instructions
    queries =  request.args.get('query').split('|')
    print("query", queries)
    # TODO: check that query is not None

    queries_size = len(queries)
    if queries_size == 0:
        return {}

    pred = predict_posology(queries)
    if queries_size == 1:
        return json.dumps({
            "query": queries[0],
            "is_posology": bool(pred[0] == 1)
        })
    
    # if multiple instructions
    predictions = []
    for i in range(queries_size):
        predictions.append({
            "query": queries[i],
            "is_posology": bool(pred[i] == 1)
        })
    return json.dumps(predictions)

if __name__ =="__main__" :
    print("start app")
    app.run(debug = True)