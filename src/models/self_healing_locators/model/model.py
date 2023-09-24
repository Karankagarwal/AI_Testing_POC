import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib  # Updated import statement

# Load data
df = pd.read_csv('/Users/karanaggarwal/PycharmProjects/POC/AI_Demo/src/models/self_healing_locators/elements.csv')

# Encode strings to numbers since RandomForest requires numerical input
le = LabelEncoder()
df_encoded = df.apply(le.fit_transform)

X = df_encoded.drop('tag', axis=1)
y = df_encoded['tag']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
rf = RandomForestClassifier(n_estimators=50, random_state=0)
rf.fit(X_train, y_train)

# Save the model for later use
joblib.dump(rf, 'model.pkl')

joblib.dump(X_train.columns.tolist(), 'columns.pkl')





