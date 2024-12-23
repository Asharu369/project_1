from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development. Change this for production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Linear regression constants
W = 1.982015  # Slope
b = 9.500380  # Intercept

@app.get('/')
def default():
    return {"status": "API is running"}

@app.post("/create_data/")
async def create_data(n_samples: int = Query(500, ge=10, description="Number of samples to generate (min 10)")):
    try:
        X_test = 3 * np.random.rand(n_samples, 1)
        y_test = 9 + 2 * X_test + np.random.rand(n_samples, 1)
        df = pd.DataFrame({"Brightness": X_test.flatten(), "True Size": y_test.flatten()})
        csv_data = df.to_csv(index=False).encode('utf-8')
        return StreamingResponse(io.BytesIO(csv_data), media_type="text/csv",
                                 headers={"Content-Disposition": "attachment; filename=generated_data.csv"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        if "Brightness" not in df.columns or "True Size" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'Brightness' and 'True Size' columns")
        df['Predictions'] = W * df['Brightness'] + b
        csv_data = df.to_csv(index=False).encode('utf-8')
        return StreamingResponse(io.BytesIO(csv_data), media_type="text/csv",
                                 headers={"Content-Disposition": "attachment; filename=predictions.csv"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/plot/")
async def plot(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        if "Brightness" not in df.columns or "True Size" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'Brightness' and 'True Size' columns")
        df['Predictions'] = W * df['Brightness'] + b
        rmse = np.sqrt(np.mean((df['Predictions'] - df['True Size']) ** 2))
        plt.figure(figsize=(10, 6))
        plt.scatter(df['Brightness'], df['True Size'], color='blue', label='True Size')
        plt.plot(df['Brightness'], df['Predictions'], color='red', label='Predictions')
        plt.title(f"Star Size Prediction (RMSE: {rmse:.2f})")
        plt.xlabel("Brightness")
        plt.ylabel("Size")
        plt.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()
        return StreamingResponse(buf, media_type="image/png",
                                 headers={"Content-Disposition": "attachment; filename=plot.png"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

