import uvicorn
from fastapi import FastAPI

import joblib
import json

from youth_data import YouthData
from preprocessing import preprocess_input

app = FastAPI()

model = joblib.load("../model/youth_income_pred.joblib") # Load model

@app.get("/")
def index():
    return {"message": "Welcome to the Youth Employment Status Predictor"}

@app.post("/predict")
def predict(input_parameters: YouthData):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    input_df = preprocess_input(input_dictionary)

    column_transformer = model["col_transformer"] # Load saved column transformer 
    classifier =  model["classifier"] # Load trained classifier

    x_input = column_transformer.transform(input_df) # Perform column transformation on input data
    
    prediction = classifier.predict(x_input) # Make Prediction on user input

    if prediction[0] == 0:
        return "Predicted employee status = Unemployed"
    else:
        return "Predicted employee status = Employed"
