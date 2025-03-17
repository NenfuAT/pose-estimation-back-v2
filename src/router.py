# app/routes.py
from fastapi import FastAPI
from pydantic import BaseModel


class URL(BaseModel):
    gyro_url: str
    acc_url: str

def registerRoutes(app: FastAPI):
    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/api")
    async def api_root():
        return {"message": "It's API"}

    @app.post("/api/estimation/quaternion")
    async def quaternionEstimation(urls: URL):
        # コントローラで処理を呼び出す
        response = app.state.ec.EstimationQuaternion(urls.gyro_url, urls.acc_url)
        return response
    
    @app.post("/api/estimation/distance")
    async def distanceEstimation(urls: URL):
        # コントローラで処理を呼び出す
        response = app.state.ec.EstimationDistance(urls.gyro_url, urls.acc_url)
        return response

    @app.post("/api/estimation/pose")
    async def poseEstimation(urls: URL):
        # コントローラで処理を呼び出す
        response = app.state.ec.EstimationPose(urls.gyro_url, urls.acc_url)
        return response
