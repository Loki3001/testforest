# -*- coding: utf-8 -*-
"""foresthealth.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-iGYnYLMxqZ_pRhjtaavE44JNOr666Oz

**Forest Health prediciton **
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor

file_path = '/content/forest_health_data (2).csv'
dataset = pd.read_csv(file_path)

print(dataset)

print(dataset.columns)

dataset.shape

dataset.info()

dataset.describe()

dataset.isnull().sum()

dataset.isnull().sum().any()

for column_name in dataset.columns:
    column = dataset[column_name]
    # Get the count of Zeros in column
    count = (column == 0).sum()
    print('Count of zeros in column ', column_name, ' is : ', count)

dataset.duplicated().sum()

sns.set()
plt.hist(dataset['Latitude'])

sns.set()
plt.hist(dataset['Tree_Height'])

sns.set()
plt.hist(dataset['Crown_Width_North_South'])

sns.set()
for column in dataset.columns[3:]:
    sns.boxplot(data=dataset, y=column)  # Create box plot for the current column
    plt.title(f"Box Plot of {column}")  # Add title to the plot
    plt.show()  # Display the plot

sns.set()
dataset.hist(figsize=(20,20));

plt.figure(figsize=(20, 20))
# Select only numeric features for correlation calculation
numeric_features = dataset.select_dtypes(include=np.number)
sns.heatmap(numeric_features.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()

#EDA
sns.boxplot(data = dataset , y = "DBH", x = 'Health_Status')

#Exploratory Data Analysis (EDA)
plt.figure(figsize=(8, 4))
sns.countplot(x='Health_Status', data=dataset)
plt.title("Distribution of Health Status")
plt.show()

sns.violinplot(data =dataset, x = 'Soil_TN', y = 'Health_Status')

sns.scatterplot(data = dataset ,x = 'Fire_Risk_Index', y = 'Health_Status')



# Identify categorical columns
categorical_columns = data.select_dtypes(include=['object']).columns
print("Categorical Columns:", categorical_columns)

# Apply one-hot encoding to categorical variables
data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)
print("Data Shape After Encoding:", data.shape)

from sklearn.preprocessing import StandardScaler

# Initialize the scaler
scaler = StandardScaler()

# Scale numerical columns
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])
print("Data After Scaling:\n", data.head())

# Final data check
print("Final Data Shape:", data.shape)
print("Final Data Sample:\n", data.head())

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", conf_matrix)

class_report = classification_report(y_test, y_pred)
print("Classification Report:\n", class_report)

feature_importances = rf_model.feature_importances_
features = X.columns
importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importances}).sort_values(by='Importance', ascending=False)
print("Feature Importances:\n", importance_df)

"""# **Biavariate Analysis**

"""

# Visualize feature importances
plt.figure(figsize=(10, 6))
sns.barplot(x=importance_df["Importance"], y=importance_df["Feature"], palette="viridis")
plt.title("Feature Importances in Random Forest Classifier")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=dataset, x="DBH", y="Tree_Height", hue="Health_Status", palette="viridis")
plt.title("Scatter Plot of DBH vs Tree Height by Health Status")
plt.xlabel("DBH (Diameter at Breast Height)")
plt.ylabel("Tree Height")
plt.legend(title="Health Status")
plt.show()

sns.pairplot(dataset, hue="Health_Status", vars=["Soil_TN", "Soil_TP", "Soil_AP", "Soil_AN"], palette="magma")
plt.suptitle("Soil Nutrients by Health Status", y=1.02)
plt.show()

"""**Menhinick Index and Gleason Index:**
These are biodiversity indices. Higher biodiversity might correlate with healthier ecosystems, which could impact tree health.



"""

plt.figure(figsize=(10, 6))
sns.scatterplot(data=dataset, x="Menhinick_Index", y="Gleason_Index", hue="Health_Status", palette="cool")
plt.title("Scatter Plot of Menhinick Index vs Gleason Index by Health Status")
plt.xlabel("Menhinick Index")
plt.ylabel("Gleason Index")
plt.legend(title="Health Status")
plt.show()

"""### **Fire Risk Index vs. Disturbance Level:**"""

plt.figure(figsize=(10, 6))
sns.scatterplot(data=dataset, x="Fire_Risk_Index", y="Disturbance_Level", hue="Health_Status", palette="Spectral")
plt.title("Scatter Plot of Fire Risk Index vs Disturbance Level by Health Status")
plt.xlabel("Fire Risk Index")
plt.ylabel("Disturbance Level")
plt.legend(title="Health Status")
plt.show()

"""# confusion matrix **visualization**"""

class_labels = ["Healthy", "Unhealthy", "Sub-Healthy"]  # Adjust according to your labels

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_labels, yticklabels=class_labels)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix with Custom Labels")
plt.show()

# Display the sorted feature importance DataFrame
print(importance_df.sort_values(by="Importance", ascending=False).head())

# Replace 'Tree_Height' with your chosen top feature
top_feature = "Tree_Height"  # Or another feature from importance_df

plt.figure(figsize=(10, 6))
sns.boxplot(x=y_test, y=X_test[top_feature])
plt.xlabel("Class")
plt.ylabel("Tree Height")  # Adjust label based on selected feature
plt.title("Distribution of Tree Height by Class")
plt.show()

