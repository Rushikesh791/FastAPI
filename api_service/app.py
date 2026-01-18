from fastapi import FastAPI, HTTPException, Query
from typing import List, Annotated, Optional, Literal
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse, HTMLResponse
from pathlib import Path
import json
import pickle
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
model_path = BASE_DIR / "D:\FastAPI\ml_service\insurance_model.pkl"

with open(model_path, "rb") as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


class UserInputs(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age must be between 1 and 119")]
    weight: Annotated[float, Field(..., gt=0, description="Weight must be between 0 and 500 kg")]
    height : Annotated[float, Field(..., gt=0, lt=2.5, description="Height must be greater than 0mtr and less than 2.5mtr")]
    income_lpa : Annotated[float, Field(..., gt=0, description="Income must be a positive value")]
    smoker : Annotated[bool, Field(..., description="Smoker status must be 'yes' or 'no'")]
    city : Annotated[str, Field(..., description="City must be a valid city name")]
    occupation : Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="Occupation must be one of 'retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', or 'private_job'")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def life_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return 'medium'
        else:
            return 'low'
        
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 18:
            return 'child'
        elif 18 <= self.age < 35:
            return 'young_adult'
        elif 35 <= self.age < 60:
            return 'adult'
        else:
            return 'senior'
        
    @computed_field
    @property
    def city_tire(self)-> str:
        if self.city in tier_1_cities:
            return 'tier_1'
        elif self.city in tier_2_cities:
            return 'tier_2'
        else:
            return 'tier_3'
        


@app.post("/predict_insurance")
def predict_insurance(input_data: UserInputs):

    input_df = pd.DataFrame([{
        'bmi': input_data.bmi,
        'age_group': input_data.age_group,
        'life_risk': input_data.life_risk,
        'occupation': input_data.occupation,
        'city_tier': input_data.city_tire,
        'income_lpa': input_data.income_lpa
    }])
        

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code =200, content={"predicted_insurance_Category": prediction})