import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_model():
    print("Starting ML Model training...")
    
    # Check if dataset exists
    csv_path = 'Healthcare.csv'
    if not os.path.exists(csv_path):
        # Default fallback in case path issues
        csv_path = os.path.join(os.path.dirname(__file__), 'Healthcare.csv')
    
    print(f"Reading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Simple cleaning: fill na
    df['Symptoms'] = df['Symptoms'].fillna('')
    df['Disease'] = df['Disease'].fillna('Unknown')
    
    # Preprocessing Symptoms: strip whitespace, convert to lowercase
    # Since symptoms are comma-separated, they can be treated as document text
    # e.g. "fever, back pain, shortness of breath"
    X = df['Symptoms'].apply(lambda x: x.lower().strip())
    y = df['Disease']
    
    # Label encoding for y
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Vectorizing symptoms using TF-IDF
    # We will use sublinear_tf=True and default english stop words (or none, since these are simple medical terms)
    vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b\w[\w\s\-]+\b', lowercase=True)
    X_vectorized = vectorizer.fit_transform(X)
    
    # Train Random Forest Classifier
    # RF works robustly with small datasets and creates non-linear decision boundaries
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_vectorized, y_encoded)
    
    print("Model fit complete.")
    
    # Save the vectorizer, model, and label encoder
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    joblib.dump(label_encoder, 'label_encoder.pkl')
    
    print("Pickle files successfully saved:")
    print("  - model.pkl")
    print("  - vectorizer.pkl")
    print("  - label_encoder.pkl")
    print("ML training complete!")

if __name__ == '__main__':
    train_model()
