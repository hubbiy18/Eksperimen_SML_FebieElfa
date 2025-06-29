import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from scipy.stats import zscore
import os

def preprocess_diabetes_dataset(filepath, save_cleaned=True):
    """
    Fungsi untuk memuat dan melakukan preprocessing dataset diabetes.

    Tahapan preprocessing:
    1. Load dataset
    2. Drop duplikat
    3. Tangani missing values
    4. Encode data kategorikal
    5. Deteksi & hapus outlier (Z-score)
    6. Normalisasi fitur numerik
    7. Simpan data bersih ke file CSV (opsional)
    8. Return dataframe bersih
    """

    # 1. Load dataset
    df = pd.read_csv(filepath)
    print(f"Data awal: {df.shape[0]} baris, {df.shape[1]} kolom")

    # 2. Drop duplicates
    df = df.drop_duplicates()

    # 3. Handle missing values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)

    # 4. Encode categorical features
    categorical_cols = df.select_dtypes(include='object').columns
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    # 5. Remove outliers with Z-score (exclude binary/target cols)
    exclude_cols = ['hypertension', 'heart_disease', 'diabetes']
    numeric_cols = df.select_dtypes(include=np.number).columns.difference(exclude_cols)
    z_scores = df[numeric_cols].apply(zscore)
    df = df[(np.abs(z_scores) < 3).all(axis=1)]
    print(f"Setelah hapus outlier: {df.shape[0]} baris")

    # 6. Feature scaling
    features_to_scale = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    scaler = StandardScaler()
    df[features_to_scale] = scaler.fit_transform(df[features_to_scale])

    # 7. Verifikasi data setelah preprocessing
    print(f"Data setelah preprocessing: {df.shape[0]} baris, {df.shape[1]} kolom")

    # 8. Save cleaned dataset (pastikan direktori kerja benar)
    if save_cleaned:
        output_path = os.path.join(os.getcwd(), "diabetes_cleaned.csv")  # Tentukan lokasi file
        df.to_csv(output_path, index=False)
        print(f"Data bersih disimpan ke '{output_path}'")

    # 9. Return cleaned dataframe
    print("Distribusi label diabetes:\n", df['diabetes'].value_counts())
    return df

# Memanggil fungsi dengan path dataset yang benar dan memastikan file disimpan
dataset_filepath = 'diabetes_prediction_dataset.csv'  # Ganti dengan path file Anda
preprocess_diabetes_dataset(dataset_filepath, save_cleaned=True)
