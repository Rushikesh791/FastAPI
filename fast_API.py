from fastapi import FastAPI, Path, HTTPException, Query
from typing import List, Annotated, Optional, Literal
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse, HTMLResponse
import json
import pickle
import pandas as pd


with open('insurance_model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()





class user_input(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age must be between 1 and 119")]
    weight: Annotated[float, Field(..., gt=0, lt=500, description="Weight must be between 0 and 500 kg")]