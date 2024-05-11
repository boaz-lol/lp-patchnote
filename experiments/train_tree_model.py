import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report



if __name__ == '__main__':

    csv_file_path = "user_1_match_10.csv"

    # Load Data
    df = pd.read_csv(csv_file_path)

    # Transform Data

    # Transform 1. Label encoding
    encoder = LabelEncoder()
    df['role'] = encoder.fit_transform(df['role'])
    df['puuid'] = encoder.fit_transform(df['puuid']) 

    # Transform 2.  Split feature & target data
    X = df.drop(['win', 'match_id'], axis=1)  
    y = df ['win']

    # Transform 3. Split train & test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Transform 4. Feature scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)   

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Test Inference
    y_pred = model.predict(X_test)

    # Evaluate model
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))