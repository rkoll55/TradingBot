import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# A kaggle machine learning project I completed on codecademy. This project invovled learning logistic regressoin and data cleaning
# Kaggle link: https://www.kaggle.com/c/titanic

# Load the passenger data
passengers = pd.read_csv('passengers.csv')
passengers['Sex'] = passengers['Sex'].map({'female':'1','male':'0'})

age_mean = int(passengers.Age.mean())
passengers.Age.fillna(
    value = age_mean,
    inplace = True
)
# Create a first class column
passengers['FirstClass'] = passengers['Pclass'].apply(lambda x:1 if x==1 else 0)

# Create a second class column
passengers['SecondClass'] = passengers['Pclass'].apply(lambda x:1 if x==2 else 0)

# Select the desired features
features = passengers[["Sex", "Age", "FirstClass", "SecondClass"]]
#print(features.head())
survival = passengers.Survived

# Perform train, test, split
train_features, test_set, training_labels, test_labels = train_test_split(features,survival)

# Scale the feature data so it has mean = 0 and standard deviation = 1
scaler = StandardScaler()

train_features = scaler.fit_transform(train_features)
test_set = scaler.transform(test_set)

# Create and train the model
model = LogisticRegression()
model.fit(train_features,training_labels)
# Score the model on the train data


print(list(zip(['Sex','Age','FirstClass','SecondClass'],model.coef_[0])))

# Sample passenger features
Jack = np.array([0.0,20.0,0.0,0.0])
Rose = np.array([1.0,17.0,1.0,0.0])
You = np.array([
  0.0,
  48.0,
  0.0,
  0.0
])
# Combine passenger arrays
sample_passengers = np.array([Jack, Rose, You])

# Scale the sample passenger features
sample_passengers = scaler.transform(sample_passengers)

# Make survival predictions!
print(model.predict(sample_passengers))
