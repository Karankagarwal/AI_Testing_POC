from pathlib import Path

from sklearn.preprocessing import LabelEncoder
import joblib
import pandas as pd
import os
# Load data from CSV file
file_path = str(Path(__file__).resolve().parent.parent) + '/elements.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Create a LabelEncoder
le = LabelEncoder()

# Fit the LabelEncoder on your data
# You should fit it on all categorical data you have
# This example assumes all data is categorical
encoded_data = {}
for column in df.columns:
    le.fit(df[column].astype(str))  # Convert column to string to ensure categorical encoding
    encoded_data[column] = le.transform(df[column].astype(str))
    # Saving a LabelEncoder for each column with a unique filename
    joblib.dump(le, f'labelencoder_{column}.pkl')

# Now, if you want to use these encoders later, you can load them from disk
# For example, to load the encoder for the 'tag' column:
le_tag = joblib.load('labelencoder_tag.pkl')
