import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd

# Pobieranie danych
ticker = 'AAPL'
data = yf.download(ticker, start="2020-01-01", end="2023-01-01")

# Tworzenie cech
data['MA10'] = data['Close'].rolling(window=10).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()
data = data.dropna()

# Przygotowanie danych do modelu
X = data[['MA10', 'MA50']]
y = data['Close']

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Trenowanie modelu
model = LinearRegression()
model.fit(X_train, y_train)

# Ocena modelu
print(f'R^2 score: {model.score(X_test, y_test)}')
