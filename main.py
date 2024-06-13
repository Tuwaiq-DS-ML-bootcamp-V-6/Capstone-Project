




from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel
import numpy as np
import pandas as pd

app = FastAPI()

# GET request
@app.get("/")
def read_root():
    return {"message": "Welcome to SRS Talent Accelerators api"}

# GET request for items
@app.get("/items/")
def create_item(item: dict):
    return {"item": item}

# Load the model
model = joblib.load('rf_model.joblib')

# Define a Pydantic model for input data validation
class InputFeatures(BaseModel):
    Education: str
    Gender: str
    EverBenched: str
    ExperienceInCurrentDomain: int

# Preprocessing function
def preprocessing(input_features: InputFeatures):
    ed = {'Bachelors': 1, 'Masters': 2, 'PHD': 3, 'Diploma': 4}
    gd = {'Male': 1, 'Female': 0}
    ev = {'Yes': 1, 'No': 0}
    dict_f = {
        'Education': ed.get(input_features.Education, 0),
        'Gender': gd.get(input_features.Gender, 0),
        'EverBenched': ev.get(input_features.EverBenched, 0),
        'ExperienceInCurrentDomain': input_features.ExperienceInCurrentDomain,
    }
    return dict_f

@app.post("/predict")
async def predict(input_features: InputFeatures):
    data = preprocessing(input_features)
    df = pd.DataFrame([data])  # Create DataFrame from a list of the dictionary
    # # Convert the DataFrame to a 2D array in the same order as your training data
    n_array = df[['Education', 'ExperienceInCurrentDomain', 'Gender', 'EverBenched']].to_numpy()
    y_probs = model.predict_proba(n_array)
    # Assuming you want the probability of the positive class (usually the second column)
    y_prob_positive_class = y_probs[:, 1]
    # Convert to percentage
    y_prob_percentage = y_prob_positive_class * 100
    y_prob_inverse_percentage = 100 - y_prob_percentage
     # Round to 2 decimal places
    y_prob_rounded = round(y_prob_inverse_percentage[0], 2)
    # Return as a single number
    return y_prob_rounded

