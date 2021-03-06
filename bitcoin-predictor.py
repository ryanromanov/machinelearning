
import quandl, math, datetime
import pandas as pd
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

quandl.ApiConfig.api_key = "Fa83dnsHpaibjtDPhjyF"

df = quandl.get('BCHARTS/COINBASEUSD')

df = df[['Open', 'High', 'Low', 'Close', 'Volume (Currency)',]]
df['HL_PCT'] = (df['High'] - df['Low']) / df ['Close'] * 100.0
df['PCT_change'] = (df['Close'] - df['Open']) / df ['Open'] * 100.0

df = df[['Close','HL_PCT','PCT_change','Volume (Currency)']]

forecast_col = 'Close'
df.fillna(-99999, inplace=True)

# this is how you select how far you want to forecast forward
# it's based on a percent of the total amount of days available
forecast_out = int(math.ceil(0.1*len(df)))

df['label'] = df[forecast_col].shift(-forecast_out)


X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)
X = X[:-forecast_out]
X_lately = X[-forecast_out:]
# stuff that we're going to predict against
# we have x, we need m and b for slope of line

df.dropna(inplace=True)
y = np.array(df['label'])
y = np.array(df['label'])

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

clf = LinearRegression(n_jobs=-1)
#clf = svm.SVR()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

forecast_set = clf.predict(X_lately)

print(forecast_set, accuracy, forecast_out)

df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]
    #df.loc[next_date] sets the next_date as the index

print(df.tail())

df['Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

#print(accuracy)



#print(df.head())
