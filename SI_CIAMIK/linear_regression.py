import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Fungsi untuk membaca data dari file CSV dan membagi menjadi fitur dan target
def read_data(file_path, target_column='2'):
    df = pd.read_csv(file_path)
    
    # Pastikan kolom yang hendak dihapus ada dalam dataframe
    columns_to_drop = ['nama'] + [str(i) for i in range(3, 8)]
    existing_columns = set(df.columns)
    columns_to_drop = [col for col in columns_to_drop if col in existing_columns]

    X = df.drop(columns=columns_to_drop)  # Fitur
    y = df[target_column]  # Target
    return X, y

def train_and_evaluate_model(X_train, y_train, X_val, y_val, X_test, y_test):
    # Inisialisasi model Linear Regression
    model = LinearRegression()

    # Latih model
    model.fit(X_train, y_train)

    # Prediksi pada data validasi
    y_val_pred = model.predict(X_val)

    # Evaluasi pada data validasi
    mse_val = mean_squared_error(y_val, y_val_pred)
    r2_val = r2_score(y_val, y_val_pred)

    # Prediksi pada data uji
    y_test_pred = model.predict(X_test)

    # Evaluasi pada data uji
    mse_test = mean_squared_error(y_test, y_test_pred)
    r2_test = r2_score(y_test, y_test_pred)

    return {
        'model': model,
        'MSE (Validation)': mse_val,
        'R-squared (Validation)': r2_val,
        'MSE (Test)': mse_test,
        'R-squared (Test)': r2_test,
        'Predictions (Validation)': y_val_pred,
        'Predictions (Test)': y_test_pred
    }

# Fungsi untuk membaca dataset dan melakukan pembelajaran
def train_model():
    # Nama file dataset
    dataset = "dummy-ml-semester2.csv"

    print(f"\nTraining Linear Regression Model using {dataset}")

    # Membaca dataset
    X, y = read_data(dataset)

    # Membagi data menjadi data latih, data validasi, dan data uji
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Melatih dan mengevaluasi model Linear Regression
    results = train_and_evaluate_model(X_train, y_train, X_val, y_val, X_test, y_test)

    # Menampilkan hasil evaluasi
    for metric, value in results.items():
        print(f"{metric}: {value}")

    # Plot hasil prediksi pada data validasi dan data uji
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.scatter(y_val, results['Predictions (Validation)'])
    plt.title("Linear Regression - Validation Set")
    plt.xlabel("True Values")
    plt.ylabel("Predictions")

    plt.subplot(1, 2, 2)
    plt.scatter(y_test, results['Predictions (Test)'])
    plt.title("Linear Regression - Test Set")
    plt.xlabel("True Values")
    plt.ylabel("Predictions")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    train_model()