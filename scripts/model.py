import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score

# Step 1: Data Cleaning
# Load dataset and remove duplicate client entries
df = pd.read_csv('raw/clients.csv')
df = df.drop_duplicates(subset=['client_id'])
df['loan_applied'] = df['loan_applied'].fillna('Unknown')
df['satisfaction_score'] = df['satisfaction_score'].fillna(df['satisfaction_score'].median())

# Calculate Age from date_of_birth
df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
df['Age'] = datetime.now().year - df['date_of_birth'].dt.year
df['Age'] = df['Age'].fillna(df['Age'].median())

# Step 2: Feature Encoding
# Encode categorical variables: client_type, region, acquisition_purpose, referral_channel, country
categorical_cols = ['client_type', 'region', 'acquisition_purpose', 'referral_channel', 'country']
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Step 3: Feature Scaling
# Normalize numeric variables: Age and Satisfaction Score
scaler = StandardScaler()
numeric_cols = ['Age', 'satisfaction_score']
df_encoded[numeric_cols] = scaler.fit_transform(df_encoded[numeric_cols])

# Exclude non-numeric/identifier columns for clustering
features_for_clustering = df_encoded.drop(columns=['client_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'loan_applied'])

# Step 4 & 5: Clustering Model Selection & Optimal Clusters
# Using K-Means to identify 4 optimal buyer segments
kmeans = KMeans(n_clusters=4, random_state=42)
df['Cluster'] = kmeans.fit_predict(features_for_clustering)

# Calculate Silhouette Score to measure clustering quality
sil_score = silhouette_score(features_for_clustering, df['Cluster'])
print(f"Silhouette Score (Quality): {sil_score:.2f}")

# Hierarchical Clustering (for validation)
hc = AgglomerativeClustering(n_clusters=4)
df['HC_Cluster'] = hc.fit_predict(features_for_clustering)

# Save the finalized data for the Streamlit dashboard
df.to_csv('clustured/clustered_clients.csv', index=False)
print("Data processing complete! Clusters saved to 'clustured/clustered_clients.csv'")