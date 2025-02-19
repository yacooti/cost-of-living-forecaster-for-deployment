from fastapi import FastAPI
from api.endpoints import router

application = FastAPI(
    title="Cost of Living Forecaster", 
    description="API for forecasting the cost of living across 20 areas in Nairobi")

application.include_router(router)