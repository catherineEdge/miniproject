# 1. Import libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# 2. Load dataset
data = pd.read_csv("house.csv")

# 3. Separate input and output
X = data[['Area', 'Bedrooms']]   # features
y = data['Price']               # target

# 4. Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Create model
model = LinearRegression()

# 6. Train model
model.fit(X_train, y_train)

# 7. Predict
y_pred = model.predict(X_test)

# 8. Evaluate model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# 9. Predict new house price
new_house = [[1400, 3]]  # Area=1400, Bedrooms=3
price = model.predict(new_house)
print("Predicted House Price:", price[0])

# 10. Simple visualization
plt.scatter(data['Area'], data['Price'])
plt.xlabel("Area")
plt.ylabel("Price")
plt.title("House Price Prediction")
plt.show()
