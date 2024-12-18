from fastapi import FastAPI, File, UploadFile
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Force non-interactive backend to avoid Tkinter issues
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Create an instance of the FastAPI application
app = FastAPI()

#Set up CORS middleware to handle cross-origin requests, enabling interaction with front-end applications.
#For production, replace '*' with specific allowed origins for better security.
app.add_middleware(
   CORSMiddleware,
  allow_origins=["*"],  # Allow all origins (use specific origins in production)
   allow_credentials=True,  # Allow cookies and other credentials
   allow_methods=["*"],  # Allow all HTTP methods (e.g., GET, POST, PUT, DELETE)
   allow_headers=["*"],  # Allow all headers
)

# Constants for the linear regression model
W = 1.982015  # Coefficient (slope) of the linear regression model
b = 9.500380  # Intercept (bias) of the linear regression model

@app.get('/')
def default():
    """
    Default endpoint to check if the application is running.

    Returns:
        dict: A simple message indicating the application is running.
    """
    return {'App': 'Running'}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint to perform predictions based on input data from an uploaded CSV file.

    Args:
        file (UploadFile): CSV file containing columns 'inputs' and 'targets'.

    Returns:
        StreamingResponse: A downloadable CSV file with an additional 'predictions' column.
    """
    # Read the uploaded file's contents
    contents = await file.read()

    # Load the contents into a Pandas DataFrame
    df = pd.read_csv(io.BytesIO(contents))

    # Rename columns for better clarity and consistency
    df.columns = ['inputs', 'targets']

    # Perform predictions using the linear regression formula: predictions = W * inputs + b
    df['predictions'] = W * df['inputs'] + b

    # Convert the updated DataFrame to a CSV format
    output = df.to_csv(index=False).encode('utf-8')

    # Return the CSV as a downloadable response with appropriate headers
    return StreamingResponse(
        io.BytesIO(output),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=predictions.csv"}
    )

@app.post("/plot/")
async def plot(file: UploadFile = File(...)):
    """
    Endpoint to generate a plot comparing actual targets and predictions based on input data.

    Args:
        file (UploadFile): CSV file containing columns 'inputs' and 'targets'.

    Returns:
        StreamingResponse: A downloadable PNG image file of the plot.
    """
    # Read the uploaded file's contents
    contents = await file.read()

    # Load the contents into a Pandas DataFrame
    df = pd.read_csv(io.BytesIO(contents))

    # Set up the plot with specified dimensions
    plt.figure(figsize=(10, 6))

    # Create a scatter plot of 'inputs' vs 'targets' to show actual data points
    plt.scatter(
        df['inputs'], df['targets'], color='royalblue', label='Actual Targets', marker='x'
    )

    # Compute predictions using the linear regression formula
    df['predictions'] = W * df['inputs'] + b

    # Calculate the Root Mean Square Error (RMSE) for the predictions
    rmse_score = np.mean(np.square(df['predictions'].values - df['targets'].values))

    # Plot the prediction line
    plt.plot(
        df['inputs'], df['predictions'], color='k', label='Predictions', linewidth=2
    )

    # Add a title with the RMSE value and labels for the axes
    plt.title(
        f'Linear Regression for Stars Data (RMSE: {round(rmse_score, 1)})', 
        color='maroon', fontsize=15
    )
    plt.xlabel('Brightness', color='m', fontsize=13)
    plt.ylabel('Size', color='m', fontsize=13)

    # Display the legend to identify the plotted data
    plt.legend()

    # Save the plot as a PNG image in a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)  # Move the buffer's pointer to the beginning
    plt.close()  # Close the plot to free memory resources

    # Return the image as a downloadable response with appropriate headers
    return StreamingResponse(
        buf,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=plot.png"}
    )
