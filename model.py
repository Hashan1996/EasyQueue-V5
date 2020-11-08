
# 1. Import Required Libraries
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
import pickle
import seaborn as sns
from sklearn.tree import DecisionTreeRegressor
from matplotlib import pyplot
import matplotlib.ticker

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier 

from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error

# 2. Import csv file
#df = pd.read_csv('report.csv')
df = pd.read_csv (r'C:\Users\USER\Downloads\report.csv') 


# 3. Data Pre-processing

# 3.1- Change date datatype
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# 3.2- Date divided to Year, Month, Week and Weekdays
df['Year'] = df.Date.dt.year
df['Month'] = df.Date.dt.month
df['Week'] = df.Date.dt.week
df['Week Day'] = df['Day'].replace(['Monday', 'Tuesday','Wednesday','Thursday', 'Friday','Saturday'], [1, 2, 3, 4, 5, 6])
df['TimeRangeInt'] = df['Time Range'].replace(['Morning', 'Evening'], [1, 2])

# 3.3- Remove columns ID,Date,Day,Time Range
df.drop(['Cutomer Count ID', 'Date', 'Day', 'Time Range'], axis=1, inplace=True)

# 3.4- Split columns
data = df[['Year', 'Month', 'Week', 'Week Day', 'TimeRangeInt', 'Customer Count']]

# 3.5- Check dataset
finalData = df[['Year', 'Month', 'Week', 'Week Day','TimeRangeInt', 'Customer Count']]


# 4. Data Visualising

# 4.1- Show Graph

# 4.1.1- Customer Count Vs Year

ax = finalData.plot(x='Year', y='Customer Count', style='o')
ax.locator_params(integer=True)
plt.title('Customer Count Vs Year')
plt.xlabel('Year')
plt.ylabel('Customer Count')
#plt.show()

# 4.1.2- Customer Count Vs Week Day
finalData.plot(x='Month', y='Customer Count', style='o')
plt.title('Customer Count Vs Month')
plt.xlabel('Month')
plt.ylabel('Customer Count')
#plt.show()

# 4.1.3- Customer Count Vs Week Day
finalData.plot(x='Week', y='Customer Count', style='o')
plt.title('Customer Count Vs Week')
plt.xlabel('Week')
plt.ylabel('Customer Count')
#plt.show()

# 4.1.4- Customer Count Vs TimeRangeInt
ax = finalData.plot(x='TimeRangeInt', y='Customer Count', style='o')
ax.locator_params(integer=True)
plt.title('Customer Count Vs TimeRangeInt')
plt.xlabel('TimeRangeInt')
plt.ylabel('Customer Count')
#plt.show()


# 5. Split data into X and Y

# 5.1- Drop Customer Count for train  model
# X values are 'Service Counter ID', 'Year', 'Month', 'Week', 'weekdayInt', 'TimeRangeInt' (independent variables)
X = finalData.iloc[:, :5]

#5.2- Dependent Varialble
# Y is Customer Count(target/dependent variable)
Y = finalData.iloc[:, -1]


# 6. Train Model

# 6.1- Split the data into train and test sets for train  model
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=3)


# 7. Evaluating Model (Accuracy & Mean Squared Error)
print("***********************************************************************")

# 7.1- GaussianNB Algorithm
# fit model on training data
gaussianNB_regressor = GaussianNB()
gaussianNB_regressor.fit(X, Y)
# make predictions for test data
gaussianNB_y_pred = gaussianNB_regressor.predict(X_test)
#predictions = [round(value) for value in y_pred]
#evaluate model
accuracy = accuracy_score(y_test, gaussianNB_y_pred)
print("GaussianNB Model Accuracy: %.2f%%" % (accuracy * 100.0))
# MSE Computation 
mse = mean_squared_error(y_test, gaussianNB_y_pred)
print("GaussianNB Model Mean Squared  Error : % f" %(mse))


print("***********************************************************************")

# 7.2- GradientBoostingClassifier Algorithm
# fit model on training data
gradientBoostingClassifier_regressor = GradientBoostingClassifier()
gradientBoostingClassifier_regressor.fit(X, Y)
# make predictions for test data
gradientBoostingClassifier_y_pred = gradientBoostingClassifier_regressor.predict(X_test)
#predictions = [round(value) for value in y_pred]
#evaluate model
accuracy = accuracy_score(y_test, gradientBoostingClassifier_y_pred)
print("GradientBoostingClassifier Model Accuracy: %.2f%%" % (accuracy * 100.0))
# MSE Computation 
mse = mean_squared_error(y_test, gradientBoostingClassifier_y_pred)
print("GradientBoostingClassifier Model Mean Squared  Error : % f" %(mse))


print("***********************************************************************")

# 7.3- Decission Tree Algorithm
# fit model on training data
decissionTree_regressor = DecisionTreeClassifier()
decissionTree_regressor.fit(X, Y)

# 7.3.1- Coefficients as Feature Importance of Decision Tree Algorithm

# Get importance
importance = decissionTree_regressor.feature_importances_

# Summarize feature importance
#for i,v in enumerate(importance):
	#print('Feature: %0d, Score: %.5f' % (i,v))

# Plot feature importance
pyplot.bar([x for x in range(len(importance))], importance)
#pyplot.show()


# make predictions for test data
decissionTree_y_pred = decissionTree_regressor.predict(X_test)
#evaluate model
accuracy = accuracy_score(y_test, decissionTree_y_pred)
print("Decission Tree Model Accuracy: %.2f%%" % (accuracy * 100.0))
# MSE Computation 
mse = mean_squared_error(y_test, decissionTree_y_pred)
print("Decission Tree Model Mean Squared  Error : % f" %(mse))


print("***********************************************************************")

# 8. Load the model to deployement
pickle.dump(decissionTree_regressor, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))

# 'Year', 'Month', 'Week', 'Week Day','DepCounterInt', 'TimeRangeInt'
#print(model.predict([[2019, 1, 1, 2, 1]]))
