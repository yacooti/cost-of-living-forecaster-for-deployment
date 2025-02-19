from fastapi import APIRouter
from services.cost_of_living_forecaster import CostOfLivingForecaster

router = APIRouter()

@router.get("/")
def home():
    return {"Message": "Welcome to the cost of living forecaster API"}

@router.post("/forecast")
def forecast(year: int = "2026", area: str = "Umoja"):
    forecaster = CostOfLivingForecaster()
    return forecaster.predict(year=year, area=area)