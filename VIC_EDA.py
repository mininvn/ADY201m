import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

df = pd.read_csv("./generated/crawlPriceVIC.csv", header = 0, delimiter = ",", encoding="unicode_escape")
df['Diff_price'] = df['High'] - df['Low']
df['Diff_day'] = df['Close'] - df['Open']
df['Diff_rate'] = df['Close']/df['Open'] - 1

df.loc[df['Diff_day'] > 0, 'Status'] = 'Inc'
df.loc[df['Diff_day'] <= 0, 'Status'] = 'Dec'
# df.loc[df['Diff_day'] == 0, 'Status'] = 'Same'

# for i in range(4, len(df)):
#     df.loc[i, 'Close_1D'] = df.loc[i - 1, 'Close']
#     df.loc[i, 'Close_2D'] = df.loc[i - 2, 'Close']
#     df.loc[i, 'Close_3D'] = df.loc[i - 3, 'Close']
#     df.loc[i, 'Close_4D'] = df.loc[i - 4, 'Close']

# df.info()
df['Diff_rate'].hist()

# plt.show()
# df = df[3000:]
# values_close = df[['Close']].values

# x = df[['Close_1D', 'Close_2D', 'Close_3D']].values
# values_status = df[['Status']].values

# x_train, x_test, y_train, y_test = train_test_split(x, values_status, test_size = 0.2, random_state = 16)

# model = linear_model.LogisticRegression()
# model.fit(x_train, y_train)

# print(model.score(x_train, y_train))
# # 0.5448818897637795
# print(model.score(x_test, y_test))
# # 0.48427672955974843
# print(model.coef_) 
# # 1.0194 -0.0151 -0.0068
# # Logistic Regression: [[ 0.00064042  0.06823315 -0.07398378]]
# print(model.intercept_)
# # 0.1419
# # Logistic Regression: [0.32821384]
# print(model.predict([[52.9, 53.4, 53.5]]))
# # 52.8
# # Logistic Regression: Inc
arima_model = ARIMA(df[['Open']].values, order=(1, 1, 0))
model = arima_model.fit()
predicts = model.predict()
for i in range(len(predicts)):
    df.loc[i, 'MA'] = predicts[i]
plt.figure(figsize=(20, 10))
df = df[-200:]
plt.plot(df['Open'].values, label = "Actual")
plt.plot(df['MA'].values, label = "MA")
plt.show()
# print(df['MA'])
# print(df['Open'].values)