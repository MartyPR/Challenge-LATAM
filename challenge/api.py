from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel
from typing import List
from typing import Optional
from challenge.model import DelayModel  

app = FastAPI()


model = DelayModel()


class FlightData(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int
    Fecha_I: Optional[str] = None  # Hacer opcional
    Fecha_O: Optional[str] = None  

class PredictRequest(BaseModel):
    flights: List[FlightData]

@app.get("/health", status_code=200)
async def get_health() -> dict: 
    return {"status": "OK"}

@app.post("/predict", response_model=dict, status_code=200)
async def post_predict(request: PredictRequest) -> dict:
    try:
        
        data = [
            {
                "OPERA": flight.OPERA,
                "TIPOVUELO": flight.TIPOVUELO,
                "MES": flight.MES,
                "Fecha-O": flight.Fecha_O if flight.Fecha_O else "2023-01-01 00:15:00",
                "Fecha-I": flight.Fecha_I if flight.Fecha_I else "2023-01-01 00:00:00",
            }
            for flight in request.flights
        ]
        df = pd.DataFrame(data)

        
        if df["MES"].max() > 12 or df["MES"].min() < 1:
            raise ValueError("Invalid value for MES: must be between 1 and 12.")
        

           
        preprocessed_data = model.preprocess(df)
        
        predictions = model.predict(preprocessed_data)
       

        return {"predict": predictions}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
