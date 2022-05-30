import pandas as pd
from sklearn.tree import DecisionTreeRegressor

# Read dataset
df = pd.read_csv("data.csv", sep=";")
X = df.drop("y", axis=1)
y = df["y"]

# Fit regression model
RegrTree1 = DecisionTreeRegressor(max_depth=2)
RegrTree1.fit(X, y)

# Predict
X_test = [[0.0380759064334241, 0.0506801187398187, 0.0616962065186885, 0.0218723549949558, -0.0442234984244464, -0.0348207628376986, -0.0434008456520269, -0.00259226199818282, 0.0199084208763183, -0.0176461251598052]]
y_1 = RegrTree1.predict(X_test)
print(y_1[0])
import pickle
with open("model.pkl", "wb") as f:
    pickle.dump(RegrTree1, f)
