# Infant Birth Weight Analysis: Biological and Lifestyle Determinants
This project conducts a comprehensive statistical analysis of the factors influencing newborn birth weight (in ounces). Using a dataset of 1,174 cleaned records, we explore how gestation, maternal development (Age/BMI), and smoking habits interact to determine neonatal outcomes.

## Key Research Findings
### 1. The "Smoking Penalty"
The most significant modifiable risk factor identified is smoking.
* Simple Model: Smoking alone explains 6% of the variance in birth weight, with babies of smokers weighing 9.27 oz less on average.
* Controlled Model: Even when adjusting for gestation, age, and BMI, the penalty remains severe: -8.22 oz (p < 0.001).
### 2. Gestation and Maternal BMI
* Gestation: Remains the strongest biological predictor (p < 0.001). Every additional day of pregnancy adds approximately 0.46 oz to the birth weight.
* Underweight Impact: Mothers classified as "Underweight" (BMI < 18.5) give birth to infants weighing 3.79 oz less (p = 0.042) than those in the "Normal" BMI category.
* Obesity Classes: While the coefficients for Obesity (Class I-III) were positive (indicating heavier babies), they were not statistically significant in this sample, likely due to lower frequency in those specific groups.
### 3. Model Robustness (VIF Analysis)
To ensure the reliability of our Multiple Regression, we performed a Variance Inflation Factor (VIF) analysis. All predictors (Gestation, Age, Smoke, BMI Categories) showed VIF values < 1.1, confirming there is no multicollinearity and that each variable contributes unique information to the model.

## Data Engineering and Methodology
### Feature Engineering: BMI
We calculated the Mother's Body Mass Index (BMI) using the formula:
$$\text{BMI} = 703 \times \frac{\text{weight (lb)}}{\text{height (in)}^2}$$
The population was then stratified into 6 clinical categories: Underweight, Normal, Overweight, and Obesity (Class I, II, III).
## Project Structure
* bwt_linear_regression.py: Full script including VIF calculation and BMI categorization.
* Figures/:
* correlation_babies.png: Heatmap showing biological correlations.
* residuals_babies.png: Histogram verifying the normality of errors (OLS assumption).

## Public Health Implications
The findings underscore a critical public health challenge: the significant impact of modifiable lifestyle factors and maternal nutritional status on neonatal outcomes. The identified 'smoking penalty' of over 8 ounces, regardless of gestation length, suggests that prenatal smoking cessation programs could yield measurable improvements in birth weight distributions.
