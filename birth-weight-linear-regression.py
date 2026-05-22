#%% Installation of required libraries
# pip install pandas numpy seaborn matplotlib statsmodels kagglehub

#%% Import of required libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import kagglehub
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import os

#%% *** 1. LOADING DATA ***

# A. Downloading the latest version of the Pregnancy Data dataset
path = kagglehub.dataset_download('debjeetdas/babies-birth-weight')

# B. Identifying the file in the download directory
files = os.listdir(path)
file_path = os.path.join(path, files[0])

# C. Reading the CSV file
df = pd.read_csv(file_path)
print('BWT Data Preview:', df.head(), df.info())

# D. Create a Figures directory if it doesn't exist
if not os.path.exists('birthweight/Figures'):
    os.makedirs('birthweight/Figures')

#%% *** 2. DATA CLEANING ***

# A. Dropping rows with missing values to ensure model validity
''' bwt: birth weight, gestation: days, age: mother's age, height: mother's height,
weight: mother's weight, smoke: smoking status '''
df_clean = df.dropna(subset=['bwt', 'gestation', 'age', 'height', 'weight', 'smoke']).copy()

# B. Adding BMI variable
# BMI = 703 * weight_lb / (height_in ** 2)
df_clean['bmi'] = 703.0 * df_clean['weight'] / (df_clean['height'] ** 2)

# C. Creating BMI category
def bmi_category(b):
    if pd.isna(b):
        return None
    if b < 18.5:
        return 'Underweight'
    elif b < 25:
        return 'Normal'
    elif b < 30:
        return 'Overweight'
    elif b < 35:
        return 'Obesity (class I)'
    elif b < 40:
        return 'Obesity (class II)'
    else:
        return 'Obesity (class III)'

df_clean['bmi_cat'] = df_clean['bmi'].apply(bmi_category)

#%% *** 3. DESCRIPTIVE ANALYSIS ***
print('--- Summary Statistics ---')
print(df_clean[['bwt', 'gestation', 'age']].describe())

# A. Correlation Heatmap to identify initial relationships
plt.figure(figsize=(10, 8))
sns.heatmap(df_clean[['bwt', 'gestation', 'age']].corr(),
            annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix: Factors Influencing Birth Weight')
plt.savefig('birthweight/Figures/correlation_babies.png')

# B. Frequency of each category of smoke
print(df_clean[['smoke', 'bmi_cat']].value_counts())
print((df_clean[['smoke', 'bmi_cat']].value_counts(normalize=True)*100).round(2))

#%% *** 4. SIMPLE LINEAR REGRESSION ***
# Hypothesis: Smoking during pregnancy lead to lower birth weights
model_simple = ols('bwt ~ C(smoke)', data=df_clean).fit()
print('\n--- Simple Linear Regression: bwt ~ smoke ---')
print(model_simple.summary())

#%% *** 5. MULTIPLE LINEAR REGRESSION ***
# Hypothesis: Gestation, mother's BMI, and age significantly affect birth weight alongside smoking
model_multiple = ols('bwt ~ C(smoke) + gestation + age + C(bmi_cat)',
                     data=df_clean).fit()
print('\n--- Multiple Linear Regression Results ---')
print(model_multiple.summary())

#%% *** 6. RESIDUAL DIAGNOSTICS ***
# Checking if errors follow a normal distribution (OLS Assumption)
plt.figure(figsize=(10, 6))
sns.histplot(model_multiple.resid, kde=True, color='purple')
plt.title('Distribution of Residuals (Multiple Regression)')
plt.xlabel('Residuals')
plt.savefig('birthweight/Figures/residuals_babies.png')
plt.show()

#%% *** 7. VIF ***

# A. Preparing numeric features
features = ['gestation', 'age', 'smoke']
X = df_clean[features].astype(float).copy()

# B. Creating dummies as integers (0/1)
bmi_dummies = pd.get_dummies(df_clean['bmi_cat'], drop_first=True, dtype=int)
X = pd.concat([X, bmi_dummies], axis=1)

# C. Adding constant and dropping any NAs
X_vif = sm.add_constant(X).dropna()

# D. Interpretation Function
def interpret_vif(vif):
    if vif <= 1.5:
        return 'Low (Safe)'
    elif vif <= 5:
        return 'Moderate (Acceptable)'
    elif vif <= 10:
        return 'High (Review)'
    else:
        return 'Very High (Action Required)'

# E. Computing VIF
vif_data = pd.DataFrame()
vif_data['feature'] = X_vif.columns
vif_data['VIF'] = [variance_inflation_factor(X_vif.values, i) for i in range(len(X_vif.columns))]

# F. Applying the interpretation function
vif_data['Status'] = vif_data['VIF'].apply(interpret_vif)

# Filter out constant for cleaner printing
final_vif = vif_data[vif_data['feature'] != 'const'].sort_values(by='VIF', ascending=False)

print('--- Final VIF Results ---')
print(final_vif)