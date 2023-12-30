import os
import boto3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from dotenv import load_dotenv

# Set page configuration
# st.set_page_config(layout="wide")

# Streamlit title
st.title('Y vs X 🚕')

# Load environment variables
load_dotenv()
# AWS Credentials (ensure these are securely set, for example, as environment variables)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize boto3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2'
)

# Function to download file from S3
def download_file_from_s3(bucket_name, s3_file_key, local_file_name):
    s3_client.download_file(bucket_name, s3_file_key, local_file_name)

# Download the file
bucket_name = 'mle-e2e-1'  # Your S3 bucket name
s3_file_key = 'outputs/inference.csv'  # S3 file key
if not os.path.exists('outputs'):
    os.makedirs('outputs')
local_file_name = 'outputs/inference.csv'
download_file_from_s3(bucket_name, s3_file_key, local_file_name)

# Load the data
df = pd.read_csv(local_file_name)

# Plotting
plt.figure(figsize=(5, 3))
plt.scatter(df['y_test'], df['y_pred'], alpha=0.6)  # Scatter plot
plt.plot(df['y_test'], df['y_test'], color='red', linewidth=2)  # Line for perfect predictions
plt.xlabel('')
plt.ylabel('')
plt.title('True vs. Predictions')
plt.legend(['Prediction', 'Perfection'])

# Display the plot in Streamlit
st.pyplot(plt)

# Display the table
# st.table(df)
